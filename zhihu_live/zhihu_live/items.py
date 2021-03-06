# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuLiveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    lecturer = scrapy.Field()
    link = scrapy.Field()
    label = scrapy.Field()
    live_class = scrapy.Field()
    introduce = scrapy.Field()
    comm_nums = scrapy.Field()
    lect_time = scrapy.Field()


