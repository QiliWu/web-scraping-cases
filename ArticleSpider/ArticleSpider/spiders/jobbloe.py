# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from urllib import parse
from ArticleSpider.items import JobbloeArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher  #分发器
from selenium import webdriver
class JobbloeSpider(scrapy.Spider):
    name = 'jobbloe'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # def __init__(self):
    #     self.browser = webdriver.Chrome()
    #     super(JobbloeSpider, self).__init__()   #这里一定要有这个了。
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     #当爬虫关闭时退出browser
    #     self.browser.quit()

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并交给scrapy下载后进行解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交个parse
        :param response:
        :return:
        """
        #从返回的信息中提取每个文章的url, 并交给scrapy进行爬取后解析
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract()[0]
            img_url = post_node.css('img::attr(src)').extract_first() #这个url是不完整的
            #yield(Request(url=post_url, meta={"front_img_url":img_url}, callback=self.parse_detail))
            yield(Request(url=parse.urljoin(response.url, post_url), meta={"front_img_url":img_url}, callback=self.parse_detail))

        #提取下一页并交给scrapy进行下载
        #class有两个属性‘next'和’page-numbers'。使用css就两次调用属性，并去除中间的空格，以此表示多值属性
        #最后一页是没有下一页标签的，所以使用extract_first
        # next_url = response.css('.next.page-numbers::attr(href)').extract_first('')
        # if next_url:
        #     yield (Request(url=next_url, callback=self.parse))

    def parse_detail(self, response):
        # #获取封面图片
        # front_image_url = response.meta.get("front_img_url", "")
        #
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # #title = response.css('.entry-header h1::text').extract()[0]
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip()[:-1].strip()
        # #create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip()[:-1].strip()
        # #点赞数，也可直接使用h10的id属性来定位标签,但是不同文章的id属性不一样，所以不能通用
        # praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0]
        # re_match = re.match('.*?(\d+).*',praise_nums)
        # if re_match:
        #     praise_nums = int(re_match.group(1))
        # else:
        #     praise_nums = 0
        # #praise_nums = int(response.css('.vote-post-up h10::text()')..extract()[0])
        # #收藏数
        # fav_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract()[0]
        # re_match = re.match('.*?(\d+).*', fav_nums)
        # if re_match:
        #     fav_nums = int(re_match.group(1))
        # else:
        #     fav_nums = 0
        # #fav_nums = int(response.css('.bookmark-btn::text').extract()[0])
        # #评论数
        # comment_nums = response.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract()[0]
        # re_match = re.match('.*?(\d+).*', comment_nums)
        # if re_match:
        #     comment_nums = int(re_match.group(1))
        # else:
        #     comment_nums = 0
        # #comment_nums = int(response.css('a[href=“#article-comment"] span::text').extract()[0].strip()[:-3])
        # #文章内容，忽略了标题，因为不同文章的标题标签不一样，不易统一。
        # content = response.xpath('//div[@class="entry"]/p/text()').extract()
        # #content = response.css('div.entry p::text').extract()
        # content = '\n'.join(content)
        # #文章标签，或是分类
        # elements = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # #elements = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        # #去除重复的评论数
        # tags = ','.join([element for element in elements if not element.strip().endswith('评论')])
        #
        # ArticleItem = JobbloeArticleItem()
        # ArticleItem['url_object_id'] = get_md5(response.url)
        # ArticleItem['title'] = title
        # try:
        #     create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now()
        # ArticleItem['create_date'] = create_date
        # ArticleItem['url'] = response.url
        # ArticleItem['front_image_url'] = [front_image_url]
        # ArticleItem['praise_nums'] = praise_nums
        # ArticleItem['fav_nums'] = fav_nums
        # ArticleItem['comment_nums'] = comment_nums
        # ArticleItem['content'] = content
        # ArticleItem['tags'] = tags


        #使用ItemLoader在获取item字段。默认ItemLoader产生的数据都是一个list
        item_loader = ArticleItemLoader(item=JobbloeArticleItem(), response=response)
        # 通过css规则提取字段
        item_loader.add_css('title', '.entry-header h1::text')
        #通过xpath规则提取字段
        item_loader.add_xpath('create_date', '//p[@class="entry-meta-hide-on-mobile"]/text()')
        #直接传入值
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_value('front_image_url', [response.meta.get("front_img_url", "")])

        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('tags', 'p.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content', 'div.entry p::text')

        #item_loader容器里的字段传递给ArticleItem
        ArticleItem = item_loader.load_item()
        import time
        time.sleep(600)

        yield ArticleItem





