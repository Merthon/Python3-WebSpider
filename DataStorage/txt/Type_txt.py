# 爬取数据存储为TXT文本格式
import requests
from pyquery import PyQuery as pq
import re

url = 'https://ssr1.scrape.center/'
html = requests.get(url).text
doc = pq(html)
items = doc('.el-card').items()
file = open('movies.txt', 'w', encoding='utf-8')
for item in items:
    # 电影名称
    name = item.find('a > h2').text()
    file.write(f'名称: {name}\n')
    # 类别
    categories = [item.text() for item in item.find('.categories button span').items()]
    file.write(f'类别: {categories}\n')
    # 上映日期
    published_at = item.find('.info:contains(上映日期)').text()
    published_at = re.search(r'\d{4}-\d{2}-\d{2}', published_at).group(1) \
    if published_at and re.search(r'\d{4}-\d{2}-\d{2}', published_at) else None
    file.write(f'上映日期: {published_at}\n')
    # 评分
    score = item.find('p.score').text()
    file.write(f'评分: {score}\n')
    file.write(f'{"=" * 50}\n')
file.close()