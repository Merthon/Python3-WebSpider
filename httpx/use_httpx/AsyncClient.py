# httpx 支持异步客户端请求（AsyncClient）
# 支持Python的async请求模式
import httpx
import asyncio
async def fetch(url):
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url)
        return response.text
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(fetch('https://www.httpbin.org/get'))
    