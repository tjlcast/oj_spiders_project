# -*- coding:utf-8 -*-

from source.login_oj import oj_login
import requests
from lxml import etree


def get_code_page(user_name):
    session_info = oj_login(user_name)

    url = 'http://code.bupt.edu.cn/submission/detail/in_contest/281479/'
    cookie = 'sessionid={sessionid}; csrftoken={csrftoken}'.format(**session_info)
    headers = {}
    headers["Content-Type"]= 'application/x-www-form-urlencoded'
    headers['Cookie'] = cookie

    response = requests.get(url, headers=headers)
    content = response.content
    html = etree.HTML(content)
    code = html.xpath('//div[@class="code"]/pre')[0].text
    print code

if __name__ == '__main__':
    get_code_page('zhangyanmei')