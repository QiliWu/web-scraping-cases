from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import time


#chrome driver 要用2.33版的。
driver = webdriver.Chrome()
driver.get('http://zq.win007.com/cn/CupMatch/75.html')
time.sleep(5)
#print(driver.page_source)
print('*'*50)
print(driver.find_element_by_xpath('//*[@id="ScoreGroupTab"]/tbody/tr[3]/td[2]/a').get_attribute('href'))

driver.close()