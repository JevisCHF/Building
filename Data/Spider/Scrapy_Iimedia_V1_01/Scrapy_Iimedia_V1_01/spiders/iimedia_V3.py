# -*- coding: utf-8 -*-
import scrapy, json, time, re, csv
from Scrapy_Iimedia_V1_01.items import ScrapyIimediaV101Item
from Scrapy_Iimedia_V1_01.isCountry import find_region
from Scrapy_Iimedia_V1_01.settings import cate3 as c


class IimediaV3Spider(scrapy.Spider):
    name = 'iimedia_V3'
    urls = {}
    # allowed_domains = ['123']
    # start_urls = ['http://123/']

    def start_requests(self):
        # config_info = json.loads(response.text)
        # print(config_info)
        # 直接进入能源页面
        for k, v in c.items():
            keys = k.split('-')
            # print(keys)
            r_id = v[:7]
            name = v[7:]
            cate = f'"{r_id}": "{name}",'
            print(cate)
            with open(
                    'E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list3.txt',
                    'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            data = {
                'pid': keys[2],
            }

            r_id = r_id + keys[0]
            name = keys[1]
            cate = f'"{r_id}": "{name}",'
            print(cate)
            with open(
                    'E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list3.txt',
                    'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            req = scrapy.FormRequest(url='https://data.iimedia.cn/front/childList', formdata=data,
                                     callback=self.parse1,
                                     dont_filter=True, meta={'cate': name, 'r_id': r_id})
            req.headers["referer"] = "https://data.iimedia.cn/page-category.jsp?nodeid=11369993"
            req.headers["Origin"] = "https://data.iimedia.cn"

            yield req

    # 建立二级目录
    def parse1(self, response):
        # r_id = response.meta['r_id']
        config_info = json.loads(response.text)['data']

        i = 1
        for info in config_info:
            c_id = info['id']
            name = info['name']
            is_end = info['is_end']

            if i < 10:
                r_id = response.meta['r_id'] + f'00{i}'
            elif (i >= 10) and (i < 100):
                r_id = response.meta['r_id'] + f'0{i}'
            elif i >= 100:
                r_id = response.meta['r_id'] + f'{i}'

            cate = f'"{r_id}": "{name}",'
            print(cate)
            i += 1
            with open(
                    'E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list3.txt',
                    'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            # 判断是否结束，结束了就爬取具体数据，否则继续循环
            if is_end:
                data = {
                    'node_id': c_id,
                }
                req = scrapy.FormRequest(url='https://data.iimedia.cn/front/getObjInfoByNodeId', formdata=data,
                                         callback=self.parse_detail,
                                         dont_filter=True, meta={'cate': name, 'r_id': r_id, 'data': data})
                req.headers['Origin'] = 'https://data.iimedia.cn'
                yield req

            else:
                data = {
                    'pid': c_id,
                }

                req = scrapy.FormRequest(url='https://data.iimedia.cn/front/childList', formdata=data,
                                         callback=self.parse1,
                                         dont_filter=True, meta={'cate': name, 'r_id': r_id, 'data': data})
                req.headers["Origin"] = "https://data.iimedia.cn"
                yield req

    # 爬取具体数据
    def parse_detail(self, response):
        nodeID = response.meta['data']
        r_id = response.meta['r_id']
        name = response.meta['cate']

        config_info = json.loads(response.text)
        # print(config_info)

        try:
            data_info = config_info['data']
            objInfo = data_info["objInfo"]

            source = objInfo["sourceName"]
            unit = objInfo["unit"]
            # name = objInfo["name"]
            frequency = objInfo["frequenceName"]

            objValue = data_info["objValue"]

            for value in objValue["form"]:

                item = ScrapyIimediaV101Item()
                # 父级目录
                item['parent_id'] = r_id
                # 名称
                item['indic_name'] = name
                # 根目录id
                n = len(r_id)
                item['root_id'] = r_id[:-(n - 1)]

                # 地区和国家
                country = find_region(name)
                item['region'] = country['region']
                item['country'] = country['country']

                if not item['country']:
                    country = find_region(source)
                    item['region'] = country['region']
                    item['country'] = country['country']

                create_time = value[0]
                data = value[1]
                data_time = create_time.split('-')
                year = int(data_time[0])
                try:
                    month = int(data_time[1])
                except:
                    month = None
                try:
                    day = int(data_time[2])
                except:
                    day = None

                # 年
                item['data_year'] = year if year else 0
                # 月
                item['data_month'] = month if month else 0
                # 日
                item['data_day'] = day if day else 0

                if frequency == '年':
                    # 频率
                    item['frequency'] = 5

                elif frequency == '季度':
                    # 频率
                    item['frequency'] = 5

                    # 频率
                    if month == 3:
                        item['frequency'] = 1
                    elif month == 6:
                        item['frequency'] = 2
                    elif month == 9:
                        item['frequency'] = 3
                    elif month == 12:
                        item['frequency'] = 4

                elif frequency == '月':
                    # 频率
                    item['frequency'] = 6

                elif frequency == '周':
                    # 频率
                    item['frequency'] = 7

                elif frequency == '天':
                    # 频率
                    item['frequency'] = 8

                else:
                    # 频率
                    item['frequency'] = 0

                if unit:
                    item['unit'] = unit
                else:
                    item['unit'] = None

                # 数据来源
                item['data_source'] = source
                # 数据产生时间
                item['create_time'] = create_time
                # 数值
                item['data_value'] = float(data)
                # 个人编号
                item['sign'] = '19'
                # 0:无效  1: 有效
                item['status'] = 1
                # 0 : 未清洗  1 ： 清洗过
                item['cleaning_status'] = 0
                yield item
                # print(item)
        except:
            print('访问数据需要登录或为报告类！！')
            with open(r'E:\Building\Data\Spider\Scrapy_Iimedia_V1_01\Scrapy_Iimedia_V1_01\fail3.txt', 'a',
                      encoding='utf-8') as f:
                f.write(str(nodeID) + '\n')


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl iimedia_V3".split())
