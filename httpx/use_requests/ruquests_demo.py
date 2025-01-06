# 爬取豆瓣
import requests
from bs4 import BeautifulSoup


# 发送请求
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
for start_num in range(0,250,25):
    response = requests.get(f"https://movie.douban.com/top250?start={start_num}",headers=headers)
    html = response.text
    soup =BeautifulSoup(html, "html.parser")
# 解析数据
    all_titles = soup.find_all("span",attrs={"class":"title"})
    for title in all_titles:
        title_string = title.string
        if "/" not in title_string:
           print(title_string)


#print(response.status_code) 
# <Response [418]> 我们可以定义请求头来绕过418错误

