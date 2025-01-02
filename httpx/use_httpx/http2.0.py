# 使用httpx库发送http2.0请求

import httpx
client = httpx.Client(http2=True)  # 开启http2.0支持
response = client.get('https://spa16.scrape.center/')
print(response.text)
print(response.http_version)  # 打印http版本