import requests
from bs4 import BeautifulSoup
import traceback    #在程序里打印异常的跟踪返回
import re

def getHTMLtext(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code   #r.apparent_encoding很慢，经历避免
        return r.text
    except:
        return ''

def getStockList(lst, StockURL):
    html = getHTMLtext(StockURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    #print(a)
    for i in a:
        try:
            href = i.attrs['href']
            #print(re.findall(r'[s][zh]/d{6}', href)[0])
            lst.append(re.findall(r'[s][zh]\d{6}', href)[0])
        except:
            continue
    #print(lst)
    return lst


def getStockInfo(lst, StockURL, fpath):
    count = 0
    for stock in lst:
        url = StockURL + stock + '.html'
        html = getHTMLtext(url)
        try:
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                stock_info = soup.find('div', {'class': 'stock-info'})
                infodict = {'股票代码':stock}
                try:
                    name = stock_info.find('a', {'class': 'bets-name'})
                    infodict.update({'股票名称': name.text.split()[0]})
                    keys = stock_info.find_all('dt')
                    values = stock_info.find_all('dd')
                    for i in range(len(keys)):
                        key = keys[i].text
                        value = values[i].text.split('\n')[-1].strip()
                        infodict[key] = value
                except:
                    continue
                print(infodict)
                with open(fpath, 'a') as f:
                    f.write(str(infodict) +'\n')
                    count = count + 1
                    print('\r当前速度{:.2f}'.format(count*100/len(lst)))
                    #'\r'会让print在打印完当前行后，将光标移至改行的起始位置。下次打印又重新从这里开始，
                    #避免了print每次都换行的操作，实现了不换行动态打印。
                    #'\r'在IDE中是禁用的。需要再commend里调用
        except:
            traceback.print_exc()
            continue



def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_path = r'D:/03-CS/web scraping cases/baidugupiao/output.txt'

    slist = []
    lst = getStockList(slist, stock_list_url)
    getStockInfo(lst, stock_info_url, output_path)


main()
