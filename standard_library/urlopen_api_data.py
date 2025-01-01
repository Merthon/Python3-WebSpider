# urlopen的API
# urllib.request.urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, *, cafile=None, capath=None, cadefault=False, context=None)

# 1.data参数
'''
不选择data参数，则发送GET请求；
该参数可以发送POST请求的数据。
如果data参数是bytes类型，则发送POST请求；
如果data参数是字典类型，则发送POST请求，并将字典中的键值对作为POST请求的表单数据。
'''
import urllib.parse # 用于url编码
import urllib.request # 用于发送请求
data = bytes(urllib.parse.urlencode({'name': 'zhangsan' }), encoding='utf-8')
# data = {'name': 'zhangsan'} # 字典类型
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read().decode('utf-8'))