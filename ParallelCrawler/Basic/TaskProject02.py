# 直接调用asyncio的ensure_future方法来创建任务，
# 不需要自己创建loop，直接使用默认的loop。
# 返回的也是task对象，可以调用task.cancel()方法取消任务。

import asyncio

async def execute(x):
    print('Number:',x)
    return x

coroutine = execute(1)
print("Coroutine:", coroutine)
print('After calling execute')

task = asyncio.ensure_future(coroutine)
print("Task:", task)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print("Task:", task)
print('After running task')