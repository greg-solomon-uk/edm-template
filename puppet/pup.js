const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    executablePath: '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe',
  });

  const page = await browser.newPage();
  await page.goto('http://localhost:8000');

  await page.waitForSelector('.clickable-phrase, strong');

  const clickables = await page.$$('.clickable-phrase, strong');
  for (const clickable of clickables) {
    const text = await page.evaluate(el => el.textContent, clickable);
    console.log('Clicking:', text);
    await clickable.click();
    await page.waitForTimeout(500);
  }

  await browser.close();
})();