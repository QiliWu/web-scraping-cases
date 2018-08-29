import MySQLdb
import requests
from scrapy.selector import Selector


class GetIP(object):
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', password='qiliwu2017', database='jobbole_spider')
    cursor = conn.cursor()

    def check_ip(self, proxy_url, ip_type, id):
        #判断ip是否可用
        http_url = 'http://www.ip.cn/' #'https://www.baidu.com' #
        try:
            proxy_dict = {ip_type: proxy_url}
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
            response = requests.get(http_url, headers=headers, proxies=proxy_dict)
            response.raise_for_status()
            code = response.status_code
            if code >= 200 and code < 300:
                selector = Selector(response=response)
                ip = selector.css('#result .well p code::text').extract()[0]
                print('请求ip地址：{0}'.format(ip))
                print('{0}经百度验证有效！'.format(proxy_url))
                return True
            else:
                print('{0}请求百度失败{1}，不可用！'.format(proxy_url, code))
                self.delete_ip(id)
                print('成功删除ip: {0}'.format(proxy_url))
                return False
        except Exception as e:
            print(e)
            self.delete_ip(id)
            print('成功删除第{0}个ip'.format(id))
            return False
    def delete_ip(self, id):
        self.cursor.execute('DELETE FROM ip_proxy WHERE id = %s' % id)
        self.conn.commit()

    def get_random_ip(self):
        #从数据库中提取任意一个ip
        self.cursor.execute("SELECT id, ip, port, ip_type FROM ip_proxy ORDER BY rand() LIMIT 1")
        for id, ip, port, ip_type in self.cursor.fetchall():
            ip_type = ip_type.lower()
            proxy_url = '{0}://{1}:{2}'.format(ip_type, ip, port)

            if self.check_ip(proxy_url, ip_type, id):
                return proxy_url
            else:
                return self.get_random_ip()


ip = GetIP()
print(ip.get_random_ip())

