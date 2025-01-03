# 实例Ajax数据
import requests
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'

# 爬取
def scrape_api(url):
    logging.info('scraping %s', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        # 解析响应内容将其转化为JSON字符串
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)
# 爬取列表页的方法
LIMIT = 10

def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)

# 爬取详情页的方法
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'
def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)
# 保存到数据库
MONGO_COLLECTION_STRING = 'mongodb://admin:admin@localhost:27017/'
MONGO_DB = 'test'
MONGO_COLLECTION = 'movies'

import pymongo

client = pymongo.MongoClient(MONGO_COLLECTION_STRING)
db = client['test']
collection = db['movies']

# 保存数据的方法
def save_data(data):
    collection.update_one({
        'name': data.get('name'),
    },{
        '$set':data
    },
    upsert=True)


# 主函数
TOTAL_PAGE = 10
def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail data: %s', detail_data)
            save_data(detail_data)
            logging.info('data saved successfully')

if __name__ == '__main__':
    main()
