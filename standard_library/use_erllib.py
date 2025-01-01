# urllib库，可以实现URL的编码和解码，以及发送HTTP请求等。
# 我们要做的就是指定请求的URL，请求头，请求体等信息
# urllib包含4个主要模块：
# - urllib.parse：用于URL的编码和解码
# - urllib.request：用于发送HTTP请求
# - urllib.error：用于处理urllib.request模块的异常
# - urllib.robotparser：用于解析robots.txt文件

# 第一步 发送请求
# urlopen()方法可以发送HTTP请求，并返回一个HTTPResponse对象。
import ssl
import urllib.request
# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

response = urllib.request.urlopen('https://www.python.org')

#print(type(response))
# <class 'http.client.HTTPResponse'>
# print(response.read().decode('utf-8'))

print(response.status)
# 200
print(response.getheaders())
print(response.getheader('Server'))