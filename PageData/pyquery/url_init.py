# URL初始化
from pyquery import PyQuery as pq
doc = pq(url='https://cuiqingcai.com')
print(doc('title')) 
#<title>静觅丨崔庆才的个人站点 - Python爬虫教程</title>
