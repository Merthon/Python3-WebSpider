from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
url = 'https://runoob.com/try/try.php?filename=jqueryi-api-droppable'
browser.get(url)

browser.switch_to.frame('iframeResult')
source = browser.find_element(By.CSS_SELECTOR,'#droppable')
target = browser.find_element(By.CSS_SELECTOR,'#droppable')
actions = ActionChains(browser)
actions.drag_and_drop(source,target)
actions.perform()