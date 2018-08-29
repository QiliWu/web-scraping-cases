# -*- coding: utf-8 -*-
import scrapy
from huxiu.items import HuxiuItem


class HuxiuSpider(scrapy.Spider):
    name = 'HuXiu'
    allowed_domains = ['huxiu.com']
    start_urls = ['http://huxiu.com/']

    def parse(self, response):
        for s in response.xpath('//div[@class = "mod-info-flow"]/div/div[@class = "mob-ctt"]'):
            item = HuxiuItem()
            item['title'] = s.xpath('h2/a/text()')[0].extract()
            item['link'] = s.xpath('h2/a/@href')[0].extract()
            url = response.urljoin(item['link'])  #在链接前添加主域名
            item['author'] = s.xpath('div[@class = "mob-author"]/a/span/text()')[0].extract()   #默认爬第一个div,所以class属性也可不写
            item['introduction'] = s.xpath('div[@class = "mob-sub"]/text()')[0].extract()    #或者div[2]/text()
            item['time'] = s.xpath('div[@class = "mob-author"]/span/text()')[0].extract()
            print(item)
