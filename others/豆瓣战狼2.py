import requests
import re
import pandas as pd

url_first = 'https://movie.douban.com/subject/26363254/comments?start=0'
head = {'User_Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
#cookies有何没有都可以
cookies={'cookie':'bid=2rRyqjlQwz0; gr_user_id=6b7b4f47-3ca9-4830-9278-bdf764931618; viewed="3117898_25910544"; _vwo_uuid_v2=9C631032C54C86BEC4DC6662A6A7032B|18a7a8d77d23ea1db53ec5334aa74015; ap=1; __utma=30149280.1639729133.1483744381.1499663886.1503544361.4; __utmc=30149280; __utmz=30149280.1499663886.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=223695111.686243379.1503544361.1503544361.1503544361.1; __utmc=223695111; __utmz=223695111.1503544361.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf6=f326ee7b5d331c5c.1503544361.1.1503546082.1503544361.'}
html= requests.get(url_first,headers=head,cookies=cookies)
#print (html.text)
reg = re.compile(r'<a href="(.*?)&amp;.*?class="next">')
#我自己写的正则表达式运行不出来
#ren = re.compile(r'<span class="votes">(.*?)</span>.*?<span class="comment-info">(.*?)</a>.*?</span>.*?<span class="comment-time " title="(.*?)"</span>.*?class="">(.*?)\n',re.S)
#这个是照搬人家的。
ren = re.compile(r'<span class="votes">(.*?)</span>.*?comment">(.*?)</a>.*?</span>.*?<span.*?class="">(.*?)</a>.*?<span>.*?title="(.*?)"></span>.*?title="(.*?)">.*?class="">(.*?)\n',re.S)

while html.status_code == 200:
    #print(re.findall(reg,html.text))
    url_next='https://movie.douban.com/subject/26363254/comments'+re.findall(reg,html.text)[0]
    #print(url_next)
    zhanlang=re.findall(ren,html.text)
    #print(zhanlang)
    data=pd.DataFrame(zhanlang)
    print(data)
    data.to_csv('C:\\Users\\1\\Desktop\\zhanlangpinglun3.csv',header=False,index=False,mode='a+') #'a+'是追加模式
    data=[]
    zhanlang=[]
    html=requests.get(url_next,headers=head,cookies=cookies)
                 
