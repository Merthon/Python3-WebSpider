# 抓取网页
import requests
import re
url = "https://ssr1.scrape.center/"
r = requests.get(url)
pattern = re.compile('<h2.*?>(.*?)</h2>', re.S) # 匹配所有<h2>标签里面的内容
titles = re.findall(pattern, r.text)
print(titles)
