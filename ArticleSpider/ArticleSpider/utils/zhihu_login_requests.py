#使用requests 模拟知乎登陆并获取cookie
#知乎页面修改了，这个方法现在已经不使用了

import requests
import time
import re
from http import cookiejar, cookies

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookie.txt')

try:
    session.cookies.load(ingore_discard=True)
except:
    print('cookie未能加载')

headers = {'User-Agent':'Mozilla/5.0'}

def is_login():
    #通过个人中心页面返回状态码来判断是否为登陆状态
    inbox_url = 'https://www.zhihu.com/people/wu-qi-li-49/activities'
    response = session.get(inbox_url, headers=headers, allow_redirect=False)
    if response.status_code != 200:
        return False
    else:
        return True

def get_xsrf():
    response = session.get('http://www.zhihu.com', headers=headers)
    match_obj = re.match('.*name="_xsrf" value="(.*?)".*', response.text, re.DOTALL)
    if match_obj:
        return match_obj.group(1)
    else:
        return ''

def zhihu_login(account, passwd):
    if re.match('^\d+$', account):
        print('手机号登陆')
        post_url = 'http://www.zhihu.com/login/phone_num'
        post_data = {'_xsrf': get_xsrf(),
                     'phone_num': account,
                     'password': passwd}

    if '@' in account:
        print('邮箱登陆')
        post_url ='http://www.zhihu.com/login/email'
        post_data = {'_xsrf': get_xsrf(),
                     'email': account,
                     'password': passwd}

    response = session.post(post_url, headers = headers, data=post_data)
    session.cookies.save()


