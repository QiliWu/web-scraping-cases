# -*- coding: utf-8 -*-
import scrapy
from quote.items import QuoteItem   #没有用到这个，为什么
import json

class SpiderquoteSpider(scrapy.Spider):
    name = 'spiderquote'
    quotes_base_url = 'http://spidyquotes.herokuapp.com/api/quotes?page=%s'
    start_urls = [quotes_base_url % 1]

    def parse(self, response):
        data = json.loads(response.body)
        item = QuoteItem()
        for i in data.get('quotes', []):
            item['text'] = i.get('text')
            item['author'] = i.get('author', {}).get('name')
            item['tags'] = i.get('tags')
            print(item)

        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(self.quotes_base_url % next_page)
