# -*- coding: utf-8 -*-
import scrapy, time, os, requests, json, re
from Scrapy_Eastmoney_V1_01.items import ScrapyEastmoneyV101Item
from Scrapy_Eastmoney_V1_01.settings import FILES_STORE, CATES_DICT


# from Scrapy_Eastmoney_V1_01.building_dir import building


class ScrapyEastmoneyV1Spider(scrapy.Spider):
    name = 'Scrapy_eastMoney_V1'
    allowed_domains = ['data.eastmoney.com/']
    base_url = 'http://data.eastmoney.com/report/zw_industry.jshtml?'

    # start_urls = ['http://123/']

    # 报告列表接口
    def start_requests(self):
        for key, value in CATES_DICT.items():
            keys = key.split('-')

            cate = f'"{keys[0]}": "{keys[1]}",'
            print(cate)
            with open(r'E:\报告\爬虫\建筑行业\Scrapy_Eastmoney_V1_01\Scrapy_Eastmoney_V1_01\spiders\cate_list.txt', 'a',
                      encoding='utf-8') as f:
                f.write(cate + '\n')

            for k, v in value.items():

                ks = k.split('-')
                r_id = keys[0] + ks[0]
                cate = f'"{r_id}": "{ks[1]}",'
                print(cate)
                # print(v)
                with open(r'E:\报告\爬虫\建筑行业\Scrapy_Eastmoney_V1_01\Scrapy_Eastmoney_V1_01\spiders\cate_list.txt', 'a',
                          encoding='utf-8') as f:
                    f.write(cate + '\n')

                if not os.path.exists(FILES_STORE):
                    os.mkdir(FILES_STORE)

                file_path = os.path.join(FILES_STORE, ks[1])
                if not os.path.exists(file_path):
                    os.mkdir(file_path)

                for page in range(int(ks[2])):
                    url = v.replace('pageNo=1', f'pageNo={page + 1}')
                    print(url)
                    req = scrapy.Request(url=url, callback=self.parse, meta={'r_id': r_id, 'file_path': file_path},
                                         dont_filter=True)
                    req.headers['Referer'] = 'http://data.eastmoney.com/report/industry.jshtml'
                    yield req

    # 获取详情页面链接
    def parse(self, response):
        config_info = response.text[17:-1]
        r_id = response.meta['r_id']
        file_path = response.meta['file_path']

        for info in eval(config_info)['data']:
            title = info['title']
            source = info['orgSName']
            issue_time = info['publishDate'][:10]
            author = info['researcher']
            encodeUrl = info['encodeUrl']
            url = self.base_url + f'encodeUrl={encodeUrl}'
            # print(title, url, source, issue_time, author)

            # if n < 10:
            #     r_id = response.meta['r_id'] + f'00{n}'
            # elif (n >= 10) and (n < 100):\
            #     r_id = response.meta['r_id'] + f'0{n}'
            # elif n >= 100:
            #     r_id = response.meta['r_id'] + f'{n}'
            #
            # cate =

            req = scrapy.Request(url=url, callback=self.parse2, dont_filter=True,
                                 meta={'title': title, 'paper_from': source, 'author': author, 'date': issue_time,
                                       'parent_id': r_id, 'file_path': file_path})
            req.headers['Referer'] = 'http://data.eastmoney.com/report/industry.jshtml'
            # yield req

    # 详情页面获取download_url
    def parse2(self, response):
        # parent_id = response.meta['parent_id']
        file_path = response.meta['file_path']

        link = response.xpath('//a[@class="pdf-link"]/@href').extract_first()
        item = ScrapyEastmoneyV101Item()

        item['abstract'] = None
        item['title'] = response.meta['title']
        item['paper_url'] = link
        item['date'] = response.meta['date']
        item['author'] = response.metta['author']
        item['paper_from'] = response.meta['paper_from']
        item['cleaning_status'] = 0

        file_name = os.path.join(file_path, item['title'] + '.pdf')

        item['parent_id'] = response.meta['parent_id']
        item['paper'] = file_name

        self.download(item['paper_url'], file_name)
        # print(item)
        yield item
        self.logger.info("item:{}".format(item))

    # 下载文件
    def download(self, url, file_name):
        # headers = {
        #     'Cookie': 'LoginKey=247EF7329DE24E3093ED65E525D44545'
        # }
        with requests.get(url=url, stream=True) as f:
            # raise_for_status() 如果status_code 返回的是200，raise_for_status() 返回的是None，如果是404，则会抛出异常
            f.raise_for_status()
            self.logger.info('请求状态码为{},开始下载'.format(f.status_code))

            with open(file_name, 'wb') as file:
                for chunk in f.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
        return


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'Scrapy_eastMoney_V1'])
