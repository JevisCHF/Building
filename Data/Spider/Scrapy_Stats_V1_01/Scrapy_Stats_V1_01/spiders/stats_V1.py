# -*- coding: utf-8 -*-
import scrapy, json, time, requests, re
from Scrapy_Stats_V1_01.items import ScrapyStatsV101Item
from scrapy.http.cookies import CookieJar


# 爬取年度建筑业数据
class StatsV1Spider(scrapy.Spider):
    name = 'stats_V1'
    # allowed_domains = ['123']
    # start_urls = ['http://123/']
    url = 'http://data.stats.gov.cn/easyquery.htm'
    Form_data = {
        'A04-hgjd': '季度数据',
        'A0F-hgnd': '年度数据',
    }

    def start_requests(self):
        p_id = '5004003'
        cate = '建筑装饰、装修和其他建筑业'
        dire = f'"{p_id}": "{cate}",'
        with open(r'E:\Building\Data\Spider\Scrapy_Stats_V1_01\Scrapy_Stats_V1_01\cate.txt', 'a',
                  encoding='utf-8') as f:
            f.write(dire + '\n')

        n = 1
        for k, v in self.Form_data.items():
            keys = k.split('-')
            key_data = {
                "id": keys[0],  # 建筑业编码：A0F（年度数据）
                "dbcode": keys[1],
                "wdcode": "zb",
                "m": "getTree",
            }
            num = p_id + f'00{n}'
            dire = f'"{num}": "{v}",'
            with open(r'E:\Building\Data\Spider\Scrapy_Stats_V1_01\Scrapy_Stats_V1_01\cate.txt', 'a',
                      encoding='utf-8') as f:
                f.write(dire + '\n')
            n += 1

            req = scrapy.FormRequest(url=self.url, callback=self.parse, dont_filter=True, formdata=key_data,
                                     meta={'p_id': num, 'dbcode': keys[1]})
            req.headers['Referer'] = 'http://data.stats.gov.cn/easyquery.htm'
            yield req

    def parse(self, response):
        cookie = {
            'JSESSIONID': '1E09D3941467EC986C49ED4CD1D14A2F',
            '_trs_uv': 'k4zanh0s_6_17bx',
            'u': 2,
            "experience": "show",
        }
        # print(cookie)
        get_info = json.loads(response.text)
        # print(get_info)
        a = 1
        for info in get_info:
            # print(info)
            Cid = info['id']
            isParent = info['isParent']
            name = info['name']
            pid = info['pid']
            # print(Cid, isParent, name, pid)

            # 5004003 国家统计局 其他建筑业
            p_id = response.meta['p_id']
            # 建立一级目录
            if a < 10:
                p_id = p_id + f'00{a}'
            elif (a >= 10) and (a < 100):
                p_id = p_id + f'0{a}'
            elif a >= 100:
                p_id = p_id + f'{a}'
            cate = f'"{p_id}": "{name}",'
            # print(cate)
            with open(r'E:\Building\Data\Spider\Scrapy_Stats_V1_01\Scrapy_Stats_V1_01\cate.txt', 'a',
                      encoding='utf-8') as f:
                f.write(cate + '\n')
            a += 1

            if isParent:
                key_data = {
                    "id": Cid,  # 能源编码：A07
                    "dbcode": response.meta['dbcode'],
                    "wdcode": "zb",
                    "m": "getTree",
                }
                req = scrapy.FormRequest(url=self.url, callback=self.parse, dont_filter=True, formdata=key_data,
                                         meta={'p_id': p_id, 'dbcode': response.meta['dbcode']})
                yield req

            else:
                keyvalue = {}
                # 参数填充
                keyvalue['m'] = 'QueryData'
                keyvalue['dbcode'] = response.meta['dbcode']
                keyvalue['rowcode'] = 'zb'
                keyvalue['colcode'] = 'sj'
                keyvalue['wds'] = '[]'
                keyvalue['k1'] = str(int(round(time.time() * 1000)))

                df = f'["wdcode": "zb", "valuecode": "{Cid}"]'
                keyvalue['dfwds'] = df.replace('[', '[{').replace(']', '}]')
                # print(keyvalue['dfwds'])

                # 第一次请求
                req = scrapy.FormRequest(url=self.url, formdata=keyvalue, cookies=cookie, callback=self.make_cate,
                                         dont_filter=True, meta={'p_id': p_id, 'cate': cate, 'Cid': Cid,
                                                                 'dbcode': response.meta['dbcode']})

                yield req

    def make_cate(self, response):
        # print(response.text)
        datanodes = json.loads(response.text)['returndata']['datanodes']
        wdnodes = json.loads(response.text)['returndata']['wdnodes']

        a = 1
        for w in wdnodes[0]['nodes']:
            title = w['cname']
            c_id = w['code']
            unit = w['unit']

            p_id = response.meta['p_id']
            # 建立一级目录
            if a < 10:
                p_id = p_id + f'00{a}'
            elif (a >= 10) and (a < 100):
                p_id = p_id + f'0{a}'
            elif a >= 100:
                p_id = p_id + f'{a}'
            cate = f'"{p_id}": "{title}",'
            print(cate)
            print(response.meta['dbcode'])
            with open(r'E:\Building\Data\Spider\Scrapy_Stats_V1_01\Scrapy_Stats_V1_01\cate.txt', 'a',
                      encoding='utf-8') as f:
                f.write(cate + '\n')
            a += 1

            for d in datanodes:
                if c_id in d['code']:
                    value = d['data']['data']
                    item = ScrapyStatsV101Item()
                    # 数据名称
                    item['indic_name'] = title
                    # 单位
                    item['unit'] = unit
                    # 数据目录
                    item['parent_id'] = p_id
                    # 根目录id
                    item['root_id'] = p_id[:1]
                    # 数值
                    item['data_value'] = value
                    # 数据来源(网站名)
                    item['data_source'] = '国家统计局'
                    # 地区
                    item['region'] = '全国'
                    # 国家
                    item['country'] = '中国'
                    # 个人编号  string
                    item['sign'] = '19'
                    # 0:无效  1: 有效       int
                    item['status'] = 1
                    # 0 : 未清洗  1 ： 清洗过      int
                    item['cleaning_status'] = 0

                    if response.meta['dbcode'] == 'hgnd':
                        year = d['code'][-4:]
                        month = 12
                        day = 31
                        # 年、月、日     数据类型：int
                        item['data_year'] = int(year)
                        item['data_month'] = month
                        item['data_day'] = day
                        # 数据产生时间    数据类型：date
                        item['create_time'] = f'{year}-{month}-{day}'
                        # 频率(0：季度， 1234： 季度 ，5678：年月周日 )    数据类型：int
                        item['frequency'] = 5

                    elif response.meta['dbcode'] == 'hgjd':
                        year = d['code'][-5:-1]
                        day = 31
                        # 年、月、日     数据类型：int
                        item['data_year'] = int(year)
                        item['data_day'] = 31

                        frequency = d['code'][-1]
                        
                        if frequency == 'A':
                            # 频率(0：季度， 1234： 季度 ，5678：年月周日 )    数据类型：int
                            item['frequency'] = 1
                            # 数据产生时间    数据类型：date
                            month = 3
                            item['data_month'] = month
                            item['create_time'] = f'{year}-{month}-{day}'

                        elif frequency == 'B':
                            # 频率(0：季度， 1234： 季度 ，5678：年月周日 )    数据类型：int
                            item['frequency'] = 2
                            # 数据产生时间    数据类型：date
                            month = 6
                            item['data_month'] = month
                            item['create_time'] = f'{year}-{month}-{day}'

                        elif frequency == 'C':
                            # 频率(0：季度， 1234： 季度 ，5678：年月周日 )    数据类型：int
                            item['frequency'] = 3
                            # 数据产生时间    数据类型：date
                            month = 9
                            item['data_month'] = month
                            item['create_time'] = f'{year}-{month}-{day}'

                        elif frequency == 'D':
                            # 频率(0：季度， 1234： 季度 ，5678：年月周日 )    数据类型：int
                            item['frequency'] = 4
                            # 数据产生时间    数据类型：date
                            month = 12
                            item['data_month'] = month
                            item['create_time'] = f'{year}-{month}-{day}'

                    yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'stats_V1'])
