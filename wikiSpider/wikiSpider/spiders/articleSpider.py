from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from wikiSpider.items import Article
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from html.parser import HTMLParser as SGMLParser

class ArticleSpider(CrawlSpider):
    name = 'article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ["http://en.wikipedia.org/wiki/Main_Page",
                  "http://en.wikipedia.org/wiki/Python_%28programming_language%29"]
    rules = [Rule(SgmlLinkExtractor(allow=('(/wiki/)((?!:).)*$'),), callback='parse_item', follow=True)]


    def parse(self, response):
        item = Article()
        title = response.xpath('//h1/text()')[0].extract()
        print('Title is: '+title)
        item['title'] = title
        return item



