# JSON 文件存储
import json
# 注意JSON字符串里的键值对必须用双引号，否则会报错
str = '''
[{
    "name": "张三",
    "age": 25,
    "gender": "男"
}, {
    "name":"李四",
    "age": 26,
    "gender": "男"
}]
'''
print(type(str))
data = json.loads(str)
# print(type(data))
# print(data)
print(data[0]['name'])