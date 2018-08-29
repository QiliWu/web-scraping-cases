# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class Huxiu2Pipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect('huxiu.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE huxiuarticle (id INTEGER PRIMARY KEY AUTOINCREMENT, title varchar(30), link varchar(20), author varchar(20), introduction varchar(50))')
        self.conn.commit()
    def process_item(self, item, spider):
        print(spider.name, 'pipelines')
        self.cur.execute("INSERT INTO huxiuarticle (title, link, author, introduction) VALUES ('{}', '{}', '{}', '{}')".format(item['title'], item['link'], item['author'], item['introduction']))
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.conn.close()
