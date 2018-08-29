# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Huxiu2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    link = scrapy.Field()  # 链接
    author = scrapy.Field()  # 作者
    introduction = scrapy.Field()  # 简介
    time = scrapy.Field()  # 时间
