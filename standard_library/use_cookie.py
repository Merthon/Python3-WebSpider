# 获取cookie
import http.cookiejar,urllib.request

# 声明一个CookieJar对象实例来保存cookie
cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
# 打印cookie信息
for item in cookie:
    print(item.name + "=" + item.value)
"""
输出:BAIDUID=AE617009356AB7133DCD971582697209:FG=1
BIDUPSID=AE617009356AB713C37BA32AE3CD76F1
PSTM=1735742159
BDSVRTM=0
BD_HOME=1
"""