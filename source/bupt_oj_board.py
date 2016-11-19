# -*- coding:utf-8 -*-

import re
from lxml import etree
import requests
import uuid

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


def get_test_board(inf):
    url = 'http://code.bupt.edu.cn/statistic/board/496/'
    cookie = 'Cookie: sessionid={sessionid}; csrftoken={csrftoken}'.format(**inf)
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    headers['Cookie'] = cookie

    page = requests.get(url, headers=headers)
    return page.content


def parser_border(content):
    html = etree.HTML(content)
    students = []
    students_html = html.xpath("//table/tr")
    for student_html in students_html:
        student_no = student_html.xpath("./td[2]")[0].text.split('#')[-1]
        total = student_html.xpath("./td[3]")[0].text
        pro_html = student_html.xpath("./td[position()>4 and position()<=last()]")
        pros = []
        for pro in pro_html:
             pros.append(re.search(r'(\d)',pro.text).group(1))
        pros = '|'.join(pros)
        students.append({'student_no': student_no, 'total': total, 'pros': pros})

    return students


def parser_submission_status():
    pass


if __name__ == '__main__':
    inf = oj_login()
    print inf
    content = get_test_board(inf)
    sit_students = parser_border(content)
    print 'sit:' + str(sit_students)


