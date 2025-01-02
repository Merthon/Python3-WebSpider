# 转义字符 加入反斜线\转义一下即可
import re

content = '(百度) www.baidu.com'
result = re.match('\(百度\) www\.baidu\.com', content)
print(result)
# <re.Match object; span=(0, 18), match='(百度) www.baidu.com'>