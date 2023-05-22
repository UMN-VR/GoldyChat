const express = require('express');
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const app = express();
let browser;
let pages = {};

app.get('/start', async (req, res) => {
    try {
        browser = await puppeteer.launch({
            executablePath: '/usr/bin/chromium-browser',
            headless: false, 
            
        });
        console.log('Browser started');
        res.send('Browser started');
    } catch (e) {
        console.error(`Failed to start browser: ${e}`);
        res.status(500).send(`Failed to start browser: ${e}`);
    }
});

app.get('/openURL', async (req, res) => {
    const page = await browser.newPage();
    await page.goto(req.query.url);
    const pageId = Date.now();
    pages[pageId] = page;
    console.log(`Opened URL: ${req.query.url}`);
    res.send({message: `Opened URL: ${req.query.url}`, pageId: pageId});
});

app.get('/takeScreenshot', async (req, res) => {
    const pageId = req.query.pageId;
    const page = pages[pageId];
    const screenshotPath = path.join('/home/goldyosv7/GoldyChat/WebScreenshots', `screenshot_${pageId}.png`);
    await page.screenshot({ path: screenshotPath });
    console.log(`Took screenshot for pageId: ${pageId}`);
    res.send({message: `Took screenshot for pageId: ${pageId}`, screenshotPath: screenshotPath});
});

app.get('/closeTab', async (req, res) => {
    const pageId = req.query.pageId;
    const page = pages[pageId];
    await page.close();
    delete pages[pageId];
    console.log(`Closed tab for pageId: ${pageId}`);
    res.send(`Closed tab for pageId: ${pageId}`);
});

app.get('/screenshot', async (req, res) => {
    const pageId = Date.now();
    const page = await browser.newPage();
    await page.goto(req.query.url);
    const screenshotPath = path.join('/home/goldyosv7/GoldyChat/WebScreenshots', `screenshot_${pageId}.png`);
    await page.screenshot({ path: screenshotPath });
    await page.close();
    console.log(`Navigated to URL: ${req.query.url}, took screenshot, and closed tab`);
    res.send(screenshotPath);
});

app.listen(3000, () => {
    console.log('Server listening on port 3000');
});
