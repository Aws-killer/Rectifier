const {join} = require('path');

/**
 * @type {import("puppeteer").Configuration}
 */
module.exports = { // Changes the cache location for Puppeteer.
    cacheDirectory: join(__dirname, '.cache', 'puppeteer'),

    // Configure Puppeteer to run headless and disable the sandbox
    launch: {
        headless: true,
        executablePath: '/tmp/86c822c7-8221-4d76-8e64-09b65bca891b/.cache/puppeteer/chrome/linux-123.0.6312.105/chrome-linux64/chrome',

        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-features=SpareRendererForSitePerProcess',
            '--disable-cpu-freq-meter',
            '--disable-cpu-throttling',
        ],
        product: 'chrome'
    }
};
