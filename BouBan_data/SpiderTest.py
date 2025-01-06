import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# 连接MongoDB
client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client.douban
collection = db.movies

# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# 定义爬取豆瓣电影TOP250的函数
def fetch_douban_top250():
    movies = []
    for start_num in range(0, 250, 25):  # 分页请求，每页25个电影
        print(f"正在爬取第 {start_num // 25 + 1} 页...")
        response = requests.get(f"https://movie.douban.com/top250?start={start_num}", headers=headers)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # 打印当前页面的 HTML 内容（用于调试）
        # print(soup.prettify())  # 可以取消注释查看整个 HTML 结构

        # 解析电影名字和评分
        all_titles = soup.find_all("span", attrs={"class": "title"})
        all_ratings = soup.find_all("span", class_="rating_num")
        all_actors = soup.find_all("span", class_="actor")

        # 打印每个元素的数量（检查是否成功获取数据）
        print(f"爬取到 {len(all_titles)} 部电影, 评分数量: {len(all_ratings)}, 演员数量: {len(all_actors)}")

        # 检查每个元素是否被正确提取
        for i, (title, rating, actor) in enumerate(zip(all_titles, all_ratings, all_actors)):
            movie = {}
            title_string = title.string
            if "/" not in title_string:  # 排除有多个名字的情况
                movie['title'] = title_string  # 电影名字
                movie['rating'] = rating.string  # 评分
                
                # 获取演员信息
                actors = actor.text.strip().split('/')  # 拆分演员列表
                actors = [actor.strip() for actor in actors]  # 去除多余空格
                movie['actors'] = actors

                # 打印电影信息
                print(f"爬取电影 {i+1}: {movie['title']}, 评分: {movie['rating']}, 演员: {movie['actors']}")
                
                # 将数据添加到列表
                movies.append(movie)
    
    print(f"总共爬取到 {len(movies)} 部电影")
    return movies

# 存储到 MongoDB
def save_to_mongo(movies):
    if movies:  # 检查 movies 列表是否非空
        try:
            result = collection.insert_many(movies)  # 使用 insert_many 一次插入所有电影
            print(f"成功插入 {len(result.inserted_ids)} 部电影")
        except Exception as e:
            print(f"插入数据时出错: {e}")
    else:
        print("没有可插入的数据，跳过插入操作")

# 主程序
if __name__ == '__main__':
    print("开始爬取豆瓣电影TOP250...")
    movies = fetch_douban_top250()
    save_to_mongo(movies)
    print("数据已成功存入MongoDB！")
