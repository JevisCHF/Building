# -*- coding: utf-8 -*-
import scrapy
import re
# import pymysql
# import click  # 日志打印
from Scrapy_Qianzhan_V1.items import ScrapyQianzhanV1Item
from Scrapy_Qianzhan_V1.start_urls import urls3, get_url
from Scrapy_Qianzhan_V1.setting_dir import set_id
from Scrapy_Qianzhan_V1.myy import select_count, select, insert


class QianzhanV1Spider(scrapy.Spider):
    name = 'qianzhan_V3'
    allowed_domains = ['d.qianzhan.com/']
    base_url = 'https://d.qianzhan.com'

    def start_requests(self):
        u = get_url(urls3)
        for i in u:
            req = scrapy.Request(url=i, callback=self.parse, dont_filter=True)
            yield req

    def parse(self, response):
        config_list = response.xpath('//div[@class="search-result_con search-result_con2"]/table/tbody/tr')
        # print(len(config_list))

        for i in range(1, len(config_list)):
            item = ScrapyQianzhanV1Item()

            title = config_list[i].xpath('./td[1]//text()').extract()
            title = ''.join(title)
            unit = config_list[i].xpath('./td[2]/text()').extract_first()
            url = self.base_url + config_list[i].xpath('./td[1]/a/@href').extract_first()
            req = scrapy.Request(url=url, callback=self.parse_detail, dont_filter=True, meta={'item': item})

            item['indic_name'] = title
            item['unit'] = unit if unit else None
            item['data_source'] = '前瞻数据库'

            yield req

    def parse_detail(self, response):
        item = response.meta['item']
        id_region = set_id(item['indic_name'])
        parent_id = id_region['p_id']
        region = id_region['region']
        count = select_count(parent_id)

        if count < 9:
            child_id = parent_id + f'00{count + 1}'
        elif (count >= 9) and (count < 99):
            child_id = parent_id + f'0{count + 1}'
        else:
            child_id = parent_id + f'{count + 1}'

        # 判断是否已存在这个目录
        pos = response.xpath('//aside[@class="navadr"]/a/text()').extract()
        isRep = '>'.join(pos)
        isHave = select(isRep, item['indic_name'])

        if not isHave:
            insert(child_id, item['indic_name'], parent_id, isRep)
            print('添加成功')

            item['root_id'] = child_id[0]
            item['parent_id'] = child_id
            item['country'] = '中国'
            item['region'] = region

            config_list = response.xpath('//table[@class="search-result_table"]/tbody/tr')

            for i in range(2, len(config_list)):
                issue_time = config_list[i].xpath('./td[@class="f_blue3"]/text()').extract_first().replace('.', '-')
                value = config_list[i].xpath('./td[3]/text()').extract_first()

                if value:
                    item['data_value'] = float(value)
                    item['sign'] = '19'
                    item['status'] = 1
                    item['cleaning_status'] = 0

                    frequency = re.search(r'\((.+)\)', item['indic_name']).group(1)
                    year = 0
                    month = 0
                    day = 0
                    if frequency == '年':
                        frequency = 5
                        year = issue_time
                        month = 12
                        day = 31

                    elif frequency == '季度':
                        if issue_time[-2:] == '03':
                            frequency = 1
                        elif issue_time[-2:] == '06':
                            frequency = 2
                        elif issue_time[-2:] == '09':
                            frequency = 3
                        elif issue_time[-2:] == '12':
                            frequency = 4

                        year = issue_time[:4]
                        month = issue_time[-2:]
                        day = 31

                    elif frequency == '月':
                        frequency = 6
                        year = issue_time[:4]
                        month = issue_time[-2:]
                        day = 31

                    elif frequency == '周':
                        frequency = 7
                        year = issue_time[:4]
                        month = issue_time[5:7]
                        day = issue_time[-2:]

                    elif frequency == '日':
                        frequency = 8
                        year = issue_time[:4]
                        month = issue_time[5:7]
                        day = issue_time[-2:]

                    else:
                        frequency = 0

                    item['data_year'] = int(year)
                    item['data_month'] = int(month)
                    item['data_day'] = int(day)
                    item['create_time'] = f'{year}-{month}-{day}'
                    item['frequency'] = frequency
                    # print(item)

                    yield item

                    self.logger.info(
                        "title({}), create_time({})".format(item['indic_name'], item['create_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'qianzhan_V3'])
