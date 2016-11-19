# -*- coding:utf-8 -*-

import os
import re
import uuid

import requests
from lxml import etree

from source.conf.problem_template import default_template

# lxml etree
# node.text       : 获取文本
# xpath('df/@df') : 获取属性
# 返回是否list是依据html标签，可能返回一个
# 正则式默认为贪婪时


teachers = [
    {
        'username': 'bupt#scshuanghai',
        'passwd': '12345678',
    },
    {
        'username': 'bupt#scszhangyanmei',
        'passwd': '12345678',
    },
    {
        'username': 'bupt#scszhanglei',
        'passwd': '19960820',
    },
]

oj_url = "http://code.bupt.edu.cn/"


def build_data():
    page = requests.get(oj_url)
    content = page.content
    tree = etree.HTML(content)
    token_value = tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")[0]

    data = dict(**teachers[1])
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

def add_a_problem_page(inf):
    url = 'http://code.bupt.edu.cn/problem/addProblem/4/'
    cookie = 'sessionid={sessionid}; csrftoken={csrftoken}'.format(**inf)
    # headers = {}
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    headers['Cookie'] = cookie
    response = requests.get(url, headers=headers)
    for item in response.request.headers.items():
        print item[0] + ' | ' + item[1]
    print response


def add_a_problem(inf):
    url = 'http://code.bupt.edu.cn/problem/addProblem/4/'
    cookie = 'sessionid={sessionid}; csrftoken={csrftoken}'.format(**inf)
    headers = {}
    headers['Cookie'] = cookie

    # data = {}
    tpl = default_template
    tpl['csrfmiddlewaretoken'] = inf['csrftoken']
    tpl['prob_title'] = 'testProblem'
    tpl['prob_desc'] = 'hello world'
    tpl['prob_input_desc'] = 'hello world'
    tpl['prob_output_desc'] = 'hello world'
    tpl['prob_input_sample'] = 'hello world'
    tpl['prob_output_sample'] = 'hello world'
    files_num = tpl.pop('files_num')
    # for item in tpl.items():
    #     data[item[0]] = (None, item[1])

    multiple_files = []
    for num in range(files_num):
        num += 1
        title = tpl['prob_title']
        file_name_input = title + '_' + str(num).zfill(2) + '.input'
        file_name_output = title + '_' + str(num).zfill(2) + '.output'
        multiple_files.append(('data_in', (file_name_input, open(os.path.abspath(".")+'/testProblem/'+file_name_input, 'rb'), 'application/octet-stream')))
        multiple_files.append(('data_out', (file_name_output, open(os.path.abspath(".")+'/testProblem/'+file_name_output, 'rb'), 'application/octet-stream')))
        multiple_files.append(('data_scr', (None, str(100))))
        # pass

    response = requests.post(url, headers=headers, data=tpl, files=multiple_files)
    for item in response.request.headers.items():
        print item[0] + ' | ' + item[1]
    print response



if __name__ == '__main__':
    inf = oj_login()
    add_a_problem(inf)
    pass
