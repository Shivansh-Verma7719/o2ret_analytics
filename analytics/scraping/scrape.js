const puppeteer = require('puppeteer');
const XLSX = require('xlsx');

(async () => {
  // Launch Puppeteer
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Navigate to the target URL
  await page.goto('https://gps-trace.com/en/hardware', { waitUntil: 'networkidle2' });
  
  // Wait for the necessary elements to load
  await page.waitForSelector('.manufacturer__link');

  // Scrape manufacturer names and links
  const data = await page.evaluate(() => {
    const items = document.querySelectorAll('.manufacturer__link');
    const result = [];
    items.forEach(item => {
      const manufacturer = item.querySelector('span').innerText;
      const link = item.href;
      result.push({ manufacturer, link });
    });
    return result;
  });

  // Close the browser
  await browser.close();

  // Create a new workbook and add the data to a sheet
  const workbook = XLSX.utils.book_new();
  const worksheet = XLSX.utils.json_to_sheet(data);
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Manufacturers');

  // Save the workbook to an Excel file
  XLSX.writeFile(workbook, 'manufacturers.xlsx');

  console.log('Scraping completed and data saved to manufacturers.xlsx');
})();
