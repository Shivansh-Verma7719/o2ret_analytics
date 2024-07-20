const puppeteer = require('puppeteer');
const xlsx = require('xlsx');

const cities = ['mumbai', 'pune', 'bengaluru', 'ahmedabad', 'jaipur', 'hyderabad', 'coimbatore', 'kolkata', 'delhi', 'chennai'];

(async () => {
    // Launch Puppeteer
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    const allData = [];

    for (const city of cities) {
        // Navigate to the provided URL
        await page.goto(`https://dir.indiamart.com/search.mp?ss=telematics+device&prdsrc=1&cq=${city}&v=4&qry_typ=P&current_mcatid=116804&lang=en&wc=2&mcatid=20677&catid=739&qr_nm=gd&res=RC4&com-cf=nl&ptrs=na&ktp=N0&mtp=S&Brand=BM&stype=attr%3D1%7Cbr&Mspl=0`, {
            waitUntil: 'networkidle0',
        });

        // Scroll the page down by a significant amount once to load more products
        await page.evaluate(() => {
            window.scrollBy(0, window.innerHeight * 3);
        });
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds to load new content

        // Evaluate the page to extract the required data
        const data = await page.evaluate((city) => {
            const listings = [];
            document.querySelectorAll('.listingCardContainer .card').forEach(card => {
                const productTitleElement = card.querySelector('.producttitle .elps a');
                const priceElement = card.querySelector('.price');
                const sellerElement = card.querySelector('.companyname a');
                const locationElement = card.querySelector('.newLocationUi span.elps1');

                const productTitle = productTitleElement ? productTitleElement.textContent.trim() : null;
                const productLink = productTitleElement ? productTitleElement.href : null;
                const price = priceElement ? priceElement.textContent.replace('₹', '').trim() : null;
                const seller = sellerElement ? sellerElement.textContent.trim() : null;
                const location = city;

                listings.push({
                    productTitle,
                    productLink,
                    price,
                    seller,
                    location,
                });
            });
            return listings;
        }, city);

        allData.push(...data);
    }

    // Close the browser
    await browser.close();

    // Convert the data to a worksheet
    const worksheet = xlsx.utils.json_to_sheet(allData);

    // Create a new workbook and append the worksheet
    const workbook = xlsx.utils.book_new();
    xlsx.utils.book_append_sheet(workbook, worksheet, 'Telematics Data');

    // Write the workbook to a file
    xlsx.writeFile(workbook, 'telematics_data.xlsx');

    console.log('Data has been written to telematics_data.xlsx');
})();
