
import scrapy
from zhihu_live.items import ZhihuLiveItem
from scrapy_splash import SplashRequest
from urllib.parse import urljoin


class live(scrapy.Spider):
    name = 'zhihu_live'
    start_urls = ["https://www.zhihu.com/lives"]
    custom_settings = {"COOKIES_ENABLED": True}
    headers = {'User-Agent': 'Mozilla/5.0'}

    def start_requests(self):
        #设置滚动条下滑以加载更多
        script = """
                        function main(splash)
                            splash:set_viewport_size(1024, 10000)
                            splash:go(splash.args.url)
                            local scroll_to = splash:jsfunc("window.scrollTo")
                            scroll_to(0, 5000)
                            splash:wait(15)
                            return {
                                html = splash:html()
                            }
                        end
                 """
        #需要设置user-agent
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, meta = {
                'dont_redirect': True,
                'splash':{
                    'args':{'lua_source':script,'images':0},
                    'endpoint':'execute',

                }
            })

    def parse(self, response):
        zh_live = ZhihuLiveItem()
        titles = response.xpath("//div[@class='LiveItem-title-vgQH utils-textEllipsis-3FN2']/text()").extract()
        lecturers = response.xpath("//div[@class='LiveItem-description-1ZrY utils-textEllipsis-3FN2']/text()").extract()
        # link = response.xpath("//a[@class='LiveItem-root-OO1E LiveItem-withMobileLayout-bLOD Card-card-102t']/@href").extract()
        links = response.xpath("//*[@id='feedLives']/div[1]/a/@href").extract()
        labels = response.xpath("//div[@class='LiveInfo-info-340v LiveItem-info-1Z1Q']/div[1]/@aria-label").extract()
        live_classes = response.xpath("//div[@class='LiveItem-tags-DFwD utils-clearfix-3oo3']/span/span/text()").extract()

        for title, lecturer, link, label, live_class in zip(titles, lecturers, links, labels, live_classes):
            zh_live['title'] = title
            zh_live['lecturer'] = lecturer
            zh_live['link'] = urljoin('https://www.zhihu.com/', link)
            zh_live['label'] = label[3:6]
            zh_live['live_class'] = live_class
            yield SplashRequest(url = zh_live['link'], callback=self.live_detail,
                                meta={'zh_live':zh_live}, args={'wait': 2})

    def live_detail(self, response):
        zh_live=response.meta['zh_live']
        zh_live['introduce'] = response.xpath('//div[@class="RichText-richText-89ez"]/text()').extract()
        zh_live['comm_nums'] = response.xpath('//div[@class="LiveContentInfo-reviewText-1ncS"]/text()').extract().split(' ')[0]
        zh_live['lect_time'] = ' '.join(response.xpath('//div[@class="LiveContentInfo-item-w7BI"]/div/text()').extract())
        yield zh_live