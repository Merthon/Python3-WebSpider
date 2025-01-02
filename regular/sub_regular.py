# 修改文本借助sub方法
import re

content = '54nk54op42pb5m8'
content = re.sub('\d+','',content)
# \d+ 匹配至少一个数字
print(content)  # nkoppbm

