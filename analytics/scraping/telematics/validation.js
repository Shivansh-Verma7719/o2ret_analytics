const xlsx = require('xlsx');
const fs = require('fs');

async function readExcel(filePath) {
    const workbook = xlsx.readFile(filePath);
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    return xlsx.utils.sheet_to_json(sheet);
}

async function writeExcel(data, filePath) {
    const newWorkbook = xlsx.utils.book_new();
    const newSheet = xlsx.utils.json_to_sheet(data);
    xlsx.utils.book_append_sheet(newWorkbook, newSheet, 'Sheet1');
    xlsx.writeFile(newWorkbook, filePath);
}

async function findDiscrepancies(manufacturerFilePath, outputFilePath, discrepancyFilePath) {
    if (!fs.existsSync(manufacturerFilePath)) {
        console.error(`File ${manufacturerFilePath} does not exist.`);
        return;
    }
    if (!fs.existsSync(outputFilePath)) {
        console.error(`File ${outputFilePath} does not exist.`);
        return;
    }

    const manufacturers = await readExcel(manufacturerFilePath);
    const outputData = await readExcel(outputFilePath);
    const discrepancies = [];

    // Create a map for quick lookup of scraped data by manufacturer
    const scrapedDataMap = new Map();
    outputData.forEach(item => {
        const manufacturerName = item.manufacturer ? item.manufacturer.toLowerCase().trim() : null;
        if (manufacturerName) {
            if (!scrapedDataMap.has(manufacturerName)) {
                scrapedDataMap.set(manufacturerName, []);
            }
            scrapedDataMap.get(manufacturerName).push(item);
        }
    });

    // Debugging: print the scrapedDataMap contents
    console.log('Scraped Data Map:', JSON.stringify([...scrapedDataMap.entries()], null, 2));

    manufacturers.forEach(manufacturer => {
        const manufacturerName = manufacturer.Manufacturer ? manufacturer.Manufacturer.toLowerCase().trim() : null;
        if (manufacturerName) {
            const scrapedData = scrapedDataMap.get(manufacturerName) || [];
            const scrapedCount = scrapedData.length;
            const expectedCount = manufacturer['Total Models'];

            // Debugging: print the manufacturer details being processed
            console.log(`Processing Manufacturer: ${manufacturer.Manufacturer}`);
            console.log(`Scraped Count: ${scrapedCount}, Expected Count: ${expectedCount}`);

            if (scrapedCount !== expectedCount) {
                discrepancies.push({
                    Manufacturer: manufacturer.Manufacturer,
                    Scraped: scrapedCount,
                    Expected: expectedCount,
                });
            }
        }
    });

    if (discrepancies.length > 0) {
        await writeExcel(discrepancies, discrepancyFilePath);
        console.log(`Discrepancies written to ${discrepancyFilePath}`);
    } else {
        console.log('No discrepancies found.');
    }
}

const manufacturerFilePath = 'manufacturer.xlsx';
const outputFilePath = 'output.xlsx';
const discrepancyFilePath = 'discrepancy.xlsx';

findDiscrepancies(manufacturerFilePath, outputFilePath, discrepancyFilePath);
