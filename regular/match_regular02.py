# 匹配方法-match
# 从字符串提取一部分内容
import re

content = 'Hello 1234567 World_This is a Regex Demo'
result = re.match('^Hello\s(\d+)\sWorld',content)
print(result)
print(result.group()) # 输出完整匹配的字符串
print(result.group(1)) # 输出第一个括号匹配的字符串
print(result.span()) # 输出匹配的字符串的位置