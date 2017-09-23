
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
import csv
import time

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wuqili2017', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE scraping')

def store(title, lecturer, link, participants, live_class):
    cur.execute('INSERT INTO zhihulive (title, lecturer, link, participants, live_class) VALUES (\'%S\', \'%S\', \'%S\', \'%S\', \'%S\')', (title, lecturer, link, participants, live_class))
    cur.connection.commit()

def getInfo(url):
    driver = webdriver.PhantomJS(executable_path=r'D:\03-CS\plantomJS\phantomjs-2.1.1-windows\bin\phantomjs')
    driver.get(url)
    print('11')
    print(driver.find_element_by_tag_name('html').text)
    pageSource = driver.page_source
    soup=BeautifulSoup(pageSource, 'html.parser')
    print(soup.text)
    time.sleep(10)

    title_list = driver.find_elements_by_xpath("//div[@class='LiveItem-title-vgQH utils-textEllipsis-3FN2']")
    print('title_list')
    #print(driver.find_element_by_xpath("//div[@TopTabNavBar-root-BO2L TopTabNavBar-isLight-x6pO utils-frostedGlassEffect-2q_T TabNavBar-root-3526']").text)
    print(title_list)
    lecturer_list = driver.find_elements_by_xpath("//div[@class='LiveItem-description-1ZrY utils-textEllipsis-3FN2']")
    print('lecturer_list')
    print(lecturer_list)
    link_list = driver.find_elements_by_xpath("//a[@href='LiveItem-root-OO1E LiveItem-withMobileLayout-bLOD Card-card-102t Card-notSafari-3UQA']")
    print('link_list')
    print(link_list)
    participants_list = driver.find_elements_by_xpath("//div[@class='LiveInfo-participants-1kng']")
    live_class_list = driver.find_elements_by_xpath("//div[@class='LiveItem-tags-DFwD utils-clearfix-3oo3']/span/span")



    #html = urlopen(url)
    #print(html)
    #soup = BeautifulSoup(html, 'html.parser')
    #print(soup.text)

    #title_list = soup.findAll('div', {'class':'LiveItem-title-vgQH utils-textEllipsis-3FN2'})
    #lecturer_list = soup.findAll('div', class_='LiveItem-description-1ZrY utils-textEllipsis-3FN2')
    #link_list = soup.findAll('a', href='LiveItem-root-OO1E LiveItem-withMobileLayout-bLOD Card-card-102t Card-notSafari-3UQA')
    #participants_list = soup.findAll('div', {'class':'LiveInfo-participants-1kng'})
    #live_class_list = soup.findAll('div', {'class': 'LiveItem-tags-DFwD utils-clearfix-3oo3'})

    csvFile = open(r'D:\03-CS\web scraping cases\zhihulive.csv', 'wt')
    writer =csv.writer(csvFile)
    writer.writerow(['title', 'lecturer', 'link', 'participants', 'live_class'])

    for i,j,k,m,n in zip(title_list, lecturer_list, link_list, participants_list, live_class_list):
        print('-'*30)
        title = i.text
        lecturer = j.text
        link = k.attrs['href']
        participants = m.text
        live_class = n.text
        writer.writerow([title, lecturer, link, participants, live_class])
        store(title, lecturer, link, participants, live_class)
        print (title, lecturer, link, participants, live_class)
    csvFile.close()
    print('finished')

getInfo('https://www.zhihu.com/lives')
conn.close()
