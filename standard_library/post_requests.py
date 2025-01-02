# requests实现POST请求
import requests

data = {'name': 'chenx', 'age': 25}
r = requests.post('http://httpbin.org/post', data=data)
print(r.text)