# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    movie_name = scrapy.Field()
    ranking = scrapy.Field()
    score = scrapy.Field()
    vote_count = scrapy.Field()
    types = scrapy.Field()
    regions = scrapy.Field()
    url = scrapy.Field()
    release_date = scrapy.Field()
    actors = scrapy.Field()



