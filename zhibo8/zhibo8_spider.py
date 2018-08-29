#encoding='utf-8'
from selenium import webdriver
from selenium.webdriver import ActionChains
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy

#爬取直播吧新闻评论，并生成词云
def get_pinglun(url, name):
    driver = webdriver.PhantomJS(executable_path=r'D:\03-CS\plantomJS\phantomjs-2.1.1-windows\bin\phantomjs')
    driver.get(url)

    loading = driver.find_element_by_xpath('//*[@id="pl_box"]/div/div[3]/div[7]')
    while loading.text != '评论已全部加载完成':
        loading.click()

    f = open(r'D:\03-CS\web scraping cases\zhibo8\\'+name+'.txt', 'w', encoding='utf-8')
    hotpl = driver.find_elements_by_xpath('//*[@id="hotdiv"]/div[@id="readfloor"]/div/div[2]/div[2]')
    hotpl_lst = []
    for i in hotpl:
        hotpl_lst.append(i.text)
        f.write(i.text+'\n')

    f.write('\n\n')
    compl = driver.find_elements_by_xpath('//*[@id="pllist"]/table/tbody/tr/td[2]/div/p')
    compl_lst = []
    for j in compl:
        compl_lst.append(j.text)
        f.write(j.text+'\n')
    print(len(hotpl_lst), len(compl_lst))
    f.close()
    driver.close()


def pinlun_cloud(name):
    f =open(r'D:\03-CS\web scraping cases\zhibo8\\'+name+'.txt', 'r', encoding='utf-8')
    text = f.read()
    parsed_text = ' '.join(jieba.cut(text))
    graph = Image.open(r'D:\03-CS\web scraping cases\zhibo8\love.jpg')
    image = numpy.array(graph)
    print(image)
    word_cloud = WordCloud(font_path=r'D:\03-CS\web scraping cases\zhibo8\simsun.ttf', background_color='white', mask=image)
    word_cloud.generate(parsed_text)
    image_color = ImageColorGenerator(image)
    word_cloud.recolor(color_func=image_color)
    plt.imshow(word_cloud, interpolation='bilinear')
   # plt.imshow(word_cloud.recolor(color_func=image_color))
    plt.axis('off')
    plt.savefig(r'D:\03-CS\web scraping cases\zhibo8\\'+name+'.png')
    plt.show()

url ='https://news.zhibo8.cc/zuqiu/2017-10-22/59ec499d63240.htm'
url2 = 'https://news.zhibo8.cc/zuqiu/2017-10-22/92551.htm'
name = 'hengda'
name2 = 'hengda2'
#get_pinglun(url=url, name=name)
#pinlun_cloud(name=name)
get_pinglun(url=url2, name=name2)
pinlun_cloud(name=name2)








