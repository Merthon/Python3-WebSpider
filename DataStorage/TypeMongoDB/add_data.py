import pymongo

# 连接MongoDB数据库
client = pymongo.MongoClient('mongodb://admin:admin@localhost:27017/')

# 连接数据库
db = client['test']

# 连接集合
collection = db['students']

# 插入数据
student1 = {
    'id': '2010222',
    'name': 'Alice',
    'age': 20,
    'gender': 'male'
}
student = {
    'id': '2010221',
    'name': 'mike',
    'age': 32,
    'gender': 'male'
}
# 插入数据
result = collection.insert_many([student1, student])

# 打印插入结果
print(result)
print(result.inserted_ids)

