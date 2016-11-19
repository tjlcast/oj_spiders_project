# -*- coding:utf-8 -*-


import os
import re
import uuid
import requests
from lxml import etree
from source.conf.problem_template import default_template
# from conf.teacher_no import teachers

# lxml etree
# node.text       : 获取文本
# xpath('df/@df') : 获取属性
# 返回是否list是依据html标签，可能返回一个
# 正则式默认为贪婪时

teachers = {
    'huanghai': {
        'username': 'bupt#scshuanghai',
        'passwd': 'destination',
    },
    'zhangyanmei': {
        'username': 'bupt#scszhangyanmei',
        'passwd': 'destination',
    },
    'zhanglei': {
        'username': 'bupt#scszhanglei',
        'passwd': 'destination',
    },
}

oj_url = "http://code.bupt.edu.cn/"



def build_data(user_name):
    page = requests.get(oj_url)
    content = page.content
    tree = etree.HTML(content)
    token_value = tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")[0]
    teacher = teachers[user_name]

    data = dict(**teacher)
    data['csrfmiddlewaretoken'] = token_value
    return data


def build_headers(data):
    user_sid = str(uuid.uuid1()).replace('-', '')
    cookie = 'Cookie: sessionid={}; csrftoken={}'.format(user_sid, data['csrfmiddlewaretoken'])
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    headers['Cookie'] = cookie
    return headers


def oj_login(user_name):
    url = oj_url+'login/'
    data = build_data(user_name)
    headers = build_headers(data)
    page = requests.post(url, data=data, headers=headers)
    return {'sessionid': re.search(r'sessionid=(.*)', page.request.headers['Cookie']).group(1), 'csrftoken': data['csrfmiddlewaretoken']}

