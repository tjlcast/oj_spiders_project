# -*- coding:utf-8 -*-

import os

import requests

from source.Action.prepare_test.test_info import test_info
from source.conf.problem_template import default_template
from source.login_oj import oj_login

# 布置test_no的考试
test_no = "4" ;
oj_url = "http://code.bupt.edu.cn/"


def prepare_a_test(inf, pro):

    url = 'http://code.bupt.edu.cn/problem/addProblem/4/'
    cookie = 'sessionid={sessionid}; csrftoken={csrftoken}'.format(**inf)
    headers = {}
    headers['Cookie'] = cookie

    tpl = default_template
    tpl['csrfmiddlewaretoken'] = inf['csrftoken']

    for key, val in pro.items():
        tpl[key] = val

    files_num = tpl.pop('files_num')

    multiple_files = []
    multiple_files.append(('data_in', ("testProblem_01.input", open(os.path.abspath(".") + '/testProblem/testProblem_01.input', 'rb'), 'application/octet-stream')))
    multiple_files.append(('data_out', ("testProblem_01.output", open(os.path.abspath(".") + '/testProblem/testProblem_01.output', 'rb'),'application/octet-stream')))
    multiple_files.append(('data_scr', (None, str(100))))

    response = requests.post(url, headers=headers, data=tpl, files=multiple_files)
    for item in response.request.headers.items():
        print item[0] + ' | ' + item[1]
    print response


def begin():

    for a_teacher in test_info[test_no]:
        user_name = a_teacher['user_name']
        inf = oj_login(user_name)
        pros = a_teacher['pro_info']
        for a_pro in pros:
            prepare_a_test(inf, a_pro)
    pass

if __name__ == '__main__':
    begin()
    pass
