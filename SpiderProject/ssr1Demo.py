# 爬虫实战
# 导入库
import requests
import logging
import re
from urllib.parse import urlparse, urljoin
import json
from os import makedirs
from os.path import exists
import multiprocessing

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: - %(message)s')
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGES = 10

# 实现一个页面爬取的函数
def scrape_page(url):
    logging.info('Scraping%s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid response code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, 
                     exc_info=True)
# 定义列表页的爬取方法  
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)

# 解析列表页，并得到每部电影的详情页的URL
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url

# 定义详情页的爬取方法
def scrape_detail(url):
    return scrape_page(url)
# 解析详情页，并得到电影的详细信息
def parse_detail(html): 
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*? class="cover">', re.S)
    name_pattern = re.compile('<h2.*?>(.*?)</h2>', re.S)
    categories_pattern = re.compile('<button.*?category.*?<span.*?>(.*?)</span>.*?</button>', re.S)
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s上映', re.S)
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else None
    published_at = re.search(published_at_pattern, html).group(1).strip() if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = re.search(score_pattern, html).group(1).strip() if re.search(score_pattern, html) else None
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }

# 保存电影信息到文件
RESULT_DIR = 'results'
exists(RESULT_DIR) or makedirs(RESULT_DIR)

def save_data(data):
    name = data.get('name')
    data_path = f'{RESULT_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False,indent=2)

# 多线程加速
# 选用多进程的里面的进程池pool，可以实现多个进程同时运行，提高爬取速度。
# main方法里添加一个参数page
# 主函数
def main():
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data%s', data)
        logging.info('saving data to json file')
        save_data(data)
        logging.info('data saved successfully')
        # logging.info('detail urls %s', list(detail_urls))

if __name__ == '__main__':
    # 多线程加速
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGES+1)
    pool.map(main, pages)
    pool.close()
    pool.join()