from urllib.error import URLError
from urllib.request import ProxyHandler,build_opener

'''
export https_proxy=http://127.0.0.1:7897 
http_proxy=http://127.0.0.1:7897 
all_proxy=socks5://127.0.0.1:7897
'''
proxy = '127.0.0.1:7897'
ProxyHandler = ProxyHandler({
    'http': 'http://' + proxy,
    'https': 'http://' + proxy
})
opener = build_opener(ProxyHandler)
try:
    response = opener.open('https://www.httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)