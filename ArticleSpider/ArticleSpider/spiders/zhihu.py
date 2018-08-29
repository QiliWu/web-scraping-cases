# -*- coding: utf-8 -*-
import scrapy
import time
import re
import urllib.parse
from ArticleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem
from scrapy.loader import ItemLoader
import json
import datetime

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_answer_url = '''https://www.zhihu.com/api/v4/questions/29138020/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=&limit=3&sort_by=default'''

    headers = {'User-Agent':'Mozilla/5.0'}

    def parse(self, response):
        """
        提取出html页面中所有的url, 并跟踪这些url进行下一步爬取
        如果提取的url格式为/question/xxx就下载之后直接进行解析函数
        """
        all_urls = response.css('a::attr(href)').extract()
        for url in all_urls:
            url = urllib.parse.urljoin(response.url, url)
            match_obj = re.match('(.*zhihu\.com/question/(\d+)).*', url)
            if match_obj:
                question_url = match_obj.group(1)
                question_id = int(match_obj.group(2))
                yield scrapy.Request(url=question_url, headers=self.headers, meta={'question_id':question_id}, callback=self.parse_question)

            else:
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        #处理question页面，从页面中提取出具体的question item
        #debug时如果修改了下面itemloader的内容，需要重新开始debug修改才能起效，否则还是按照修改之前的代码运行。
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_value('zhihu_id', response.meta.get('question_id', ''))
        item_loader.add_css('title', 'h1::text')
        item_loader.add_css('topics', '.Tag.QuestionTopic .Popover div::text')
        item_loader.add_value('url', response.url)
        item_loader.add_css('content', '.QuestionHeader-detail')   #只去html值，不取text值
        item_loader.add_css('answer_num', '.List-headerText span::text')
        item_loader.add_css('comments_num', '.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num', '.NumberBoard-itemValue::text')  #这里有个坑，button标签在爬下来后变成了div
        item_loader.add_css('click_num', '.NumberBoard-itemValue::text')
        #itemloader.add_css('crawl_time', 'h1.QuestionHeader-title::text')

        question_item = item_loader.load_item()
        yield question_item

        #发起获取前20个answer的请求
        yield scrapy.Request(url=self.start_answer_url.format(response.meta.get('question_id', '')),
                             headers=self.headers,
                             callback=self.parse_answer)

    def parse_answer(self, response):
        answer_json = json.loads(response.text)
        is_end = answer_json['paging']['is_end']
        next_answer_url = answer_json['paging']['next']

        for data in answer_json['data']:
            itemloader = ItemLoader(item=ZhihuAnswerItem(), response=response)
            itemloader.add_value('zhihu_id', data['id'])
            itemloader.add_value('question_id', data['question']['id'])
            itemloader.add_value('author_id', data['author']['id'] if 'id' in data['author'] else None)
            itemloader.add_value('url', data['url'])
            itemloader.add_value('content', data['content'] if 'content' in data else data['excerpt'])
            itemloader.add_value('create_time', data['created_time'])
            itemloader.add_value('update_time', data['updated_time'])
            itemloader.add_value('praise_num', data['voteup_count'])
            itemloader.add_value('comments_num', data['comment_count'])
            itemloader.add_value('crawl_time', datetime.datetime.now())

            answer_item = itemloader.load_item()
            yield answer_item

        if not is_end:
            yield scrapy.Request(url=next_answer_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        from selenium import webdriver

        browser = webdriver.Chrome()
        browser.get('https://www.zhihu.com/signin')
        time.sleep(3)

        # 通过send_keys()方法传递用户名和密码
        browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('15013238232')
        browser.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').send_keys(
            '15013238232')
        browser.find_element_by_css_selector('.Button.SignFlow-submitButton').click()

        time.sleep(10)
        Cookies = browser.get_cookies()
        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            # #写入文件
            # f = open('D:/03-CS/scrapy/ArticleSpider/ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            # pickle.dump(cookie, f)
            # f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=Cookies, headers = self.headers)]
