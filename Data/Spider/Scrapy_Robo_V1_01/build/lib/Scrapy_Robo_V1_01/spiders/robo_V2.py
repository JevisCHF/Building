# -*- coding: utf-8 -*-
import scrapy, json, os, re
from Scrapy_Robo_V1_01.items import ScrapyRoboV101Item
from Scrapy_Robo_V1_01.settings import cate2 as c


class RoboV1Spider(scrapy.Spider):
    name = 'robo_V2'
    # allowed_domains = ['123']
    # start_urls = ['http://123/']

    # 登录
    def start_requests(self):
        # 登陆,https://gw.datayes.com/usermaster/authenticate/web.json
        url = 'https://gw.datayes.com/usermaster/authenticate/web.json'
        data = {
            # me
            'username': 'lcANIz7li12eYrqyxoqgwVPcMOOWx3FHXngIkwLrWH9HiHQe7sEwBs365WnOivqrIU17rIgSL5gzNfcjCC5KDluYwbRUA1jVkoRYLhFk/OvMtsluanyuaG6uBPfDsPdS21lyQL/wSGOoyOgSsZUYLzbsvOt4omQxTfrey13p180=',
            'password': 'rNZ54m/u8vhijjsl9uBwx0ge/iS5/gNRGf5CChNoALtJTPg8ZL9LpMBL4fjIQDEtEvV3R1bG2piNP9PNhPN25gw0WRKV0rp+iecE7XgWUHOZaSM6gevEPmGz5ANna1ZEoqvBOENZD8uoPMLidclCAh2Lhm23FqUV0WGyeoLbXsY=',
            'rememberMe': 'false'
        }
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse_data, dont_filter=True)

    # 起始网站
    def parse_data(self, response):
        # 行业分类：ID
        for k, v in c.items():
            keys = k.split('-')
            print(keys)

            root_id = v[:7]
            name = v[7:]
            cate = f'"{root_id}": "{name}",'
            print(cate)
            with open(
                    r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list2.txt',
                    'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            r_id = root_id + f'00{keys[0]}'
            name = keys[1]

            cate = f'"{r_id}": "{name}",'
            print(cate)
            with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list2.txt',
                      'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            url = f'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/{keys[2]}'
            req = scrapy.Request(url=url, callback=self.parse1, dont_filter=True,
                                 meta={'r_id': r_id, 'key': keys[0]})
            req.headers['referer'] = "https://robo.datayes.com/v2/landing/indicator_library"
            req.headers['origin'] = "https://robo.datayes.com"
            yield req

    # 判断是否还有子数据，否则直接获取详情
    def parse1(self, response):
        config_list = json.loads(response.text)
        data = config_list['data']
        i = 1
        if int(response.meta['key']) == 3:

            for li in data['childData']:
                r_id = response.meta['r_id']
                c_id = li['id']
                name = li['nameCn']
                hasChildren = li['hasChildren']
                indicId = li['indicId']

                if i < 10:
                    r_id = r_id + f'00{i}'
                elif (i >= 10) and (i < 100):
                    r_id = r_id + f'0{i}'
                elif i >= 100:
                    r_id = r_id + f'{i}'

                cate = f'"{r_id}": "{name}",'
                print(cate)
                with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list2.txt',
                          'a', encoding='utf-8') as f:
                    f.write(cate + '\n')

                i += 1

                if hasChildren:
                    url = f'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/{c_id}'
                    req = scrapy.Request(url=url, callback=self.parse2, dont_filter=True,
                                         meta={'r_id': r_id, 'key': 0})
                    req.headers['referer'] = "https://robo.datayes.com/v2/landing/indicator_library"
                    req.headers['origin'] = "https://robo.datayes.com"
                    yield req

                else:
                    url = f'https://gw.datayes.com/rrp_adventure/web/dataCenter/indic/{indicId}?compare=false'
                    req = scrapy.Request(url=url, callback=self.parse_content, meta={'r_id': r_id, 'name': name})
                    req.headers['referer'] = "https://robo.datayes.com/v2/landing/indicator_library"
                    req.headers['origin'] = "https://robo.datayes.com"
                    yield req

        else:
            for li in data['childData']:
                r_id = response.meta['r_id']
                c_id = li['id']
                name = li['nameCn']
                hasChildren = li['hasChildren']
                indicId = li['indicId']

                if i < 10:
                    r_id = r_id + f'00{i}'
                elif (i >= 10) and (i < 100):
                    r_id = r_id + f'0{i}'
                elif i >= 100:
                    r_id = r_id + f'{i}'

                cate = f'"{r_id}": "{name}",'
                print(cate)
                with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list2.txt',
                          'a', encoding='utf-8') as f:
                    f.write(cate + '\n')

                i += 1

                if hasChildren:
                    url = f'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/{c_id}'
                    req = scrapy.Request(url=url, callback=self.parse1, dont_filter=True,
                                         meta={'r_id': r_id, 'key': 0})
                    req.headers['referer'] = "https://robo.datayes.com/v2/landing/indicator_library"
                    req.headers['origin'] = "https://robo.datayes.com"
                    yield req
                else:
                    url = f'https://gw.datayes.com/rrp_adventure/web/dataCenter/indic/{indicId}?compare=false'
                    req = scrapy.Request(url=url, callback=self.parse_content, meta={'r_id': r_id, 'name': name})
                    req.headers['referer'] = "https://robo.datayes.com/v2/landing/indicator_library"
                    req.headers['origin'] = "https://robo.datayes.com"
                    yield req

    def parse2(self, response):
        config_list = json.loads(response.text)
        data = config_list['data']
        i = 1
        for li in data['childData']:
            r_id = response.meta['r_id']
            c_id = li['id']
            name = li['nameCn']
            hasChildren = li['hasChildren']
            indicId = li['indicId']

            if '建筑' in name:
                if i < 10:
                    r_id = r_id + f'00{i}'
                elif (i >= 10) and (i < 100):
                    r_id = r_id + f'0{i}'
                elif i >= 100:
                    r_id = r_id + f'{i}'

                cate = f'"{r_id}": "{name}",'
                print(cate)
                with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list2.txt',
                          'a', encoding='utf-8') as f:
                    f.write(cate + '\n')

                i += 1

                if hasChildren:
                    url = f'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/{c_id}'
                    req = scrapy.Request(url=url, callback=self.parse1, dont_filter=True,
                                         meta={'r_id': r_id, 'key': 0})
                    req.headers['referer'] = "https://robo.datayes.com/v2/landing/indicator_library"
                    req.headers['origin'] = "https://robo.datayes.com"
                    yield req

    # 开始爬取数据
    def parse_content(self, response):
        parent_id = response.meta['r_id']
        indic_name = response.meta['name']
        config_info = json.loads(response.text)
        data_info = config_info['data']['indic']

        # name = data_info['indicName']
        region = data_info['region']
        country = data_info['country']

        for info in config_info['data']['data']:
            item = ScrapyRoboV101Item()
            # 父级目录
            item['parent_id'] = parent_id
            # 根目录id
            n = len(parent_id)
            item['root_id'] = parent_id[:-(n - 1)]

            # 地区和国家
            item['region'] = region
            item['country'] = country

            # 数值
            data = info['dataValue']
            # 名称
            item['indic_name'] = indic_name

            data_time = info['periodDate'].replace('-', '')
            # 频率
            frequency = data_info['frequency']

            year = int(data_time[0:4])
            month = int(data_time[4:6])
            day = int(data_time[6:8])

            # 年
            item['data_year'] = year if year else 0
            # 月
            item['data_month'] = month if month else 0
            # 日
            item['data_day'] = day if month else 0

            if frequency == '年':

                # 频率
                item['frequency'] = 5

            elif frequency == '季':

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

            elif frequency == '日':
                # 频率
                item['frequency'] = 8
            else:

                # 频率
                item['frequency'] = 0

            # 单位
            unit = data_info['unit']
            if unit:
                item['unit'] = unit
            else:
                suffix = re.findall(r'\((.*?)\)', indic_name)
                num = len(suffix)
                if suffix:
                    item['unit'] = suffix[num - 1]
                else:
                    item['unit'] = None

            # 数据来源(网站名)
            item['data_source'] = data_info['dataSource']

            # 数据产生时间
            item['create_time'] = info['periodDate']
            # 数值
            item['data_value'] = data
            # 个人编号
            item['sign'] = '19'
            # 0:无效  1: 有效
            item['status'] = 1
            # 0 : 未清洗  1 ： 清洗过
            item['cleaning_status'] = 0
            yield item


if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl robo_V2".split()
    cmdline.execute(args)
