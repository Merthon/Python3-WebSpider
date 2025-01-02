# 将字符串编译成正则表达式对象 compile()
import re 

content1 = '2019-12-23 12:00'
content2 = '2019-12-1 12:55'
content3 = '2019-12-1 13:14'
pattern = re.compile('\d{2}:\d{2}')
result1 = re.sub(pattern,'',content1)
result2 = re.sub(pattern,'',content2)
result3 = re.sub(pattern,'',content3)
print(result1,result2,result3)
# 2019-12-23  2019-12-1  2019-12-1 