import requests

proxy = 'http://127.0.0.1:1080'
proxies = {
    'http': proxy,
    'https': proxy
}
try:
    response = requests.get('http://www.baidu.com', proxies=proxies)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(e)