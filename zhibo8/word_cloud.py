#encoding='utf-8'
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy


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


#pinlun_cloud('shuhao')
pinlun_cloud('hayward')