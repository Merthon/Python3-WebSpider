import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s  - %(levelname)s : %(message)s')

INDEX_URL = 'https://spa2.scrape.center/page/{page}'
TIMEOUT = 10
TOTAL_PAGE = 10
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
HEADLESS = False

from pyppeteer import launch
browser ,tab = None, None

async def init():
    global browser, tab
    browser = await launch(headless=HEADLESS, args=['--no-sandbox'f'--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}'])
    tab = await browser.newPage()
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})

# 定义一个爬取方法
from pyppeteer.errors import TimeoutError
async def scrape_page(url,selector):
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector, options={'timeout': TIMEOUT*1000})
    except TimeoutError:
        logging.error('error occurred while scraping %s',url,exc_info=True)

# 实现爬取页
async def scrape_pages(page):
    url = INDEX_URL.format(page=page)
    await scrape_page(url,'.item .name')

# 爬取电影页详情页
async def parse_index():
    return await tab.querySelectorAllEval('.item .name','nodes => nodes.map(node => node.]href)')

import asyncio
async def main():
    await init()
    try:
        tasks = []
        for page in range(1, TOTAL_PAGE+1): 
            tasks
            await scrape_pages(page)
            detail_urls = await parse_index()
            logging.info('detail_urls: %s', detail_urls)
    finally:
        await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())