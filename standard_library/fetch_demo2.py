# 抓取二进制数据
import requests
r = requests.get('https://scrape.center/favicon.ico')
# print(r.text)
# print(r.content)
# 提取信息并保存
with open('favicon.ico', 'wb') as f:
    f.write(r.content)
