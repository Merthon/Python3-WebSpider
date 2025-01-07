from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# ChromeDriver 配置
chrome_driver_path = "/Users/chenx/chromedriver-mac-x64/chromedriver"  # 替换为你的 ChromeDriver 路径
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式（可选）
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU（可选）
chrome_options.add_argument("--no-sandbox")  # 避免权限问题
chrome_options.add_argument("--disable-dev-shm-usage")  # 避免内存不足问题
chrome_options.add_argument("start-maximized")  # 启动时最大化窗口
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")  # 设置 User-Agent

# 启动浏览器
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 访问目标页面
url = "https://www.zhipin.com/web/geek/job?query=python&city=101030100"
driver.get(url)

# 等待页面加载完成（推荐显式等待）
time.sleep(5)  # 简单等待页面加载完成

# 提取页面 HTML（可选）
page_source = driver.page_source
print(page_source[:500])  # 打印部分 HTML 内容，调试用

# 提取职位信息（示例）
try:
    # 查找职位卡片元素（替换为目标页面实际的 XPath 或 CSS 选择器）
    jobs = driver.find_elements(By.CSS_SELECTOR, ".job-card-wrapper")

    for job in jobs:
        # 提取信息：职位名称、公司名称、薪资等
        job_name = job.find_element(By.CSS_SELECTOR, ".job-name").text
        company_name = job.find_element(By.CSS_SELECTOR, ".company-text").text
        salary = job.find_element(By.CSS_SELECTOR, ".job-limit > span").text
        print(f"职位：{job_name}, 公司：{company_name}, 薪资：{salary}")

except Exception as e:
    print("提取数据出错:", e)

# 关闭浏览器
driver.quit()
