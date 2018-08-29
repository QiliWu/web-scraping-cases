# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class DoubanPipeline(object):
    def __init__(self):
        self.client= pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['scrapy']
        self.collection = self.db['douban_movie_2']


    def process_item(self, item, spider):
        print(spider.name, 'pipelines')
        movie = dict(item)
        self.collection.insert(movie)
        return item
