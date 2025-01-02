# 匹配方法-match
import re
# 先声明一个字符串
content = 'Hello 123 4567 World_This is a Regex Demo'
print(len(content)) # 41
# 写正则表达式
result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}',content)
print(result) #<re.Match object; span=(0, 25), match='Hello 123 4567 World_This'>
# group()方法可以获取匹配到的字符串 
# span()方法可以获取匹配到的字符串的位置
print(result.group()) #Hello 123 4567 World_This
print(result.span()) #(0, 25)

