# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class ZhihuLivePipeline(object):
    def process_item(self, item, spider):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='wuqili2017', db='mysql', charset='utf8')
        self.cur = self.conn.cursor()
        self.cur.execute('USE zhihu')

        insert_sql = "INSERT INTO zhihu (title, lecturer, link, label, live_class) VALUES ({}, {}, {}, {}, {})".format(
            item['title'], item['lecturer'], item['link'], item['label'], item['live_class'])
        self.cur.execute(insert_sql)
        self.cur.connection.commit()
        self.conn.close()
        return item


