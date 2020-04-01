# -*- coding: utf-8 -*-
import pymysql
from Scrapy_Qianzhan_V1.file1 import cate
from Scrapy_Qianzhan_V1.file import cate1, cate2, cate3, cate4
from Scrapy_Qianzhan_V1.config import HOST, PORT, MYSQL_CLIENT, MYSQL_TABLE, ROOT_FIELD
import click


def connect():
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="root",
                           database="building",
                           charset="utf8")
    db = conn.cursor()
    return db, conn


def insert(sql):
    db, conn = connect()
    try:

        info = db.execute(sql)
        print(info)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


def main():
    cate = [cate1, cate2, cate3, cate4]
    for i in cate:
        for key, value in i.items():

            if len(key) <= 4:
                parent_menu_id = key[0]
                id = key
                menu_name = value
                sql = "insert into building_qianzhan(id, menu_name, parent_menu_id) values('%s','%s','%s');" % (
                id, menu_name, parent_menu_id)
                # print(sql)
                insert(sql)
            else:
                parent_menu_id = key[:-3]
                id = key
                menu_name = value
                sql = "insert into building_qianzhan(id, menu_name, parent_menu_id) values('%s','%s','%s');" % (
                id, menu_name, parent_menu_id)
                # print(sql)
                insert(sql)


class mysqlAPP():
    def __init__(self):
        self.client = pymysql.connect(**MYSQL_CLIENT)
        self.cursor = self.client.cursor()
        self.table = MYSQL_TABLE

    def select_count(self, parent_id):
        sql = f'SELECT count(*) FROM building_qianzhan_copy1 WHERE parent_menu_id = {parent_id}'
        print(sql)
        self.cursor.execute(sql)
        # fetchone 返回字典
        result = self.cursor.fetchone()
        if result:
            return result
        return

    def select(self, child_id):
        sql = f'SELECT count(*) FROM building_qianzhan_copy1 WHERE id = {child_id}'
        print(sql)
        self.cursor.execute(sql)
        # fetchone 返回字典
        result = self.cursor.fetchone()
        if result:
            return result
        return

    def insert(self, id, menu, parent_id):
        sql = f'INSERT INTO {self.table} VALUES ({id}, {menu}, {parent_id})'
        try:
            self.cursor.execute(sql)
        except Exception as e:
            click.echo("插入操作异常，异常为:{}".format(e))
            with open('error.log', 'a', encoding='utf8') as f:
                f.write('插入异常字段为:' + dic['dir_name'] + '\n')

    def close(self):
        self.client.close()


if __name__ == '__main__':
    main()
