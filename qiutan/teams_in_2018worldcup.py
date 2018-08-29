from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import time
import traceback


def getURLlist(url, teamURLlist, driver):
    #获取每个参赛国家对应的链接
    driver.get(url)
    time.sleep(3)
    try:
        a_list = driver.find_elements_by_xpath('//table[@id="ScoreGroupTab"]/tbody/tr/td[2]/a')
        #print(len(a_list))
        if a_list:
            for i in a_list:
                teamURLlist.append(i.get_attribute('href'))
            # driver.close()
            return teamURLlist
        else:
            return []
    except:
        traceback.print_exc()
        return []


def getMatchInfo(teamURLlist, fpath, driver):
    with open (fpath, 'w') as f:
        f.write('比赛,时间,主队,比分,客队,犯规,黄牌,红牌,控球率,射门（射正）,传球（成功）,传球成功率,过人次数,评分\n')
        if teamURLlist:
            for url in teamURLlist:
                driver.get(url)
                time.sleep(3)
                # 总共包含5页的数据，虽然所有数据在driver.page_source中都可见。
                # 但是，除第一页以外，其他的数据style属性都是“display:none",selenium对这些元素是无法直接操作的。
                # 我们需要通过JavaScipt 修改display的值
                # 首先把html中的所有tr标签的style属性都设为display='block'
                js = 'document.querySelectorAll("tr").forEach(function(tr){tr.style.display="block";})'
                driver.execute_script(js)

                #接下来，就可以把所有的比赛成绩数据都爬下来
                infolist = driver.find_elements_by_xpath('//div[@id="Tech_schedule"]/table/tbody/tr')

                # 第一个tr中包含的是表格的title信息，剔除
                for tr in infolist[1:]:
                    td_list = tr.find_elements_by_tag_name('td')
                    matchinfo = []
                    for td in td_list:
                        # 部分td的style属性也为“display:none"，info 则对应为‘’，
                        # 这些td对应的是角球，越位，头球，救球，铲球等信息，不是很重要，就不爬取了。
                        info = td.text
                        if info:  # 去除空字符
                            matchinfo.append(td.text)
                            matchinfo.append(',')    #添加逗号作为分隔符
                    matchinfo.append('\n')   #在列表最后加上换行符
                    print(matchinfo)
                    #将一条比赛信息写入到文件中
                    f.writelines(matchinfo)
                #每个网页爬完后，就把打开的浏览器关掉

def main():
    # chrome driver 要和chrome浏览器对应的版本
    driver = webdriver.Chrome()
    start_url = 'http://zq.win007.com/cn/CupMatch/75.html'
    output = r'D:/03-CS/web scraping cases/qiutan/worldcup2018.csv'
    startlist = []
    resultlist = getURLlist(start_url, startlist, driver)
    print(resultlist)
    getMatchInfo(resultlist, output, driver)
    print('\nfinished\n')

main()

