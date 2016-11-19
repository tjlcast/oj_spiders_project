# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors

class Db_manager:
    def __init__(self):
        pass

    def connect(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='destination', db='bupt_oj_spider', port=3306,
                                    cursorclass=MySQLdb.cursors.DictCursor)
        return self.conn.cursor()

    def create_database(self, database_name='bupt_oj_spider'):
        sql = 'create database bupt_oj_spider default character set utf8'

        try:
            cur = self.connect()
            if cur == None:
                raise Exception()
        except Exception as e:
            raise Exception("连接失败")

        try:
            eff = cur.execute(sql)
        except Exception as e:
            print e

    def create_test_table(self, name):
        sql = '''create table {name} (id int primary key auto_increment,
        submit_id varchar(20),
        prob_id varchar(20),
        result varchar(20),
        memory varchar(20),
        code_language varchar(20),
        code_len varchar(20),
        submit_time datetime,
        user_name varchar(20),
        score varchar(20),
        evaluation_machine varchar(20),
        code text,
        ip varchar(20)
        run_time datetime,
        ) ;
        '''.format(name=name)
        sql = sql.replace('\n', '').replace('\t', '')
        cur = self.connect()
        eff = cur.execute(sql)

    def add_an_item(self, table_name, item):
        sql = """
        insert into {table_name}(submit_id, prob_id, result, memory, code_language, code_len, submit_time, user_name, score, evaluation_machine, code, ip, run_time)
        values("{submit_id}", "{prob_id}", "{result}", "{memory}", "{code_language}", "{code_len}", "{submit_time}", "{user_name}", "{score}", "{evaluation_machine}", "{code}", "{ip}", "{run_time}")
        """
        sql = sql.format(table_name=table_name, **item)
        sql = sql.replace('\n', '')
        cur = self.connect()
        eff = cur.execute(sql)
        self.close(cur)
        return eff

    def close(self, cursor):
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def get_max_submit_no(self, test_name):
        sql = '''
        select max(submit_id) from {test_name}
        '''.format(test_name=test_name)
        sql = sql.replace('\n', '')

        try:
            cur = self.connect()
            res = cur.execute(sql)
            ans = cur.fetchall()
            print ans
            self.close(cur)
            print res
            return ans[0]['max(submit_id)']
        except Exception as e:
            print e
        return '000'


if __name__ == '__main__':
    dm = Db_manager()
    max_id = dm.get_max_submit_no('test00')
    print max_id
