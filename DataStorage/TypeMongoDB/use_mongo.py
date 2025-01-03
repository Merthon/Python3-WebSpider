# 使用MongoDB存储数据
import pymongo

# 连接MongoDB数据库
client = pymongo.MongoClient('localhost', 27017)

# 连接数据库
db = client['test']

# 连接集合
collection = db['students']

# 插入数据
student = {
    'id': '2010222',
    'name': 'Alice',
    'age': 20,
    'gender': 'male'
}

# 插入数据
result = collection.insert_one(student)
print(result)
print(result.inserted_id)