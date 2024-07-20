const puppeteer = require('puppeteer');
const XLSX = require('xlsx');

(async () => {
  // Read the manufacturers data from Excel
  const workbook = XLSX.readFile('manufacturers.xlsx');
  const sheetName = workbook.SheetNames[0];
  const sheet = workbook.Sheets[sheetName];
  const manufacturers = XLSX.utils.sheet_to_json(sheet);

  // Initialize Puppeteer
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const products = [];

  // Loop through each manufacturer
  for (const manufacturer of manufacturers) {
    const { manufacturer: manufacturerName, link: manufacturerLink } = manufacturer;
    console.log(`Scraping products for manufacturer: ${manufacturerName}`);

    await page.goto(manufacturerLink, { waitUntil: 'networkidle2' });

    try {
      await page.waitForSelector('.device__link', { timeout: 30000 });

      // Scrape product details
      const productData = await page.evaluate(() => {
        const items = document.querySelectorAll('.device__link');
        const result = [];
        items.forEach(item => {
          const productName = item.querySelector('span').innerText;
          const productLink = item.href;
          result.push({ productName, productLink });
        });
        return result;
      });

      // Append the manufacturer name to each product
      productData.forEach(product => {
        product.manufacturer = manufacturerName;
        products.push(product);
      });

      // Log the number of products scraped for this manufacturer
      console.log(`Scraped ${productData.length} products for manufacturer: ${manufacturerName}`);
    } catch (error) {
      // Handle the case where no products are found
      if (error.name === 'TimeoutError') {
        console.log(`No products found for manufacturer: ${manufacturerName}`);
      } else {
        console.log(`An error occurred while scraping ${manufacturerName}: ${error.message}`);
      }
    }
  }

  // Close the browser
  await browser.close();

  // Create a new workbook and add the data to a sheet
  const newWorkbook = XLSX.utils.book_new();
  const newWorksheet = XLSX.utils.json_to_sheet(products);
  XLSX.utils.book_append_sheet(newWorkbook, newWorksheet, 'Products');

  // Save the workbook to an Excel file
  XLSX.writeFile(newWorkbook, 'products.xlsx');

  console.log('Scraping completed and data saved to products.xlsx');
})();
