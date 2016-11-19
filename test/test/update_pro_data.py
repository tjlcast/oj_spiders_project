# -*- coding:utf-8 -*-

import os
import re
import uuid

import requests
from lxml import etree

from source.conf.problem_template import default_template

"""
    @author: tangjialiang
    把改文件的｛同级目录｝中的files数据上传到teacher的存在题目中
"""


teachers = {
    'huanghai': {
        'username': 'bupt#scshuanghai',
        'passwd': 'destinaiton',
    },
    'zhangyanmei': {
        'username': 'bupt#scszhangyanmei',
        'passwd': 'destinaiton',
    },
    'zhanglei': {
        'username': 'bupt#scszhanglei',
        'passwd': 'destinaiton',
    },
}

teacher = teachers["zhangyanmei"]
oj_url = "http://code.bupt.edu.cn/"
files = ['1223_test_pro_second']


def build_data():
    page = requests.get(oj_url)
    content = page.content
    tree = etree.HTML(content)
    token_value = tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")[0]

    data = dict(**teacher)
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


def update_pro_data(inf):
    # tests = [for file in os.listdir('./') if ]
    for file in files:
        datas = os.listdir('./'+file)
        old(inf, datas, file)


def old(inf, datas, pro_info):
    pro_no = pro_info.split('_')[0]
    pro_name = '_'.join(pro_info.split('_')[1:])

    update_url = "http://code.bupt.edu.cn/problem/updateProblem/{}/".format(pro_no)
    cookie = 'sessionid={sessionid}; csrftoken={csrftoken}'.format(**inf)
    headers = {}
    headers['Cookie'] = cookie
    response = requests.get(update_url, headers=headers)
    content = response.content
    html = etree.HTML(content)

    # data = {}
    tpl = default_template
    tpl['csrfmiddlewaretoken'] = inf['csrftoken']
    # tpl['prob_title'] = 'testProblem'
    tpl['prob_title'] = html.xpath('//input[@name="prob_title"]/@value')[0]
    # tpl['prob_desc'] = 'hello world'
    tpl['prob_desc'] = html.xpath('//textarea[@name="prob_desc"]')[0].text
    # tpl['prob_input_desc'] = 'hello world'
    tpl['prob_input_desc'] = html.xpath('//textarea[@name="prob_input_desc"]')[0].text
    # tpl['prob_output_desc'] = 'hello world'
    tpl['prob_output_desc'] = html.xpath('//textarea[@name="prob_output_desc"]')[0].text
    # tpl['prob_input_sample'] = 'hello world'
    tpl['prob_input_sample'] = html.xpath('//textarea[@name="prob_input_sample"]')[0].text
    # tpl['prob_output_sample'] = 'hello world'
    tpl['prob_output_sample'] = html.xpath('//textarea[@name="prob_output_sample"]')[0].text
    if 'files_num' in tpl.keys():
        tpl.pop('files_num')


    try:
        if len(datas)%2 != 0:
            raise Exception('the number of data is even where do {pro_no} {pro_name}'.format(pro_no=pro_no, pro_name=pro_name))
        pro_num = len(datas) / 2
        multiple_files = []
        for num in range(pro_num):
            num += 1
            file_name_input = pro_no + '_' +pro_name + '_' + str(num).zfill(2) + '.input'
            file_name_output = pro_no + '_' +pro_name + '_' + str(num).zfill(2) + '.output'
            multiple_files.append(('data_in', (file_name_input, open(os.path.abspath(".")+'/'+pro_info+'/'+file_name_input, 'rb'), 'application/octet-stream')))
            multiple_files.append(('data_out', (file_name_output, open(os.path.abspath(".")+'/'+pro_info+'/'+file_name_output, 'rb'), 'application/octet-stream')))
            multiple_files.append(('data_scr', (None, str(100))))
    except Exception as e:
        raise Exception(str(e), 'where do {pro_no} {pro_name}'.format(pro_no=pro_no, pro_name=pro_name))

    response = requests.post(update_url, headers=headers, data=tpl, files=multiple_files)
    for item in response.request.headers.items():
        print item[0] + ' | ' + item[1]
    print response


if __name__ == '__main__':
    inf = oj_login()
    update_pro_data(inf)
    pass
