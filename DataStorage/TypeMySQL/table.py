# 创建表
import pymysql

# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='root', port=3306,db='spider')
# 创建游标
cursor = db.cursor()
# 创建表
sql = 'CREATE TABLE IF NOT EXISTS `students` ( `id` VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (`id`))'
cursor.execute(sql)
db.close()