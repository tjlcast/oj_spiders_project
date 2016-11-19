# -*- coding:utf-8 -*-

import re
from lxml import etree
import requests
import uuid
import json

# tips:
# json模块中dumps，loads对变量进行操作
# json模块中的dump，load对io操作

teachers = [
    {
        'username': 'bupt#scshuanghai',
        'passwd': 'destinaiton',
    },
]

oj_url = "http://code.bupt.edu.cn/"


def build_data():
    page = requests.get(oj_url)
    content = page.content
    tree = etree.HTML(content)
    token_value = tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")[0]

    data = dict(**teachers[0])
    data['csrfmiddlewaretoken'] = token_value
    return data


def build_headers(data):
    user_sid = str(uuid.uuid1()).replace('-', '')
    cookie = 'Cookie: sessionid={}; csrftoken={}'.format(user_sid, data['csrfmiddlewaretoken'])
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    headers['Cookie'] = cookie
    return headers


def oj_login():
    url = oj_url+'login/'
    data = build_data()
    headers = build_headers(data)
    page = requests.post(url, data=data, headers=headers)
    return {'sessionid': re.search(r'sessionid=(.*)', page.request.headers['Cookie']).group(1), 'csrftoken': data['csrfmiddlewaretoken']}


def get_test_no(inf):
    url = 'http://code.bupt.edu.cn/contest/manage/'
    cookie = 'Cookie: sessionid={sessionid}; csrftoken={csrftoken}'.format(**inf)
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    headers['Cookie'] = cookie

    page = requests.get(url, headers=headers)
    return page.content


def parse_test_no(content):
    pat = re.compile(r"<a href=\"(.*?)\">2016-计算导论与程序设计-第.*?次机考-第.*?场\(.*?\)</a>")
    test_no = pat.findall(content)
    json.dump(test_no, open('test_no.dat', 'w'))


if __name__ == '__main__':
    inf = oj_login()
    content = get_test_no(inf)
    parse_test_no(content)
