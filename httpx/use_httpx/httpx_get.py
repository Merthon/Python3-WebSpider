# httpx和requests有很多的相似之处
import httpx
response = httpx.get('https://www.httpbin.org/get')
print(response.status_code) # 状态码
print(response.headers) #响应头
print(response.text) # 响应体