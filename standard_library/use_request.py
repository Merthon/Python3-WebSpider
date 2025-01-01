# urlopen可以发起最基本的HTTP请求，返回一个HTTPResponse对象。
# 如果需要往请求中加入HTTP头部信息，可以使用Request对象。
import urllib.request
import ssl

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context
request = urllib.request.Request('https://www.python.org')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))

# 查看request类的参数
#class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
# url: 请求的URL地址(必传参数)
# data: 请求的数据，可以是bytes类型的数据，也可以是包含表单数据的字典类型数据。
# headers: 请求的HTTP头部信息，字典类型。
# origin_req_host: 原始请求的主机名，默认为空。
# unverifiable: 是否可以验证SSL证书，默认False。
# method: 请求的方法，默认为空，表示GET请求。

