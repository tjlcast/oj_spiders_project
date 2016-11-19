# -*- coding:utf-8 -*-

from source.login_oj import oj_login
from source.Spider.Db_manager import Db_manager
from lxml import etree
import requests

class OJ_Api:
    def __init__(self):
        self.login_inf = None
        self.host = 'http://code.bupt.edu.cn'

    def login(self):
        student_name = "huanghai"
        self.login_inf = oj_login(student_name)


    def get_test_info(self, test_id):
        url = self.host + '/submission/status/contest/{test_id}/page/1/?'.format(test_id=test_id)

        # 得到数据库中相应考试的最大submit_no，
        db = Db_manager()
        max_submit_id = db.get_max_submit_no('test_' + test_id)

        submit_inf = {}

        # 遍历（如果有>=停止）:得到每一页统计（通过点击"下一页"得到下一页）
        while url != None:
            content = self.send_get_request(url)
            html = etree.HTML(content)

            tr_list = html.xpath('//table[@class="table table-bordered table-striped table-hover"]/tr')
            for tr in tr_list:
                item = {
                    'submit_id': '',
                    'prob_id': '',
                    'result': '',
                    'memory': '',
                    'code_language': '',
                    'code_len': '',
                    'submit_time': '',
                    'user_name': '',
                    'score': '',
                    'evaluation_machine': '',
                    'code': '',
                    'ip': '',
                    'run_time': '',
                }
                td_list = tr.xpath('./td')
                item['submit_id'] = td_list[0].text
                item['prob_id'] = td_list[1].xpath('./a/@href')[0]
                item['result'] = td_list[2].xpath('.//a')[0].text
                item['run_time'] = td_list[3].xpath('./span')[0].text
                item['memory'] = td_list[4].text
                item['code_language'] = td_list[5].text
                item['code_len'] = td_list[6].xpath('./a')[0].text
                item['submit_time'] = td_list[7].text
                item['user_name'] = td_list[8].xpath('./a')[0].text


                detail_url = 'http://code.bupt.edu.cn/submission/detail/in_contest/' + item['submit_id'] + '/'
                detail_content = self.send_get_request(detail_url)
                detail_html = etree.HTML(detail_content)

                try:
                    item['score'] = detail_html.xpath('//div[@class="judge-details"]//strong')[0].text
                except:
                    item['score'] = "0"
                detial_tr_list = detail_html.xpath('//table[@class="table-left table-hover"]/tbody/tr')
                item['evaluation_machine'] = detial_tr_list[7].xpath('./td')[1].text
                item['ip'] = detial_tr_list[6].xpath('./td')[1].text
                item['code'] = detail_html.xpath('//div[@class="code"]/pre')[0].text

                submit_inf[item['submit_id']] = item
                print td_list


            div = html.xpath('//div[@class="pagination pagination-centered"]')[-1]
            a = div.xpath('./ul/li/a[last()]')[-1]
            url = self.host + a.xpath('./@href')[0]
            if a.xpath('./@href')[0]=='#':
                url = None
            print url
        print submit_inf


        # 得到每一条记录的detail

        # 存为一个［｛｝］

        # 保存到数据库

    def send_post_request(self, url ):
        pass

    def send_get_request(self, url ):
        cookie = 'Cookie: sessionid={sessionid}; csrftoken={csrftoken}'.format(**self.login_inf)
        headers = {"Content-Type": 'application/x-www-form-urlencoded'}
        headers['Cookie'] = cookie
        response = requests.get(url, headers=headers)
        return response.content


if __name__ == '__main__':
    oj = OJ_Api()
    oj.login()
    oj.get_test_info('496')
    print oj.login_inf

