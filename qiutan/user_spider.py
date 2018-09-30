# -*- coding: utf-8 -*-
# python36
__author__ = 'wuqili'

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

#爬取球探网所有注册用户的名称，话题数，关注数，和粉丝数
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def userinfo(url):
    #获得单个用户的信息
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    #获取用户名
    username = soup.find('div', {'class':'title'}).find('a',{'href':'#'}).text.strip()
    #获取用户ID
    userID = url.split('=')[-1]
    info = soup.find('div', {'class':'userMsg'})
    num_list = info.find_all('span', {'class':'red b'})
    # 获取话题数
    theme_num = num_list[0].text
    # 获取关注数
    follow_num = num_list[1].text
    # 获取粉丝数
    fans_num = num_list[2].text
    return [username, userID, theme_num, follow_num, fans_num]

def get_fans(userID, username, fans_num):
    #根据用户的ID获取用户粉丝信息, 并写入cdv文件
    url = 'http://ba2.win007.com/user/MyFans?toUserid={0}'.format(userID)
    with open('%s_fans.csv' % username, 'w', encoding='utf8') as f:
        f.write('粉丝名,粉丝ID,粉丝数,主页链接,\n')
        #每页显示18个粉丝, pages为总页数
        pages = fans_num // 18 + 1
        for page in range(1, pages+1):
            data = {'page': page}
            headers = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Length': '6',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'ba2.win007.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                    }
            r = requests.post(url, data=urlencode(data), headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            fans_list = soup.find_all('li')
            for fans in fans_list:
                name_info = fans.find('div', {'class':'name'}).find('a')
                fans_name = name_info.text
                fans_link = 'http://ba2.win007.com'+ name_info.attrs['href']
                fansID = fans_link.split('=')[-1]
                fans_fansnum = fans.find('div', {'class':'info hui_txt'}).text[3:]
                f.write(','.join([fans_name, fansID, fans_fansnum, fans_link, '\n']))
                f.flush()

def get_follow(userID, username, follow_num):
    #根据用户ID获取用户关注者的信息, 并写入cdv文件
    url = 'http://ba2.win007.com/user/MyFollow?toUserid={0}'.format(userID)
    with open('%s_follow.csv' % username, 'w', encoding='utf8') as f:
        f.write('关注用户名,关注用户ID,粉丝数,用户主页链接,\n')
        # 每页显示18个关注者, pages为总页数
        pages = follow_num // 18 + 1
        for page in range(1, pages + 1):
            data = {'page': page}
            headers = {'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Connection': 'keep-alive',
                       'Content-Length': '6',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Host': 'ba2.win007.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                       }
            r = requests.post(url, data=urlencode(data), headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            follow_list = soup.find_all('li')
            for follow in follow_list:
                name_info = follow.find('div', {'class': 'name'}).find('a')
                follow_name = name_info.text
                follow_link = 'http://ba2.win007.com' + name_info.attrs['href']
                followID = follow_link.split('=')[-1]
                follow_fansnum = follow.find('div', {'class': 'info hui_txt'}).text[3:]
                f.write(','.join([follow_name, followID, follow_fansnum, follow_link, '\n']))
                f.flush()

def get_theme(userID, username, theme_num):
    # 根据用户ID获取用户发表话题的信息, 并写入cdv文件
    url = 'http://ba2.win007.com/user/MyThemes?toUserid={0}'.format(userID)
    with open('%s_themes.csv' % username, 'w', encoding='utf8') as f:
        f.write('话题名,话题链接,发表时间,浏览数,回复数,\n')
        # 每页显示10个关注者, pages为总页数
        pages = theme_num // 10 + 1
        for page in range(1, pages + 1):
            data = {'page': page}
            headers = {'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Connection': 'keep-alive',
                       'Content-Length': '6',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Host': 'ba2.win007.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                       }
            r = requests.post(url, data=urlencode(data), headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            theme_list = soup.find_all('div', {'class':'win'})
            for theme in theme_list:
                info = theme.find('a')
                #话题名称
                title = info.text
                #话题链接
                theme_link = 'http://ba2.win007.com' + info.attrs['href']
                #话题发表时间
                pub_time = theme.find('span', {'class':'hui t12'}).text.strip()[3:]
                #浏览数
                read_num = theme.find('div', {'class':'icon_read'}).text.strip()
                #回复数
                reply_num = theme.find('div', {'class': 'icon_reply'}).text.strip()
                f.write(','.join([title, theme_link, pub_time, read_num, reply_num, '\n']))
                f.flush()


def topusers():
    #从用户关注排行榜获取排名前1594位的用户ID
    url = 'http://ba2.win007.com/usersort.html?pn={0}'
    f = open('topusers.csv', 'w', encoding='utf8')
    f.write('用户名,用户ID,主题,关注,粉丝,\n')  #逗号分隔，没空格
    try:
        for i in range(1,41):
            #获取第i页所有用户主页链接，进而获取用户信息
            url = url.format(i)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            info_list = soup.find('table', {'class':'mytable'}).find_all('a', {'target':'_blank'})
            for info in info_list[::2]:
                user_url = 'http://ba2.win007.com' + info.attrs['href']
                user_info = userinfo(user_url)
                user_info.append('\n')
                f.write(','.join(user_info))
                f.flush()
    except Exception as e:
        print(e)
    finally:
        f.close()

if __name__ == '__main__':
    # topusers()
    # get_fans('823396', '七届盘王', 2427)
    # get_follow('1873035', 'hongri13', 41)
    # get_theme('1899903', '307900', 430)

