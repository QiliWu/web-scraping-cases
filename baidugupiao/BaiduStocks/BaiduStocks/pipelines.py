# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaidustocksPipeline(object):
    def process_item(self, item, spider):
        return item

class BaidustocksInfoPipeline(object):
    def open_spider(self, spider):
        self.f = open('BaiduStockInfo.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        try:
            line = str(dict(item)) + '\n'    #需要将item类元素先转成字典，再转成字符串
            self.f.write(line)
        except:
            pass
        return item

    def close_spider(self, spider):
        self.f.close()