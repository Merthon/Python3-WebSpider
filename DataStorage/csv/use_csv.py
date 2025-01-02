# 使用python的csv模块读写csv文件

import csv

# 写入csv文件
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'Alice', '20'])
    writer.writerow(['10002', 'Bob', '25'])
    writer.writerow(['10003', 'Charlie', '30'])
    writer.writerow(['10004', 'David', '35'])
