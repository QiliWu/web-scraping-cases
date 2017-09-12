from wordcloud import WordCloud
import matplotlib.pyplot as plt

file = open(r"D:\03-CS\web scraping cases\books\THE Little Duke.txt", 'r')

text = file.read()


wordcloud = WordCloud().generate(text)   #the simplest, black background, square shape



plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()    #forgot this line first

print('finished')
