# requests库的使用
import requests

# 发送get请求
response = requests.get('https://www.baidu.com')
print(type(response))
print(response.status_code)
print(response.cookies)