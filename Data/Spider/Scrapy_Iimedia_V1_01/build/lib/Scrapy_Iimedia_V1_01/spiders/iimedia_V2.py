# -*- coding: utf-8 -*-
import scrapy, json, time, re, csv
from Scrapy_Iimedia_V1_01.items import ScrapyIimediaV101Item
from Scrapy_Iimedia_V1_01.isCountry import find_region
from Scrapy_Iimedia_V1_01.settings import cate2 as c


class IimediaV1Spider(scrapy.Spider):
    name = 'iimedia_V2'
    urls = {}

    # allowed_domains = ['123']
    # start_urls = ['http://123/']

    # json数据接口, post请求
    def start_requests(self):
        # config_info = json.loads(response.text)
        # print(config_info)
        # 直接进入能源页面
        for k, v in c.items():
            keys = k.split('-')
            # print(keys)
            root_id = v[:7]
            name = v[7:]
            cate = f'"{root_id}": "{name}",'
            print(cate)
            with open(
                    'E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list2.txt',
                    'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            data = {
                'key': keys[1],
                'sourceType': '1',
                'nodeIdOfRoot': '0',
                'returnType': '0',
            }

            r_id = root_id + keys[0]
            name = '其他建筑业'

            cate = f'"{r_id}": "{name}",'
            print(cate)
            with open(
                    'E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list2.txt',
                    'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            req = scrapy.FormRequest(url='https://data.iimedia.cn/front/search', formdata=data,
                                     callback=self.parse1,
                                     dont_filter=True, meta={'cate': name, 'root_id': r_id, 'data': data})
            req.headers["Origin"] = "https://data.iimedia.cn"

            yield req

    # 建立二级目录
    def parse1(self, response):
        # print(1)
        config_info = json.loads(response.text)['data']['index']
        # print(config_info)
        i = 1
        for info in config_info:
            num = response.meta['root_id']
            name = info['name']
            childIds = info['childIds']
            child = info['child']  # 判断是否还有子数据，若为空，则没有子数据

            if i < 10:
                num = num + f'00{i}'
            elif (i >= 10) and (i < 100):
                num = num + f'0{i}'
            elif i >= 100:
                num = num + f'{i}'

            cate = f'"{num}": "{name}",'
            i += 1
            print(cate)
            with open('E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list2.txt',
                      'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            yield from self.rec(num, child, childIds)

    # 解析数据结构
    def rec(self, root_id, child, childIds):
        global num
        if child:
            i = 1
            for childdata in child:
                num = root_id
                name = childdata['name']
                childIds = childdata['childIds']
                child = childdata['child']  # 判断是否还有子数据，若为空，则没有子数据

                if i < 10:
                    num = num + f'00{i}'
                elif (i >= 10) and (i < 100):
                    num = num + f'0{i}'
                elif i >= 100:
                    num = num + f'{i}'

                cate = f'"{num}": "{name}",'
                print(cate)
                i += 1
                with open(
                        'E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list2.txt',
                        'a', encoding='utf-8') as f:
                    f.write(cate + '\n')

                yield from self.rec(num, child, childIds)
        else:
            i = 1
            # self.urls = {}
            for Ids in childIds:
                if i < 10:
                    num = root_id + f'00{i}'
                elif (i >= 10) and (i < 100):
                    num = root_id + f'0{i}'
                elif i >= 100:
                    num = root_id + f'{i}'

                self.urls[num] = Ids
                i += 1

            for r, Ids in self.urls.items():
                data = {
                    'node_id': str(Ids)
                }
                yield scrapy.FormRequest(url='https://data.iimedia.cn/front/getObjInfoByNodeId',
                                         callback=self.parse_detail,
                                         formdata=data, meta={'root_id': r, 'data': data})

            self.urls = {}

    # 爬取具体数据
    def parse_detail(self, response):
        nodeID = response.meta['data']
        num = response.meta['root_id']
        # print(num)
        config_info = json.loads(response.text)
        # print(config_info)

        try:
            data_info = config_info['data']
            objInfo = data_info["objInfo"]

            source = objInfo["sourceName"]
            unit = objInfo["unit"]
            name = objInfo["name"]
            frequency = objInfo["frequenceName"]

            objValue = data_info["objValue"]

            cate = f'"{num}": "{name}",'
            print(cate)
            with open('E:\\Building\\Data\\Spider\\Scrapy_Iimedia_V1_01\\Scrapy_Iimedia_V1_01\\spiders\\cate_list2.txt',
                      'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            for value in objValue["form"]:

                item = ScrapyIimediaV101Item()
                # 父级目录
                item['parent_id'] = num
                # 名称
                item['indic_name'] = name
                # 根目录id
                n = len(num)
                item['root_id'] = num[:-(n - 1)]

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
            with open(r'E:\Building\Data\Spider\Scrapy_Iimedia_V1_01\Scrapy_Iimedia_V1_01\fail2.txt', 'a',
                      encoding='utf-8') as f:
                f.write(str(nodeID) + '\n')


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl iimedia_V2".split())
