# 一般会用//开头的XPath规则，来选取所有符合要求的节点
from lxml import etree
html = etree.parse('PageData/use_XPath/test.html', etree.HTMLParser())
result = html.xpath('//*')
print(result)