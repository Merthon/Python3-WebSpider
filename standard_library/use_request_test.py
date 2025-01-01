# 传入多个参数尝试构建Request类
from urllib import request,parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'host': 'www.httpbin.org'
}
dict = {'name' : 'merthon'}
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, headers=headers, data=data)
response = request.urlopen(req)
print(response.read().decode('utf-8'))