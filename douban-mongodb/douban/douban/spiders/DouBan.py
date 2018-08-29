# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
import re
from douban.items import DoubanItem
import time

class DoubanSpider(scrapy.Spider):
    name = 'DouBan'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

    def start_requests(self):
        #url在浏览器中打开直接是个json文件，里面包含我们需要的各种信息
        url = "https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20"
        yield Request(url, headers=self.headers)

    def parse(self, response):
        #response.body是bytes格式,使用json.loads对其进行解码，此处datas是列表格式
        datas = json.loads(response.body)
        item = DoubanItem()
        #print(datas)
        #datas的列表里包含了很多字典，字典中的键值对就是我们需要爬取的内容
        if datas:
            for data in datas:
                #item['_id'] = data['id']
                item['ranking'] = data['rank']
                item['movie_name'] = data['title']
                item['types'] = data['types']
                item['regions'] = data['regions']
                item['release_date'] = data['release_date']
                item['actors'] = data['actors']
                item['score'] = data['score']
                item['vote_count'] = data['vote_count']
                item['url'] = data['url']
                print(type(item))
                yield item



            start_num = re.search(r'start=(\d+)', response.url).group(1)
            next_page = re.sub(r'start=(\d+)','start='+str(int(start_num)+20), response.url)
            yield Request(next_page, headers=self.headers)