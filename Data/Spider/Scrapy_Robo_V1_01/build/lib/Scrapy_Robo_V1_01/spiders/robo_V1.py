# -*- coding: utf-8 -*-
import scrapy, json, os, re
from Scrapy_Robo_V1_01.items import ScrapyRoboV101Item
from Scrapy_Robo_V1_01.settings import cate as c


class RoboV1Spider(scrapy.Spider):
    name = 'robo_V1'

    headers = {
        'origin': 'https://robo.datayes.com',
        'referer': 'https://robo.datayes.com/v2/landing/indicator_library',
    }

    # allowed_domains = ['123']
    # start_urls = ['http://123/']

    # 登录
    def start_requests(self):
        # 登陆,https://gw.datayes.com/usermaster/authenticate/web.json
        url = 'https://gw.datayes.com/usermaster/authenticate/web.json'
        data = {
            # ly
            'username': 'a8B83H8erh7uFDPsSUL/IPNpIbwbZKtw4OLZZILeyPmyNJc0sh8l1ftH3x+Cw9NC2rnULHO8HFflCtSw3kXO+TpF3jNaeEmwEBDv7UJE0Gj8aBmQf5xIkOg17C4DJA4IVn4GoYokAuQltHhYy2rAHWROfVgKU/m1bg5wNolu3WI=',
            'password': 'bBHrHblccrcOUmdJ+ZYfhdZtV356sxZKjI1p3+W2sywEYCXPnyKFpazJX9CWx6SFEXEf1yMZiOaYEdxT+JPA0F8T7FkB4mc82CqjQYbIUUhaHkgYvQB5niZgFW03jojwzBHr+9AP9ixvxhb5Obiqzw2myh8GU7/XWPs3uXiiDNs=',
            'rememberMe': 'false',
        }
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse_data, dont_filter=True)

    # 起始网站
    def parse_data(self, response):
        # 行业分类：关键字
        for k, v in c.items():
            keys = k.split(' ')

            root_id = v[:7]
            name = v[7:]
            cate = f'"{root_id}": "{name}",'
            print(cate)
            with open(
                    r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list.txt',
                    'a', encoding='utf-8') as f:
                f.write(cate + '\n')
            for i in range(len(keys)):
                r_id = root_id + f'00{i + 1}'
                name = keys[i]

                cate = f'"{r_id}": "{name}",'
                print(cate)
                with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list.txt',
                          'a', encoding='utf-8') as f:
                    f.write(cate + '\n')

                url = f'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input={keys[i]}'
                req = scrapy.Request(url=url, callback=self.parse1, dont_filter=True,
                                     meta={'root_id': r_id, 'link': url}, headers=self.headers)
                # req.headers['referer'] = "https://robo.datayes.com/v2/landing/indicator_library"
                # req.headers['origin'] = "https://robo.datayes.com"
                yield req

    # 解析数据结构
    def rec(self, routeNames, macro, hasChildren, childData, data, link):
        if hasChildren:
            i = 1
            for child in childData:
                co = data
                nameCn = child['nameCn']
                routeNames = child['routeNames']
                indicId = child['indicId']
                hasChildren = child['hasChildren']
                childData = child['childData']

                if i < 10:
                    num = co + f'00{i}'
                elif (i >= 10) and (i < 100):
                    num = co + f'0{i}'
                elif i >= 100:
                    num = co + f'{i}'

                cate = f'"{num}": "{nameCn}",'
                print(cate)
                i += 1
                with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list.txt',
                          'a', encoding='utf-8') as f:
                    f.write(cate + '\n')

                yield from self.rec(routeNames, macro, hasChildren, childData, num, link)
        else:
            url = link + f'&macro={macro}&catelog={routeNames}'
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse2, meta={'num': data}, headers=self.headers)

    # 建立下一级目录
    def parse1(self, response):
        root_id = response.meta['root_id']
        link = response.meta['link']

        config_info = json.loads(response.text)
        catelog = config_info['data']['catelog']
        i = 1
        for log in catelog:
            nameCn = log['nameCn']
            routeNames = log['routeNames']
            indicId = log['indicId']
            hasChildren = log['hasChildren']
            childData = log['childData']

            if i < 10:
                num = root_id + f'00{i}'
            elif (i >= 10) and (i < 100):
                num = root_id + f'0{i}'
            elif i >= 100:
                num = root_id + f'{i}'

            cate = f'"{num}": "{nameCn}",'
            i += 1
            with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list.txt',
                      'a', encoding='utf-8') as f:
                f.write(cate + '\n')
            print(cate)
            # print(nameCn, routeNames, hasChildren)
            yield from self.rec(routeNames, nameCn, hasChildren, childData, num, link)

    def parse2(self, response):
        # print(123456)
        config_info = json.loads(response.text)
        hits = config_info['data']['hits']
        i = 1
        for hit in hits:
            num = response.meta['num']
            indicId = hit['indicId']
            nameCn = hit['title']
            # infoSourceCn = hit['infoSourceCn']
            # print(indicId, nameCn, infoSourceCn)

            if i < 10:
                num = num + f'00{i}'
            elif (i >= 10) and (i < 100):
                num = num + f'0{i}'
            elif i >= 100:
                num = num + f'{i}'

            cate = f'"{num}": "{nameCn}",'
            print(cate)
            i += 1
            with open(r'E:\Building\Data\Spider\Scrapy_Robo_V1_01\Scrapy_Robo_V1_01\spiders\cate_list.txt',
                      'a', encoding='utf-8') as f:
                f.write(cate + '\n')

            url = 'https://gw.datayes.com/rrp_adventure/web/dataCenter/indic/{}?compare=false'.format(indicId)
            yield scrapy.Request(url, callback=self.parse_content, dont_filter=True,
                                 meta={'num': num, 'indic_name': nameCn}, headers=self.headers)

    # 开始爬取数据
    def parse_content(self, response):
        parent_id = response.meta['num']
        indic_name = response.meta['indic_name']
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

    args = "scrapy crawl robo_V1".split()
    cmdline.execute(args)
