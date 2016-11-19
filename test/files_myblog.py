# -*- coding:utf-8 -*-

import os
import requests
import re
from lxml import etree

def upload_files():

    url = "http://127.0.0.1:8000/get_files/"
    response = requests.get(url)
    content = response.content

    html = etree.HTML(content)
    csrfmiddlewaretoken = html.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
    headers = {'Cookie': 'csrftoken='+csrfmiddlewaretoken}
    files = {
            'csrfmiddlewaretoken': (None, csrfmiddlewaretoken),
            'test': (None, 'hello world'),
            'testProblem_01.output': ('testProblem_01.output', open(os.path.abspath(".")+'/testProblem/testProblem_01.output', 'rb'), 'application/octet-stream'),
            'testProblem_01.input': ('testProblem_01.input', open(os.path.abspath(".")+'/testProblem/testProblem_01.input', 'rb'), 'application/octet-stream')
            }

    response = requests.post(url, headers=headers, files=files)
    print response


if __name__ == '__main__':
    upload_files()
