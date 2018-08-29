# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#自定义图像管道文件需要继承scrapy自带的管道文件类
from scrapy.pipelines.images import ImagesPipeline
import json
from scrapy.exporters import JsonItemExporter  #scrapy自带的json导出API
import MySQLdb
from twisted.enterprise import adbapi  #adbapi使的我们数据库的操作异步化
import MySQLdb.cursors

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        #在return这里设计一个断点，可以用来检测front_image_path是否设置成功
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = open('article.json', 'wb')  #一定要用wb

    def process_item(self, item, spider):
        #json.jumps返回的是字符串。 ensure_ascii解决中文乱码问题。
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self, spider):
        self.file.close()



class JsonExporterPipeline(object):
    #使用scrapy提供的json exporter导出json文件
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'qiliwu2017', 'jobbole_spider',
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        #将sql插入语句移至相应的item中编写，以满足不同的item定制sql语句
        # insert_sql = """
        #              insert into jobbole_article(title, create_date, url, url_object_id,
        #              fav_nums, praise_nums, comment_nums, tags, content)
        #              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        #              """
        # self.cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'],
        #                                  item['url_object_id'], item['fav_nums'],
        #                                  item['praise_nums'], item['comment_nums'],
        #                                  item['tags'], item['content']))

        #从item类中调用insert_sql, params
        insert_sql, params = item.get_insert_sql()
        self.cursor.execute(insert_sql, params)

        self.conn.commit()
        return item

    def spider_closed(self, spider):
        self.conn.close()

from twisted.enterprise import adbapi  #adbapi使的我们数据库的操作异步化
import MySQLdb.cursors

class MysqlTwistedPipeline(object):
    #通过twisted实现数据库的异步操作
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  #从settings获取参数
        dbparams = dict(
                        host=settings['MYSQL_HOST'],
                        user = settings['MYSQL_USER'],
                        password = settings['MYSQL_PASSWD'],
                        database = settings['MYSQL_DBNAME'],
                        charset = 'utf8',
                        cursorclass = MySQLdb.cursors.DictCursor,
                        use_unicode = True
                        #注意，这里的变量名一定要与connect函数中的参数名一样
                    )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入 变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item)

    #添加一个处理异步插入时出现的异常错误的函数
    def handle_error(self, failure, item):
        print(failure)


    def do_insert(self, cursor, item):
        # 从item类中调用定制的insert_sql, params
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

        return item


#自定义一个图片处理管道文件, 使其产生front_image_path字段
class ArticleimagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        #先用pass在这里设断点，获得results的格式
        #results = [(True, {'url': 'http://wx2.sinaimg.cn/large/7cc829d3gy1fptsk9tvx8j20go0b441z.jpg',
        #                         'path': 'full/031407902bdeff19a2af7d3163aefed119d82c52.jpg',
        #                         'checksum': '277e1d3743656284ce99910973cdca73'})]
        if 'front_image_path' in item:
            for status, value in results:
                item['front_image_path'] = value['path']
        #一定要有return item
        return item