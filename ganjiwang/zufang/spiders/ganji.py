import scrapy
from ..items import ZufangItem

class GanjiSpider(scrapy.Spider):
    name = 'zufang'
    start_urls = ['http://bj.ganji.com/fang1/chaoyang/']


    def parse(self,response):
        #print(response)
        zf = ZufangItem()
        title_list = response.xpath(".//div[@class='f-list-item ']/dl/dd[1]/a/text()").extract()
        #print(title_list)
        #f-list-item后 有个空格
        price_list = response.xpath(".//div[@class='f-list-item ']/dl/dd[5]/div[1]/span[1]/text()").extract()
        #print(price_list)
        for i,j in zip(title_list, price_list):
            zf['title']=i
            zf['price']=j
            yield zf
            #print(i,':',j)
#//*[@id="puid-2883032984"]/dl/dd[5]/div[1]/span[1]   for single price
#.//div[@class='f-list-item ']/dl/dd[5]/div[1]/span[1]     for all the price