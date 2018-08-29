import requests
from scrapy.selector import Selector
import json
import MySQLdb


class StoreIP(object):
    conn = MySQLdb.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='qiliwu2017',
        database='jobbole_spider')
    cursor = conn.cursor()

    def get_ip_from_api(self, api_url):
        r = requests.get(api_url)
        data = json.loads(r.text)
        for proxy in data['msg']:
            port = proxy['port']
            ip = proxy['ip']
            proxy_ip = ip + ':' + port
            print(proxy_ip)
            self.cursor.execute(
                'INSERT INTO mogu_ip(proxy_ip) VALUES (%s)', (proxy_ip,))
            self.conn.commit()
        self.conn.close()
        return ('插入数据库成功')


class GetIP(object):
    conn = MySQLdb.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='qiliwu2017',
        database='jobbole_spider')
    cursor = conn.cursor()

    def check_ip(self, proxy_dict):
        # 判断ip是否可用
        http_url = 'http://www.ip.cn/'
        try:

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
            response = requests.get(
                http_url, headers=headers, proxies=proxy_dict)
            response.raise_for_status()
            code = response.status_code
            if code >= 200 and code < 300:
                selector = Selector(response=response)
                ip = selector.css('#result .well p code::text').extract()[0]
                if ip in proxy_dict['http'] or ip in proxy_dict['https']:
                    return True
                else:
                    return False
            else:
                return False
        except BaseException:
            return False

    def get_random_valid_ip(self):
        # 从数据库提取一个有效的ip
        self.cursor.execute(
            'SELECT id, proxy_ip FROM mogu_ip ORDER BY rand() LIMIT 1')
        for ip_info in self.cursor.fetchall():
            id = ip_info[0]
            proxy_ip = ip_info[1]
            proxy_dict_http = {'http': 'http://' + proxy_ip}
            proxy_dict_https = {'https': 'https://' + proxy_ip}
            if self.check_ip(proxy_dict_http):
                return ('http', proxy_dict_http['http'])
            elif self.check_ip(proxy_dict_https):
                return ('https', proxy_dict_http['https'])
            else:
                self.cursor.execute(
                    'DELETE FROM mogu_ip WHERE id= {0}'.format(id))
                self.conn.commit()
                return self.get_random_valid_ip()


# api_url = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=7e5d4716e4c445adadd33397bb47aa21&count=10&expiryDate=5&format=1'
# store_ip = StoreIP()
# print(store_ip.get_ip_from_api(api_url))

# api里面的ip一会就失效了。
get_ip = GetIP()
print(get_ip.get_random_valid_ip())
# 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=7e5d4716e4c445adadd33397bb47aa21&count=10&expiryDate=5&format=1'
