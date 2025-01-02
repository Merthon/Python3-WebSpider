# 获取和设置cookie
import requests

# 获取cookie
response = requests.get('http://www.baidu.com')
print(response.cookies)
for key, value in response.cookies.items():
    print(key + '=' + value)