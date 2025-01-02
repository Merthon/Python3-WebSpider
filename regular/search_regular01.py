# search方法，会依次以每个字符作为开头扫描字符串
import re
html = '''
<div id="songs-list">
    <h2 class="title">经典老歌</h2>
    <p class="introduction">
    经典老歌列表
    </p>
    <ul id = "song-list" class="list-group">
        <li data-view="2">一路上有你</li>
        <li data-view="7">
            <a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
        </li>
        <li data-view="4" class="active">
            <a href="/3.mp3" singer="齐秦">往事随风</a>
        </li>
        <li data-view="6"><a href="/4.mp3" singer="张惠妹">红豆</a></li>
        <li data-view="5"><a href="/5.mp3" singer="王菲">菊次郎的夏天</a></li>
        <li data-view="5">
            <a href="/6.mp3" singer="陈慧琳">记事本</a>
        </li>
    </ul>
    </div>
'''
result = re.search('li.*?active.*?singer="(.*?)">(.*?)</a>', html, re.S)
if result:
    print(result.group(1))
    print(result.group(2)) 
