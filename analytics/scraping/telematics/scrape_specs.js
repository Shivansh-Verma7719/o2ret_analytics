const puppeteer = require('puppeteer');
const xlsx = require('xlsx');
const fs = require('fs');

// const locationToScrape = 'chennai'; // Change this variable to the desired location

// Load the Excel file
const workbook = xlsx.readFile('telematics_data_with_specs_interrupted.xlsx');
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];

// Convert the worksheet to JSON format
let data = xlsx.utils.sheet_to_json(worksheet);

// Function to add a delay
function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

// Function to extract product information
async function extractProductInfo(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set a custom user agent and referrer
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
    await page.setExtraHTTPHeaders({
        'referrer': 'https://www.google.co.in/'
    });

    await page.goto(url, { waitUntil: 'networkidle0' });

    const productSpecSelector = '#pdpD div.dtlsec1 div table tbody';

    const specs = await page.evaluate((selector) => {
        const rows = document.querySelectorAll(selector + ' tr');
        return Array.from(rows).map(row => {
            const columns = row.querySelectorAll('td');
            return `${columns[0].innerText}: ${columns[1].innerText}`;
        }).join(', ');
    }, productSpecSelector);

    await browser.close();
    return { specs };
}

// Function to save data to Excel file
function saveToExcel(data, filename) {
    const newWorksheet = xlsx.utils.json_to_sheet(data);
    const newWorkbook = xlsx.utils.book_new();
    xlsx.utils.book_append_sheet(newWorkbook, newWorksheet, sheetName);
    xlsx.writeFile(newWorkbook, filename);
}

// Main function to update the Excel file
async function updateExcelFile() {
    process.on('SIGINT', () => {
        console.log('Interrupted, saving data to Excel file...');
        saveToExcel(data, `telematics_data_with_specs_interrupted.xlsx`);
        process.exit();
    });

    for (let i = 0; i < data.length; i++) {
        if (data[i].location.toLowerCase() !== locationToScrape.toLowerCase()) {
            continue;
        }

        // Skip rows that already have Specs data
        console.log(data[i].Specs);
        if (data[i].Specs) {
            continue;
        }

        const { productLink } = data[i];
        console.log(`Extracting data for: ${productLink}`);

        // Add a random delay between 1 and 3 seconds
        // await delay(Math.floor(Math.random() * 2000) + 1000);

        const { specs } = await extractProductInfo(productLink);

        // Log the extracted information
        console.log(`Specs: ${specs}`);
        
        data[i]['Specs'] = specs;
    }

    // Save updated data to Excel file
    saveToExcel(data, `telematics_data_with_specs_interrupted.xlsx`);
    console.log('Excel file updated successfully!');
}

// Run the script
updateExcelFile().catch(error => {
    console.error('Error updating Excel file:', error);
});
