# 查询数据
import pymongo

# 连接MongoDB数据库
client = pymongo.MongoClient('mongodb://admin:admin@localhost:27017/')

# 连接数据库
db = client['test']

# 连接集合
collection = db['students']

# 查询单个数据 
# result = collection.find_one({'name': 'mike'})
# 查询多个数据
results = collection.find({'age': 20})
# 打印查询结果
print(results)
for result in results:
    print(result)
