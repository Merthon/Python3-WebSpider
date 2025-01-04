import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(devtools=True)
    page = await browser.newPage()
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    await page.goto('https://antispider1.scrape.center/')
    await asyncio.sleep(100)

asyncio.get_event_loop().run_until_complete(main())