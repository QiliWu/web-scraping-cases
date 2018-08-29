# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
#from ArticleSpider.tools.get_ip import GetIP


class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        #super(RandomUserAgentMiddleware, self).__init__()
        mro_list = self.__class__.__mro__
        print(mro_list)

        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        random_ua = getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', random_ua)
        h = request.headers

# class ProxyIPMiddleware(object):
#     #设置动态变化的ip
#     def process_request(self, request, spider):
#         get_ip = GetIP()
#         scheme, proxy_url = get_ip.get_random_valid_ip()
#         request.meta['proxy'] = proxy_url

from selenium import webdriver
import time
from scrapy.http import HtmlResponse
class JSPageMiddleware(object):
    #通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == 'jobbloe': #并不是所有爬虫都需要使用chrome
            # browser = webdriver.Chrome()
            spider.browser.get(request.url)
            time.sleep(3)

            #返回一个HTMLResponse对象，scrapy就不会在将该url交给下载器再下载了，
            #而是直接将response返回给spider
            return HtmlResponse(
                url = spider.browser.current_url,
                body = spider.browser.page_source,
                encoding = 'utf-8',
                request = request
            )





