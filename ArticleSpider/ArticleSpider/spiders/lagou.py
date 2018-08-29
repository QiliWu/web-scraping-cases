# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from datetime import datetime


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    #爬取拉钩需要设置headers，应为每个请求都需要，所以直接修改settings会比较方便。
    # 此外还可以定制start_requests和parse_response中最后yield Request时添加headers信息。
    custom_settings = {
        'COOKIES_ENABLED':False,
        'DOWNLOAD_DELAY':2,
        'DEFAULT_REQUEST_HEADERS':{
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
            (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"""
        }
    }

    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*$'),follow=True),
        Rule(LinkExtractor(allow=r'gongsi$'),  follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+\.html$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item_loader = ArticleItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('title', '.job-name::attr(title)')
        item_loader.add_css('salary', '.job_request p .salary::text')
        item_loader.add_xpath('job_city', '//dd[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath('work_years', '//dd[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath('degree_need', '//dd[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('job_type', '//dd[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css('publish_time', '.publish_time::text')
        item_loader.add_css('tags', '.position-label li::text')
        item_loader.add_css('job_advantage', '.job-advantage p::text')
        item_loader.add_css('job_desc', '.job_bt div')
        item_loader.add_css('job_addr', '.work_addr')
        item_loader.add_css('company_name', '#job_company dt a img::attr(alt)')
        item_loader.add_css('company_url', '#job_company dt a::attr(href)')
        item_loader.add_value('crawl_time', datetime.now())

        lagou_item = item_loader.load_item()
        yield lagou_item



