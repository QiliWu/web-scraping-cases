from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

headers = {
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN, zh;q=0.8",
    "Connection":"keep-alive",
    "Host":"img.titan007.com",
    "Referer":"http://zq.win007.com/cn/CupMatch/2018/75.html",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    }

driver = webdriver.PhantomJS(executable_path=r'D:\03-CS\plantomJS\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get('http://zq.win007.com/cn/CupMatch/75.html' )
try:
    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ScoreGroupDiv"][@style="display: block;"]')))
finally:
    print(driver.page_source)
    driver.close()