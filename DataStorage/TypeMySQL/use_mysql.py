# 连接数据库，并将数据存储在数据库中
import pymysql

# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='root', port=3306)
# 创建游标
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
print('Database version:',data)

# 创建数据库
cursor.execute('CREATE DATABASE spider DEFAULT CHARACTER SET utf8mb4')
db.close()