import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr.findAll('td')   ##需要用findAll， 而不是find_all 或者tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string])
    return(ulist)

def printUnivList(ulist, num):
    # 创建一个模板，将所有的字段宽度都定义为10， {4}表示当输入字符宽度不够时，使用第四个元素进行填充。第四个元素是12288
    template = "{0:^10}\t{1:{4}^10}\t{2:{4}^10}\t{3:^10}"
    print(template.format("排名", '学校名称','地理位置','评分', chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(template.format(u[0], u[1], u[2], u[3], chr(12288)))

def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    html = getHTMLText(url)
    ulist = fillUnivList(uinfo, html)
    printUnivList(ulist, 20)

main()

