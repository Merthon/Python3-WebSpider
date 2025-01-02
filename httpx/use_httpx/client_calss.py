#client对象
import httpx
with httpx.Client() as client:
    response = client.get('https://www.httpbin.org/get')
    print(response)