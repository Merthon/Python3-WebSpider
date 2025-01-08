from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# 同书籍不一样，新版修改了find_element(By.ID,'')
# input_first = browser.find_element(By.ID,'q')
# input_second = browser.find_element(By.CSS_SELECTOR,'#q')
# input_third = browser.find_element(By.XPATH,'//*[@id="q"]')
# print(input_first, input_second, input_third)
# lis = browser.find_elements(By.CSS_SELECTOR,'.service-bd--LdDnWwA9 li')
# print(lis)
# browser.close()
# 节点交互
input = browser.find_element(By.ID,'q')
input.send_keys('iphone')
time.sleep(1)
input.clear()
input.send_keys('iphone')
button = browser.find_element(By.CLASS_NAME,'btn-search')
button.click()
