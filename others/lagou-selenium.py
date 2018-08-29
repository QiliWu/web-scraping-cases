import random, time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import pymongo

#伪装User Agent
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.settings.userAgent'] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36")
driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=r'D:\03-CS\plantomJS\phantomjs-2.1.1-windows\bin\phantomjs')

#不伪装User Agent，直接爬取时会报错
#driver.PhantomJS(executable_path=r'D:\03-CS\plantomJS\phantomjs-2.1.1-windows\bin\phantomjs')

#设置mongodb
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['scrapy']


def getlagou(driver, url):
    #导航到目标网址
    driver.get(url)

    for i in range(1,31):
        #获取当页的dom
        pagecontent = driver.page_source
        #解析HTML文档， result是一个etree._element
        result = etree.HTML(pagecontent)

        #result.xpath('//div[@id="s_position_list"]/ul[@class="item_con_list"]/li')
        #提取HTML中所有招聘信息的列表。每一条信息都包含在<li></li>中。所以上述路径需包含li
        for j in result.xpath('//div[@id="s_position_list"]/ul[@class="item_con_list"]/li'):
            #job需放在循环里面，每次循环时都重新置零。否则不能一条一条的插入
            job = {}
            #j.xpath()得到的是一个列表，列表中只有一个字符串元素， j.xpath()[0]即是提取这个字符串。对于字符串，没有extract()方法可用了
            job['name'] = j.xpath('div/div/div[@class="p_top"]/a[@class="position_link"]/h3/text()')[0]#[0].extract()
            job['company'] = j.xpath('div/div[@class="company"]/div[@class="company_name"]/a/text()')[0]#[0].extract()
            job['salary'] = j.xpath('div/div/div[@class="p_bot"]/div/span/text()')[0]#[0].extract()
            job['link'] = j.xpath('div/div/div[@class="p_top"]/a[@class="position_link"]/@href')[0]#[0].extract()

            #experience的位置比较特殊，是标签套标签。
            #首先j.xpath()选取整个标签，返回只有一个元素的列表。
            #再j.xpath()[0]提取出这个元素，返回一个etree._element.
            #随后.xpath('string(.)')可以提取其中的所有text,包括span和div中的,返回字符串。
            #使用strip()去除字符串首尾的空格。此时的字符串是两段text（span和div),之间以\n分隔
            #因此使用split('\n')将字符串分裂成两段，返回列表，我们只要第二段，即[1]
            #最后再用strip()去除目标字符串前后的空格。
            job['experience'] = j.xpath('div/div/div[@class="p_bot"]/div')[0].xpath('string(.)').strip().split('\n')[1].strip()#[0].extract()
            job['industry'] = j.xpath('div[@class="list_item_top"]/div[@class="company"]/div[@class="industry"]/text()')[0].strip()#[0].extract()
            job['environment'] = j.xpath('div/div/div/a/span[@class="add"]/em/text()')[0]#[0].extract()
            #写xpath时基本思路是对的，但是中间出现了很多拼写错误，导致纠结了很久。下次要注意！

            #将得到的一条招聘信息插入到mongodb中
            db.lagou_cs.insert(job)
        #设置单次循环任务休眠时间
        time.sleep(random.choice(range(3)))
        print("第【{}】页抓取成功".format(i))

        #切换到下一页，注意(.../a[last()]).clock()的用法。点击a中最后一个，即下一页按钮，
        #HTML没有显示出a中所有子tag, 没办法用列表索引。这里只能这样做。
        #driver.find_element_by_xpath('//div[@class="pager_container"]/a[last()]').click()
        driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]').click()
    print('finished')
    #一定是所有循环都结束后才能关闭driver.
    # 最开始把它放在了第一个循环里面，导致第一页爬取结束后driver就关闭了，之后一直报错：由于对方计算机积极拒绝访问，爬取失败。
    driver.quit()

#url = 'http://www.lagou.com/zhaopin'
#mydata = getlagou(driver, url)

cs = 'https://www.lagou.com/jobs/list_?px=new&hy=%E7%A7%BB%E5%8A%A8%E4%BA%92%E8%81%94%E7%BD%91,%E6%95%99%E8%82%B2&city=%E5%85%A8%E5%9B%BD#filterBox'
interesting = getlagou(driver, cs)
