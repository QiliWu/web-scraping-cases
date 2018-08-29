import requests
from scrapy.selector import Selector
import json

api_url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=6c87747f15594af08c7e7201e2e0c757&count=20&expiryDate=0&format=1'
r = requests.get(api_url)
data = json.loads(r.text)
for proxy in data['msg']:
    port = proxy['port']
    ip = proxy['ip']

    http_url = 'http://www.ip.cn/'  # 'https://www.baidu.com' #
    try:
        proxy_dict = {'http': 'http://' + ip + ':' + port,
                      'https': 'https://' + ip + ':' + port}
        print(proxy_dict)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        response = requests.get(http_url, headers=headers, proxies=proxy_dict)
        response.raise_for_status()
        code = response.status_code
        if code >= 200 and code < 300:
            selector = Selector(response=response)
            ip = selector.css('#result .well p code::text').extract()[0]
            print('请求ip地址：{0}'.format(ip))

        else:
            print('请求百度失败{0}，不可用！'.format(code))

    except Exception as e:
        print(e)
