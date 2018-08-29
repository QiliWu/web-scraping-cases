#使用selenium+chrome爬取知乎live(www.zhihu.com/lives)上live信息，并通过下拉以加载更多。

from urllib.parse import urljoin
from selenium import webdriver
import pymysql
import csv
import time

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wuqili2017', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE scraping')

def store(title, lecturer, link, participants, live_class):
    #保存至本地MYSQL数据库
    cur.execute('INSERT INTO zhihulive (title, lecturer, link, participants, live_class) VALUES (\'%S\', \'%S\', \'%S\', \'%S\', \'%S\')', (title, lecturer, link, participants, live_class))
    cur.connection.commit()

def getInfo(url):
    #知乎live页面是js加载的
    driver = webdriver.Chrome(executable_path=r'E:\01_python\web_scraping_cases\web-scraping-cases\zhihu_live\zhihu_live\chromedriver.exe')
    driver.get(url)
    title_list, lecturer_list, link_list, participants_list, live_class_list = [], [], [], [], []
    for i in range(10):
        time.sleep(5)
        title_list = driver.find_elements_by_xpath("//div[@class='LiveItem-title-vgQH utils-textEllipsis-3FN2']")
        lecturer_list = driver.find_elements_by_xpath("//div[@class='LiveItem-description-1ZrY utils-textEllipsis-3FN2']")
        link_list = driver.find_elements_by_xpath("//a[@class='LiveItem-root-OO1E LiveItem-withMobileLayout-bLOD Card-card-102t Card-notSafari-3UQA']")
        participants_list = driver.find_elements_by_xpath("//div[@class='LiveInfo-participants-1kng']")
        live_class_list = driver.find_elements_by_xpath("//div[@class='LiveItem-tags-DFwD utils-clearfix-3oo3']/span/span")
        #下拉以加载更多
        driver.execute_script(
            "window.scrollTo({0}*1*document.body.scrollHeight, {1}*1*document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;".format(
                i, i + 1))
    csvFile = open(r'zhihulive.csv', 'w', encoding='utf-8')
    try:
        writer =csv.writer(csvFile)
        writer.writerow(['title', 'lecturer', 'link', 'participants', 'live_class'])
        for i,j,k,m,n in zip(title_list, lecturer_list, link_list, participants_list, live_class_list):
            print('-'*30)
            title = i.text
            lecturer = j.text
            link = urljoin('https://www.zhihu.com/', k.get_attribute('href'))
            participants = m.text
            live_class = n.text
            writer.writerow([title, lecturer, link, participants, live_class])
            store(title, lecturer, link, participants, live_class)
            print (title, lecturer, link, participants, live_class)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
        conn.close()
    print('finished')

getInfo('https://www.zhihu.com/lives')

