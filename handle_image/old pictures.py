from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium import webdriver
import os
from PIL import Image

# 下载100张图片，并将这些图片组合成一张图片

path = os.path.dirname(os.path.abspath(__file__))
path = path+"\old pictures\\"

def download_img():
    driver = webdriver.PhantomJS(executable_path=r'D:\03-CS\plantomJS\phantomjs-2.1.1-windows\bin\phantomjs')
    driver.get('https://mp.weixin.qq.com/s/G21dhvmoQkzHjYsBJUl5aA')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.find('div', {'id':'js_content'}).findAll('img', {'data-s':'300,640'})
    #print(len(list))
    #img_list = []
    for i in list[2:len(list)-1]:
        #print(i['data-src'])
        #img_list.append(i['src'])
        #i['src']不能下载图片，只能用i['data-src']
        try:
            urlretrieve(i['data-src'], r'D:\03-CS\web scraping cases\old pictures\%s.jpg' % (list.index(i)-1))
        except Exception as e:
            print(e)
            pass
    driver.close()

def check_img():
    file_list = os.listdir(path)  #用于返回指定的文件夹包含的文件或文件夹的名字的列表
    for file in file_list:
        try:
            im = Image.open(path+file)
            print(im.format, im.size, im.mode)
        except:
            print(file)

def combine_img():
    #PIL拼图
    #所有100张图，均生成为400X400的缩略图，布局成10X10的方式，需要总画布大小为4000X4000。
    mw = 400  # 每张图的大小：长度
    ms = 10  #列数
    msize = mw * ms
    toImage = Image.new('RGB', (4000, 4000))
    for j in range(1, 11):
        for k in range(1, 11):
            try:
                fromImage = Image.open(path+'%s.jpg' % str(ms*(j-1)+k))
                fromImage = fromImage.resize((400, 400), Image.ANTIALIAS)
                toImage.paste(fromImage, ((k-1)*mw, (j-1)*mw))
                print(j,k)
            except IOError:
                pass

    toImage.show()
    toImage.save(path+'final.jpg')
    print('finished')

download_img()
check_img()
combine_img()
