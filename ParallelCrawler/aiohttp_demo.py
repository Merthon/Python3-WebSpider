# aiohttp异步爬取实战
import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s  - %(levelname)s : %(message)s')
INDEX_URL = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}/'

PAGE_SIZE = 18
PAGE_NUMBER = 100
CONCURRENCY = 5

# 爬取列表页
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s',url)
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s',url,exc_info=True)
async def scrape_index(page):
    url = INDEX_URL.format(offset=PAGE_SIZE * (page - 1))
    return  await scrape_api(url)

import json
async def main():
    global session
    session = aiohttp.ClientSession()
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
    results = await asyncio.gather(*scrape_index_tasks)
    logging.info('results %s',json.dumps(results,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())