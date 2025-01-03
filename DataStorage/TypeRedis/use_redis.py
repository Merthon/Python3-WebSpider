# 连接Redis数据库
from redis import StrictRedis

# 创建Redis客户端实例
redis = StrictRedis(host='localhost', port=6379, db=0)
# 存储数据
redis.set('name', 'Bob')

# 获取数据
print(redis.get('name'))
# b'Bob'