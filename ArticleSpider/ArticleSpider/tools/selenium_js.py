import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://blog.jobbole.com/all-posts/')
time.sleep(10)
# #模拟鼠标下拉三次
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(5)

# chrome_opt = webdriver.ChromeOptions()
# prefs = {'profile.managed_default_content_settings.images': 2}  #将这个值设为2就是不加载图片了
# chrome_opt.add_experimental_option('prefs', prefs)
# browser = webdriver.Chrome(chrome_options=chrome_opt)
# browser.get('https://www.taobao.com')

