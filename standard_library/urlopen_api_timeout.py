# urlopen的API
# urllib.request.urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, *, cafile=None, capath=None, cadefault=False, context=None)
# 2. timeout参数
# timeout参数指定了请求的超时时间，单位为秒。
# 如果请求超出了指定时间，则会抛出socket.timeout异常。
# 默认情况下，timeout参数的值为socket._GLOBAL_DEFAULT_TIMEOUT，
# 它表示系统默认的超时时间。
# import urllib.request
# response = urllib.request.urlopen('https://www.httpbin.org/get', timeout=0.1)
#print(response.read())
# output: urllib.error.URLError: <urlopen error _ssl.c:989: The handshake operation timed out>

# 加入异常
import socket
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('https://www.httpbin.org/get', timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('Timeout')
        
# output: Timeout


