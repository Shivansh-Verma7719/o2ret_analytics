const puppeteer = require("puppeteer");
const xlsx = require("xlsx");

function delay(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

async function blinkit(keyword, pincode) {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--incognito"],
  });
  const context = await browser.createIncognitoBrowserContext();
  const page = await context.newPage();
  await page.setViewport({ width: 1280, height: 800 });

  const url = `https://blinkit.com/s/?q=${keyword}`;
  await page.goto(url, { waitUntil: "networkidle2" });

  // Find and set the location input field
  const locationInputSelector =
    "xpath=/html/body/div[1]/div/div/div[1]/header/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input";
  await page.waitForSelector(locationInputSelector);

  // Type pincode with a delay
  await page.type(locationInputSelector, pincode, { delay: 500 });

  // Wait for autocomplete options to appear and select the correct one
  const autocompleteOptionsSelector =
    ".LocationSearchList__LocationLabel-sc-93rfr7-2";
  await page.waitForSelector(autocompleteOptionsSelector);
  const options = await page.$$(autocompleteOptionsSelector);

  let locationFound = false;
  for (const option of options) {
    const text = await page.evaluate((el) => el.textContent, option);
    if (text.includes(`${pincode}`)) {
      await option.click();
      locationFound = true;
      break;
    }
  }

  if (!locationFound) {
    console.log(`Location not found for pincode ${pincode}.`);
    await browser.close();
    return [];
  }
  await delay(2000); // Wait for 2 seconds to load more products

  // Check for non-servicability warning
  const nonServicableSelector = ".non-serviceable-step";
  const nonServicable = await page.$(nonServicableSelector);
  if (nonServicable) {
    console.log(`Pincode ${pincode} is not serviceable.`);
    await browser.close();
    return [
      {
        pincode,
        name: "N/A",
        deliveryTime: "N/A",
        price: "N/A",
        discount: "N/A",
        nonServicable: true,
      },
    ];
  }

  // Wait for products to load
  const productSelector = 'a[data-test-id="plp-product"]';
  await page.waitForSelector(productSelector);

  // Scroll to the bottom of the page multiple times to load all products
  let previousHeight;
  while (true) {
    previousHeight = await page.evaluate("document.body.scrollHeight");
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
    await delay(1500); // Wait for 1.5 seconds to load more products
    const newHeight = await page.evaluate("document.body.scrollHeight");
    if (newHeight === previousHeight) break;
  }

  const products = await page.$$(productSelector);
  const productDetails = [];

  for (let i = 0; i < Math.min(products.length, 15); i++) {
    const product = products[i];
    const productDetail = await page.evaluate(
      (el, pincode) => {
        const name =
          el.querySelector(".Product__UpdatedTitle-sc-11dk8zk-9")
            ?.textContent || "N/A";
        const deliveryTime =
          el.querySelector(".Product__UpdatedETAContainer-sc-11dk8zk-6")
            ?.textContent || "N/A";
        const price =
          el.querySelector(
            ".Product__UpdatedPriceAndAtcContainer-sc-11dk8zk-10 > div > div"
          )?.textContent || "N/A";
        const discount =
          el.querySelector(".Product__UpdatedOfferTitle-sc-11dk8zk-2")
            ?.textContent || "N/A";
        return { name, deliveryTime, price, discount, pincode };
      },
      product,
      pincode
    );
    productDetails.push(productDetail);
  }

  await browser.close();
  return productDetails;
}

async function saveResultsToExcel(results) {
  // Transform the results to the desired format
  const transformedResults = results.map((result) => {
    const row = {
      Pincode: result.Pincode,
      "Search Term": result["Search Term"],
    };
    result.products.forEach((product, index) => {
      row[
        `Product${index + 1}`
      ] = `${product.name}, ${product.deliveryTime}, ${product.price}, ${product.discount}`;
    });
    return row;
  });

  // Create Excel file with transformed results
  const wb = xlsx.utils.book_new();
  const ws = xlsx.utils.json_to_sheet(transformedResults);
  xlsx.utils.book_append_sheet(wb, ws, "Products");
  xlsx.writeFile(wb, "blink-items-structured.xlsx");
  console.log("Progress saved to blink-items-structured.xlsx");
}

// Declare the results array in the outer scope
const results = [];

async function runScraping() {
  const workbook = xlsx.readFile("yoga-bar.xlsx");
  const sheetName = workbook.SheetNames[0];
  const sheet = workbook.Sheets[sheetName];
  const data = xlsx.utils.sheet_to_json(sheet);

  for (const row of data) {
    const pincode = row.Pincode;
    if (!pincode) {
      console.log(`Skipping row with missing pincode: ${JSON.stringify(row)}`);
      continue;
    }

    console.log(`Scraping for pincode: ${pincode}`);

    try {
      const brandedResults = await blinkit("yoga bar", pincode.toString());
      const genericResults = await blinkit("protein bar", pincode.toString());

      results.push({
        Pincode: pincode.toString(),
        "Search Term": "yoga bar",
        products: brandedResults,
      });

      results.push({
        Pincode: pincode.toString(),
        "Search Term": "protein bar",
        products: genericResults,
      });
    } catch (error) {
      console.error(`Error scraping pincode ${pincode}:`, error);
    }
  }

  await saveResultsToExcel(results);
  console.log("Scraping and file creation done.");
}

// Handle Ctrl+C to save progress
process.on("SIGINT", async () => {
  console.log("Ctrl+C detected, saving progress...");
  await saveResultsToExcel(results);
  process.exit();
});

runScraping();
