const puppeteer = require('puppeteer');
const xlsx = require('xlsx');
const fs = require('fs');

async function readExcel(filePath) {
    const workbook = xlsx.readFile(filePath);
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    return xlsx.utils.sheet_to_json(sheet, { defval: "" });
}

async function writeExcel(data, filePath) {
    const newWorkbook = xlsx.utils.book_new();
    const newSheet = xlsx.utils.json_to_sheet(data);
    xlsx.utils.book_append_sheet(newWorkbook, newSheet, 'Sheet1');
    xlsx.writeFile(newWorkbook, filePath);
}

async function getTotalUnitsSold(link) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
    await page.setExtraHTTPHeaders({
        'Referer': link,
        'Accept-Language': 'en-US,en;q=0.9',
    });

    await page.setRequestInterception(true);
    page.on('request', (request) => {
        if (['image', 'stylesheet', 'font', 'media'].includes(request.resourceType())) {
            request.abort();
        } else {
            request.continue();
        }
    });

    try {
        await page.goto(link, { waitUntil: 'networkidle2' });

        const totalUnitsSold = await page.$eval(
            'body > div.container > div.block.block-text.hw_device > div.block-content > div > div.col-md-4.col-sm-5.col-sm-offset-3.col-md-offset-0 > div > div > div > div.row.mh-45 > div.col-xs-4 > div.green.number',
            el => el.innerText.trim()
        );

        await browser.close();
        return totalUnitsSold;
    } catch (error) {
        console.error(`Error fetching sold from ${link}: ${error.message}`);
        await browser.close();
        return null;
    }
}

async function updateUnitsSold(outputFilePath, output2FilePath) {
    if (!fs.existsSync(outputFilePath)) {
        console.error(`File ${outputFilePath} does not exist.`);
        return;
    }

    const data = await readExcel(outputFilePath);
    for (const item of data) {
        if (item.Link) {
            console.log(`Fetching sold for ${item['Product Name']}...`);
            const totalUnitsSold = await getTotalUnitsSold(item.Link);
            if (totalUnitsSold !== null) {
                item['sold'] = totalUnitsSold;
                console.log(`sold for ${item['Product Name']}: ${totalUnitsSold}`);
            } else {
                item['sold'] = 'Error';
                console.log(`Failed to fetch sold for ${item['Product Name']}`);
            }
        } else {
            item['sold'] = 'No Link';
        }
    }

    await writeExcel(data, output2FilePath);
    console.log(`Updated data written to ${output2FilePath}`);
}

const outputFilePath = 'output.xlsx';
const output2FilePath = 'output2.xlsx';

updateUnitsSold(outputFilePath, output2FilePath);
