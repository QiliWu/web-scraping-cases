# -*- coding: utf-8 -*-
import scrapy
import json
from huxiu_2.items import Huxiu2Item
from lxml import etree

class HuxiuarticleSpider(scrapy.Spider):
    name = 'HuXiuarticle'
    def start_requests(self):
        url = 'http://www.huxiu.com/v2_action/article_list'   #这个URL很奇怪
        for i in range(1, 10):
            #FormRequest是Scrapy 发送POST请求的方法
            yield scrapy.FormRequest(
                url = url,
                formdata={"huxiu_hash_code": "b192849123c3420267da71fbfbf1f5f4", "page": str(i)},
                callback = self.parse
            )

    def parse(self, response):
        item = Huxiu2Item()
        data = json.loads(response.text)  #对str对象进行decode
        s = etree.HTML(data['data'])
        #print('sss' + '\n' + s.itertext)
        title_list = s.xpath('//a[@class="transition msubstr-row2"]/text()')
        link_list = s.xpath('//a[@class="transition msubstr-row2"]/@href')
        author_list = s.xpath('//span[@class="author-name"]/text()')
        introduction_list = s.xpath('//div[@class="mob-sub"]/text()')
        for a, b, c, d in zip(title_list, link_list, author_list, introduction_list):
            item['title'] = a
            item['link'] = b
            item['author'] = c
            item['introduction'] = d
            yield item




