# 为某个task对象绑定一个回调函数，
# 当task执行完毕时，自动调用回调函数。

import asyncio
import requests

async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status

def  callback(task):
    print('Status:',task.result())

coroutine = request()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)
print('Task:',task)

loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task:',task)