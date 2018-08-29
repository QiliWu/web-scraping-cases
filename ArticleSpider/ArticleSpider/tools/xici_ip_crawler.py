import requests
from fake_useragent import UserAgent
import MySQLdb
from scrapy.selector import Selector
import random
import time

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', password='qiliwu2017', database='jobbole_spider')
cursor = conn.cursor()
ua = UserAgent()

def get_html(url):
    user_agent = ua.random
    print(user_agent)
    try:
        r = requests.get(url, headers={'User-Agent': user_agent})
        r.raise_for_status()
        if r.status_code >= 200 and r.status_code < 300:
            return r
        else:
            return None
    except Exception as e:
        print(e)
        return None

base_url = 'http://www.xicidaili.com/nn/{0}'



def parse_html(response):
    selector = Selector(response=response)
    tr_list = selector.css('#ip_list tr')
    for tr in tr_list[1:]:
        td = tr.css('td')
        ip = td[1].css('::text').extract()[0]
        port = td[2].css('::text').extract()[0]
        ip_type = td[5].css('::text').extract()[0]
        speed = float(td[6].css('div::attr(title)').extract()[0].split('秒')[0])
        insert_sql ="""
            INSERT INTO ip_proxy(ip, port, ip_type, speed) VALUES(%s,%s,%s,%s)
            """
        cursor.execute(insert_sql,(ip, port, ip_type, speed))
        conn.commit()



if __name__ == '__main__':
    base_url = 'http://www.xicidaili.com/nn/{0}'
    for i in range(1, 100):
        url = base_url.format(i)
        r = get_html(url)
        if r:
            parse_html(r)
            print('成功抓取第{0}页'.format(i))
            time.sleep(random.random())
        else:
            pass
    print('finished')
    conn.close()


