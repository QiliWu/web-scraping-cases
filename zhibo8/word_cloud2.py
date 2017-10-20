#encoding='utf-8'
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt



def pinlun_cloud(name):
    f =open(r'D:\03-CS\web scraping cases\zhibo8\\'+name+'.txt', 'r', encoding='utf-8')
    text = f.read()
    parsed_text = ' '.join(jieba.cut(text))
    word_cloud = WordCloud(font_path=r'D:\03-CS\web scraping cases\zhibo8\simsun.ttf', background_color='black')
    word_cloud.generate(parsed_text)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

#pinlun_cloud('shuhao')
pinlun_cloud('hayward')