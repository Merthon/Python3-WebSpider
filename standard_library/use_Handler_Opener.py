# Handler 和 Opener两个类的使用
# 案例： 弹出认证窗口，爬虫如何请求这样的页面
# 答案：使用BaseHandler中的HTTPBasicAuthHandler类，可以实现HTTP基本认证。
# 具体步骤如下：
from urllib.request import build_opener, HTTPBasicAuthHandler,HTTPPasswordMgrWithDefaultRealm
from urllib.error import HTTPError
import ssl

# 忽略SSL证书验证

username = 'admin'
password = 'admin'
url = 'https://ssr3.scrape.center/'

# 构建密码管理对象
p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)

# 构建认证处理器
auth_handler = HTTPBasicAuthHandler(p)

# 构建opener
opener = build_opener(auth_handler)

# 发送请求
try:
    response = opener.open(url)
    html = response.read().decode('utf-8')
    print(html)
except HTTPError as e:
    print(e.reason)

