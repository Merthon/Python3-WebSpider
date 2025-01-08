import requests, json

url = 'https://api.diffbot.com/v3/article'
params = {
    'token': '77b41f6fbb24496d5113d528306528fa',
    'url': 'https://news.ifeng.com/c/7kQcQG2peWU',
    'fields': 'meta'
}
response = requests.get(url, params=params)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))