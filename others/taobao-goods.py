import re
import requests
import time

def getHTMLtext(url):
    headers ={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
    try:
        r = requests.get(url, headers = headers, timeout=120)   #一定要设置timeout，否则爬下的html为空
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        #print(r.text)
        return r.text
    except:
        return ''

def parseHTML(ils, html):
    price_ls = re.findall(r'"view_price":"[\d.]*"', html)  #(\d+).(\d*)这样会把价格在小数点左右分为2个数字
    name_ls = re.findall(r'"raw_title":".*?"', html)
    print(price_ls)
    print(name_ls)
    for i in range(len(price_ls)):
        price = eval(price_ls[i].split(':')[1])    #eval用于去掉字符两端的双引号
        name = eval(name_ls[i].split(':')[1])
        ils.append([price, name])
    #print(ils)

    return ils

def printGoodsList(ils):
    template = "{:4}\t{:6}\t{:10}"
    print(template.format('序号', '价格', '商品名称'))
    count = 0
    for i in ils:
        count = count + 1
        print(template.format(count, i[0], i[1]))

def main():
    goods = '书包'
    depth = 3
    start_url = 'https://s.taobao.com/search?q=' + goods
    infolist = []
    for i in range(depth):
        try:
            url = start_url+'&s='+str(44*i)
            html = getHTMLtext(url)
            infolist = parseHTML(infolist, html)
            time.sleep(10)

        except:
            return ''
    #print(infolist)
    printGoodsList(infolist)

main()