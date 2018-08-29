# -*- coding: utf-8 -*-
import scrapy
import re
#下载百度股票数据
class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        a_list = response.css('a::attr(href)').extract()
        for a in a_list:
            try:
                stock = re.findall(r'[s][hz]\d{6}', a)[0]
                stock_url = 'https://gupiao.baidu.com/stock/'+ stock + '.html'
                yield scrapy.Request(url = stock_url, callback=self.parse_stock)
            except:
                continue

    def parse_stock(self, response):
        infoDict = {}
        stock_info = response.css('.stock-info')
        name = stock_info.css('.bets-name').extract()[0]
        infoDict.update({'股票名称': re.findall('\n.*<s', name)[0].split()[0] + re.findall('s[hz]\d{6}',name)[0]})
        keys = stock_info.css('dt').extract()
        vals = stock_info.css('dd').extract()
        for i in range(len(keys)):
            #re.findall(r'>.*</dt>', keys[i])[0]返回的结果是‘>最高</dt>', 所以要去[1:-5]的切片
            key = re.findall(r'>.*</dt>', keys[i])[0][1:-5]
            try:
                value = re.findall(r'>.*</dd>', vals[i])[0][1:-5]
            except:
                value = '--'
            infoDict[key] = value
        yield infoDict

