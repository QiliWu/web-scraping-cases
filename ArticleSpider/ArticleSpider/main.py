from scrapy.cmdline import execute
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.abspath(__file__))  #D:\03-CS\scrapy\ArticleSpider\ArticleSpider\main.py
# print(os.path.dirname(os.path.abspath(__file__))) #D:\03-CS\scrapy\ArticleSpider\ArticleSpider
# print(sys.path.append(os.path.dirname(os.path.abspath(__file__))))  #None
execute(['scrapy', 'crawl', 'jobbloe'])
# execute(['scrapy', 'crawl', 'zhihu'])
# execute(['scrapy', 'crawl', 'lagou'])
