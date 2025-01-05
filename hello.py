from selenium import webdriver
from time import sleep

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
sleep(2)
browser.close()