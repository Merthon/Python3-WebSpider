# 定义一个协程
import asyncio

async def execute(x):
    print('Number:',x)
    # coroutine: <coroutine object execute at 0x10d4b4040>

coroutine = execute(1)
print('coroutine:', coroutine)
 # After calling execute
print('After calling execute')
 # Number: 1
loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine) #将coroutine封装乘task对象
print('After calling loop')
# After calling loop