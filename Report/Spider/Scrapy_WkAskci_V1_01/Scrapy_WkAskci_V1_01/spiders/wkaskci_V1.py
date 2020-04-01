# -*- coding: utf-8 -*-
import scrapy, time, os, requests, json, re
from Scrapy_WkAskci_V1_01.items import ScrapyWkaskciV101Item
from Scrapy_WkAskci_V1_01.settings import FILES_STORE, CATES_DICT
from Scrapy_WkAskci_V1_01.building_dir import building


class WkaskciV1Spider(scrapy.Spider):
    name = 'wkaskci_V1'
    allowed_domains = ['wk.askci.com']
    # n = 1

    # cookie = {
    #     'LoginKey': '5D55891D41FF4DA5A32C010E478E3F09',
    # }

    # 报告列表接口
    def start_requests(self):
        for p in range(1, 11):
            # tradeId=8 表示建筑房产行业， page 表示页数，    limit   表示每一页显示多少内容
            url = f'http://wk.askci.com/ListTable/GetList?keyword=&bookName=&tradeId=8&typeId=&tagName=&publisher=&page={p}&limit=90'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    # 获取详情页面链接并返回response
    def parse(self, response):
        config_list = json.loads(response.text)
        # print(config_list)

        for i in config_list['data']:
            title = i['BookName']
            cate = i['StrBookTagName']
            if ',' in cate:
                cate = cate.split(',')[0]

            date_time = i['StrBookPublishDate']
            paper_from = i['BookPublisher']
            ReadUrl = i['ReadUrl']
            try:
                p_id = building[cate]

                if not os.path.exists(FILES_STORE):
                    os.mkdir(FILES_STORE)

                file_path = os.path.join(FILES_STORE, cate)
                if not os.path.exists(file_path):
                    os.mkdir(file_path)

                yield scrapy.Request(url=ReadUrl, callback=self.parse2,
                                     meta={'title': title, 'paper_from': paper_from, 'date_time': date_time,
                                           'p_id': p_id, 'file_path': file_path,
                                           'cate': cate})
            except:
                pass

    # 详情页面获取download_url
    def parse2(self, response):
        # cate = response.meta['cate']
        file_path = response.meta['file_path']
        p_id = response.meta['p_id']
        Coo = response.headers['Set-Cookie']
        link = re.search(r'wkpdfpath=(.+); domain=', str(Coo)).group(1).replace('%253a', ':').replace('%252f', '/')
        item = ScrapyWkaskciV101Item()
        item['abstract'] = None
        item['title'] = response.meta['title']
        item['paper_url'] = link
        item['date'] = response.meta['date_time']
        item['author'] = None
        item['paper_from'] = response.meta['paper_from']
        item['cleaning_status'] = 0

        file_name = os.path.join(file_path, item['title'] + '.pdf')

        item['parent_id'] = p_id
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
            f.raise_for_status()
            self.logger.info('请求状态码为{},开始下载'.format(f.status_code))

            with open(file_name, 'wb') as file:
                for chunk in f.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
        return


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'wkaskci_V1'])
