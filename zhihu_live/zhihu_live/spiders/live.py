from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import scrapy
from zhihu_live.items import ZhihuLiveItem



class live(scrapy.Spider):
    name = 'zhihu_live'
    start_urls = ["https://www.zhihu.com/lives"]

    def parse(self, response):
        zh_live = ZhihuLiveItem()
        title = response.xpath(".//div[@class='LiveItem-title-vgQH utils-textEllipsis-3FN2']/.text()").extract()
        lecturer = response.xpath(".//div[@class='LiveItem-description-1ZrY utils-textEllipsis-3FN2']/.text()").extract()
        link = "http://www/zhihu.com"+response.xpath(".//div[@class='Card-group-1iQj Card-card-102t Card-notSafari-3UQA]/a/@href").extract()
        #link = "http://www/zhihu.com"+response.xpath("//*[@id='feedLives']/div[1]/a/@href").extract()
        label = response.xpath(".//div[@class='LiveInfo-info-340v LiveItem-info-1Z1Q']/div[1]/@aria-label[3:6]").extract()
        live_class = response.xpath(".//div[@class='LiveItem-tags-DFwD utils-clearfix-3oo3']/span/span/.text()").extract()

        for i, j, k, l, m in zip(title, lecturer, link, label, live_class):
            zh_live['title'] = i
            zh_live['lecturer'] = j
            zh_live['link'] = k
            zh_live['label'] = l
            zh_live['live_class'] = m
        yield zh_live

