# 贪婪和非贪婪匹配
# 贪婪
# import re
# content = 'Hello 123 4567 World_This is a Regex Demo'
# result = re.match('^He.*(\d+).*Demo$', content)
# print(result)
# print(result.group(1)) # 7
'''
在贪婪匹配下，.*可以匹配到尽可能多的字符，因此会匹配到整个字符串。
而在非贪婪匹配下，.*只会匹配到尽可能少的字符，写法为.*?。
'''
# 非贪婪
import re
#content = 'Hello 1234567 World_This is a Regex Demo'
# result = re.match('^He.*?(\d+).*Demo$',content)
# print(result)
# print(result.group(1))  # 1234567

# 注意：如果匹配的结果在字符串的结尾，.*?有可能会匹配不到任何字符，因此结果为空。
content = 'http://weibo.com/comment/kEraCN'
result1 = re.match('http.*?comment/(.*?)',content)
result2 = re.match('http.*?comment/(.*)',content)
print('result1:',result1.group(1))  # 
print('result2:',result2.group(1))  # kEraCN