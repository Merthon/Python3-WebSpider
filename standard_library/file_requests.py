# 文件上传
import requests
file = {'file': open('favicon.ico', 'rb')}
response = requests.post('http://httpbin.org/post', files=file)
print(response.text)