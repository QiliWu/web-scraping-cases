# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from w3lib.html import remove_tags

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

class ArticleItemLoader(ItemLoader):
    #自定义一个itemloader, 重载ItemLoader类。
    default_output_processor = TakeFirst()
    #如此就会默认提取列表中的第一个元素



def date_convert(value):
    #日期转化函数
    try:
        value = value.strip()[:-1]
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def return_value(value):
    return value

def get_nums(value):
    re_match = re.match('.*?(\d+).*', value)
    if re_match:
        nums = int(re_match.group(1))
    else:
        nums = 0
    return nums

def remove_comment_in_tags(value):
    if '评论' in value:
        return ''
    else:
        return value

def num_convert(value):
    try:
        value = int(value)
    except:
        value = int(re.sub(',','', value))
    return value

class JobbloeArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(input_processor = MapCompose(date_convert))
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(output_processor = MapCompose(return_value))
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(input_processor = MapCompose(get_nums))
    fav_nums = scrapy.Field(input_processor = MapCompose(get_nums))
    comment_nums = scrapy.Field(input_processor = MapCompose(get_nums))
    tags = scrapy.Field(input_processor = MapCompose(remove_comment_in_tags),
                        output_processor = Join(','))
    content = scrapy.Field()

    def get_insert_sql(self):
        #这里的self就是实例化的item
        insert_sql = """
                        insert into jobbole_article(title, create_date, url, url_object_id, 
                        fav_nums, praise_nums, comment_nums, tags, content)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                     """
        params = (self['title'], self['create_date'], self['url'],
                  self['url_object_id'], self['fav_nums'],
                  self['praise_nums'], self['comment_nums'],
                  self['tags'], self['content'])
        return insert_sql, params


class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    #create_time = scrapy.Field()
    #update_time = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                        INSERT INTO zhihu_questions(zhihu_id, topics, url, title, content, 
                        answer_num, comments_num, watch_user_num, click_num, crawl_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), 
                        comments_num=VALUES(comments_num), watch_user_num=VALUES(watch_user_num), 
                        click_num=VALUES(click_num)
                     """

        #处理itemloader返回的列表中的字段
        zhihu_id = self['zhihu_id'][0]
        topics = ','.join(self['topics'])
        url = self['url'][0]
        title = self['title'][0]
        content = self['content'][0]
        answer_num = get_nums(self['answer_num'][0])
        comments_num = get_nums(self['comments_num'][0])
        watch_user_num = num_convert(self['watch_user_num'][0])   #数字大于1000时会采用科学计数法1,000格式，需要转换
        click_num = num_convert(self['click_num'][1])
        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        params = (zhihu_id, topics, url, title, content, answer_num,
                  comments_num, watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                        INSERT INTO zhihu_answers(zhihu_id, question_id, author_id, url, content, 
                        create_time, update_time, comments_num, praise_num, crawl_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE content=VALUES(content), update_time=VALUES(update_time), 
                        comments_num=VALUES(comments_num), praise_num=VALUES(praise_num)
                    """

        zhihu_id = self['zhihu_id'][0]
        question_id = self['question_id'][0]
        author_id = self['author_id'][0]
        url = self['url'][0]
        praise_num = self['praise_num'][0]
        comments_num = self['comments_num'][0]
        content = self['content'][0]
        create_time = datetime.datetime.fromtimestamp(self['create_time'][0])
        update_time = datetime.datetime.fromtimestamp(self['update_time'][0])

        crawl_time = self['crawl_time'][0]

        params = (zhihu_id, question_id, author_id, url, content, create_time,
                  update_time, comments_num, praise_num, crawl_time)

        return insert_sql, params


# class ArticleItemLoader(ItemLoader):
#     #自定义一个itemloader, 重载ItemLoader类。
#     default_output_processor = TakeFirst()
#     #如此就会默认提取列表中的第一个元素

def remove_slash(value):
    if '/' in value:
        value = value.replace('/','')
    value = value.strip()
    return value

def remove_space(value):
    value = value.split('\n')
    value = ' '.join([i.strip() for i in value if i.strip() != '查看地图'])
    return value

class LagouJobItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(input_processor=MapCompose(remove_slash))
    work_years = scrapy.Field(input_processor=MapCompose(remove_slash))
    degree_need = scrapy.Field(input_processor=MapCompose(remove_slash))
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(input_processor=Join(','))
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(input_processor=MapCompose(remove_tags))
    job_addr = scrapy.Field(input_processor=MapCompose(remove_tags, remove_space))
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                     insert into lagou_job(url, url_object_id, title, salary, job_city,
                      work_years, degree_need, job_type, publish_time, tags, job_advantage,
                       job_desc, job_addr, company_name, company_url, crawl_time)
                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                     ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc) 
                     """

        params = (self['url'], self['url_object_id'], self['title'], self['salary'], self['job_city'],
                  self['work_years'], self['degree_need'], self['job_type'], self['publish_time'],
                  self['tags'], self['job_advantage'], self['job_desc'], self['job_addr'],
                  self['company_name'], self['company_url'], self['crawl_time'])

        return insert_sql, params

