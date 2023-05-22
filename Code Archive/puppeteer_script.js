// Puppeteer script (puppeteer_script.js)
const fs = require('fs');
const puppeteer = require('puppeteer');
const path = require('path');

const takeScreenshots = async (urls) => {
  const screenshotPaths = [];
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium-browser',
    headless: false
  });

  for (let i = 0; i < urls.length; i++) {
    const page = await browser.newPage();
    await page.goto(urls[i]);
    const screenshotPath = path.join('/home/goldyosv7/GoldyChat/WebScreenshots', `screenshot_${i}.png`);  
    await page.screenshot({ path: screenshotPath });
    screenshotPaths.push(screenshotPath);
    console.log(`Saved screenshot for ${urls[i]} at: ${path.resolve(screenshotPath)}`);
  }

  // Write the screenshot paths to a file
  const screenshotPathsFile = path.join('/home/goldyosv7/GoldyChat/WebScreenshots', 'screenshot_paths.txt');
  fs.writeFileSync(screenshotPathsFile, screenshotPaths.join('\n'));
  console.log(`Screenshot paths written to ${path.resolve(screenshotPathsFile)}`);
  // The browser will stay open after the script finishes
  console.log('puppeteer_script.js execution completed.');
};

(async () => {
  const urls = process.argv.slice(2);
  if (urls.length < 1) {
    console.log('Please specify URLs as arguments.')
  } else {
    await takeScreenshots(urls);
  }
})();