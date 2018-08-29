# -*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

def url_analysis(u,h,e,s,n):
    '''
    用于分析网页，最后返回一个含有二级网址的标签列表，
    u:起始网址
    h:头部信息
    s:二级网址包含的特定字段
    n:网页页码
    '''
    url_lst=[]
    for i in range(1,n+1):
        r = requests.get(url=u+str(i)+'.shtml',headers=h)
        #print(r.text)
        r.encoding = 'urf-8'
        soup = BeautifulSoup(r.text,'html.parser')
        #print(soup.prettify())
        r2 = soup.find_all('a',href = re.compile(e))  #r2要通过遍历才能获得
        for j in r2:
            r3 = j.attrs['href']
            if r3.find('.shtml')==-1 or r3.find('413642')!=-1:
                continue
            else:
                url_lst.append(s+r3[-12:])
    #print(url_lst)
    return url_lst

def content(u,h):
    """
    爬取网页标签信息
    u:爬取的二级网址
    h:头部信息
    """
    r = requests.get(url=u,headers=h)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    pattern = '<li class="haoma3"><i class="blue bold fz18">开奖号码</i><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span><span class="blue">(.*?)</span>'
    #问题出在正则表达式
    res = re.search(pattern,r.text)
    nums = []
    for i in range(1,8):
        nums.append(res.group(i))
        nums.append(',')
        #print(nums)
    nums.append('\n')
    return nums
   


if __name__=='__main__':
    web_u = 'http://www.cwl.gov.cn/kjxx/ssq/hmhz/index_'
    web_h ={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_bddcb154f385b71c72d95dae58113e9c=1503674215,1503679458,1503682803; Hm_lpvt_bddcb154f385b71c72d95dae58113e9c=1503682803; _gscu_1878479644=03674220r4cx1s20; _gscs_1878479644=t03682803c6e4sz20|pv1; _gscbrs_1878479644=1; 21_vq=51',
            'Host': 'www.cwl.gov.cn',
            'Referer': 'http//www.cwl.gov.cn/kjxx/ssq/hmhz/index_5.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    web_e = '../../../kjxx/ssq/kjgg/'

    web_s='http://www.cwl.gov.cn/kjxx/ssq/kjgg/'
    

    f=open('C:\\Users\\1\\Desktop\\shuangseqiu.csv','w')
    f.seek(0)
    f.write('red1,red2,red3,red4,red5,red6,blue\n')

    for i in url_analysis(web_u,web_h,web_e,web_s,10):
        #print(i)
        data = content(i,web_h)
        #print(data)
        f.writelines(data)

    f.close()    


    
print('finished')
