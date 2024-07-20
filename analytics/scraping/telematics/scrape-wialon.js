const puppeteer = require('puppeteer');
const xlsx = require('xlsx');
const fs = require('fs');

async function scrapeManufacturerData(manufacturer, url, totalModels) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Set user agent and other headers to avoid detection
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
    await page.setExtraHTTPHeaders({
        'Referer': url,
        'Accept-Language': 'en-US,en;q=0.9',
    });

    // Disable loading images and stylesheets
    await page.setRequestInterception(true);
    page.on('request', (request) => {
        if (['image', 'stylesheet', 'font', 'media'].includes(request.resourceType())) {
            request.abort();
        } else {
            request.continue();
        }
    });

    let pageNum = 1;
    const results = [];

    while (pageNum <= 5) {
        const pageUrl = `${url}?page=${pageNum}`;
        console.log(`Scraping ${pageUrl}...`);

        try {
            await page.goto(pageUrl, { waitUntil: 'networkidle2' });

            const tableExists = await page.$('#w1 > table');
            if (!tableExists) {
                console.log(`No table found on page ${pageNum}. Ending scraping for ${manufacturer}.`);
                break;
            }

            const rows = await page.$$('#w1 > table tbody tr');
            console.log(`Found ${rows.length} rows on page ${pageNum}.`);

            for (const row of rows) {
                try {
                    const product = await row.$eval('td:nth-child(2) a', a => ({
                        name: a.innerText.trim(),
                        link: a.href,
                    }));
                    const totalUnits = await row.$eval('td:nth-child(3)', td => td.innerText.trim());

                    results.push({
                        product_name: product.name,
                        product_link: product.link,
                        total_units: totalUnits,
                        manufacturer: manufacturer,
                    });
                } catch (error) {
                    console.error(`Error scraping row: ${error.message}`);
                    continue;
                }
            }

            if (results.length >= totalModels) {
                console.log(`Scraped enough rows (${results.length}) for ${manufacturer}. Stopping.`);
                break;
            }
        } catch (error) {
            console.error(`Error scraping page ${pageNum} of ${manufacturer}: ${error.message}`);
            break;
        }

        pageNum++;
    }

    await browser.close();
    return results;
}

async function readExcel(filePath) {
    const workbook = xlsx.readFile(filePath);
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    return xlsx.utils.sheet_to_json(sheet);
}

async function writeExcel(data, filePath) {
    const existingData = fs.existsSync(filePath) ? await readExcel(filePath) : [];
    const combinedData = existingData.concat(data);

    const newWorkbook = xlsx.utils.book_new();
    const newSheet = xlsx.utils.json_to_sheet(combinedData);
    xlsx.utils.book_append_sheet(newWorkbook, newSheet, 'Sheet1');
    xlsx.writeFile(newWorkbook, filePath);
}

async function logDiscrepancy(manufacturer, totalScraped, totalExpected) {
    const logMessage = `Manufacturer: ${manufacturer}, Scraped: ${totalScraped}, Expected: ${totalExpected}\n`;
    fs.appendFileSync('discrepancies.txt', logMessage, 'utf8');
}

async function main() {
    const inputFilePath = 'manufacturer.xlsx';
    const outputFilePath = 'output.xlsx';

    if (!fs.existsSync(inputFilePath)) {
        console.error(`File ${inputFilePath} does not exist.`);
        return;
    }

    const manufacturers = await readExcel(inputFilePath);
    let allResults = [];
    
    // Define the last manufacturer manually
    const lastManufacturer = null; // Update this manually as needed
    let startScraping = false;

    for (const manufacturer of manufacturers) {
        if (lastManufacturer) {
            if (startScraping) {
                console.log(`Resuming scraping from manufacturer: ${manufacturer.Manufacturer}`);
            } else if (manufacturer.Manufacturer === lastManufacturer) {
                startScraping = true;
                console.log(`Starting scraping from manufacturer: ${manufacturer.Manufacturer}`);
            } else {
                console.log(`Skipping manufacturer: ${manufacturer.Manufacturer}`);
                continue;
            }
        } else {
            startScraping = true;
            console.log(`Starting scraping for manufacturer: ${manufacturer.Manufacturer}`);
        }

        const results = await scrapeManufacturerData(manufacturer.Manufacturer, manufacturer['Manufacturer Links'], manufacturer['Total Models']);
        console.log(`Scraped ${results.length} products for ${manufacturer.Manufacturer}.`);
        allResults = allResults.concat(results);

        // Check for discrepancy and log if necessary
        if (results.length !== manufacturer['Total Models']) {
            await logDiscrepancy(manufacturer.Manufacturer, results.length, manufacturer['Total Models']);
        }

        // Save progress after each manufacturer
        await writeExcel(allResults, outputFilePath);
        console.log(`Progress saved to ${outputFilePath}`);
    }

    console.log(`All data written to ${outputFilePath}`);
}

// Handle graceful shutdown and save progress
process.on('SIGINT', async () => {
    console.log('Received SIGINT. Saving progress...');
    try {
        await writeExcel(allResults, 'output.xlsx');
        console.log('Progress saved to output.xlsx');
    } catch (error) {
        console.error(`Error saving progress: ${error.message}`);
    }
    process.exit();
});

let allResults = [];
main();
