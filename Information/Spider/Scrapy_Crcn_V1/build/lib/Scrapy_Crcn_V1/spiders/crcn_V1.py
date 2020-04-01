# -*- coding: utf-8 -*-
import scrapy
import re
import time
from Scrapy_Crcn_V1.items import ScrapyCrcnV1Item
from scrapy.utils import request


class CrcnV1Spider(scrapy.Spider):
    name = 'crcn_V1'
    allowed_domains = ['www.crcn.com.cn']
    # start_urls = ['http://www.crcn.com.cn//']
    base_url = 'http://www.crcn.com.cn'
    month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    # 获取发布文章的年月日
    def start_requests(self):
        # a = 2007
        for n in range(2008, 2010):
            # year = self.base_url[28:32]
            # month = self.base_url[33:35]
            # a += 1
            for m in self.month:
                url = f'http://www.crcn.com.cn/html/{n}-{m}/period.xml'
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    # 获取文章的列表     http://www.crcn.com.cn/html/2008-01/01/node_1.htm
    def parse(self, response):
        config_list = re.findall(r'<period_date>(.+)</period_date>', response.text)
        for config in config_list:
            configs = config.split('-')
            # url = f'http://www.crcn.com.cn/html/{configs[0]}-{configs[1]}/{configs[2]}/node_1.htm'
            for i in range(1,5):
                url = f'http://www.crcn.com.cn/html/{configs[0]}-{configs[1]}/{configs[2]}/node_{i}.htm'
                req = scrapy.Request(url=url, callback=self.parse2, meta={'issue_date': config, 'url': url})
                yield req


    # 获取文章的详细链接
    def parse2(self, response):
        url = response.meta['url']
        issue_time = response.meta['issue_date']
        config_list = response.xpath('//div[@id="titleList1"]/ul/li')
        for config in config_list:
            item = ScrapyCrcnV1Item()

            title = config.xpath('./a/div/text()').extract_first()
            href = config.xpath('./a/@href').extract_first()
            link = url.replace(url[-10:], href)
            # print(title, url)
            req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

            item['id'] = request.request_fingerprint(req)
            item['title'] = title
            item['content_url'] = link
            item['title_images'] = None
            item['issue_time'] = issue_time

            yield req

    # 获取文章详情
    def parse_detail(self, response):
        item = response.meta['item']

        content = response.xpath('//div[@class="oooot"]').extract_first()
        images = response.xpath('//div[@class="info_content"]//img/@src').extract()
        if images:
            images_url = []
            for img in images:
                if 'http' in img:
                    images_url.append(img)
                else:
                    image = f'{self.base_url}{img}'
                    images_url.append(image)
            images_urls = '; '.join(images_url)
            item['images'] = images_urls if images_urls else None
        else:
            item['images'] = None

        item['content'] = content
        item['tags'] = None
        item['industry_categories'] = 'E'
        item['industry_Lcategories'] = '48'
        item['industry_Mcategories'] = '481'
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '中国铁道建筑报'
        item['source'] = '中国铁道建筑报'
        item['author'] = None
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['information_categories'] = '新闻资讯'
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'crcn_V1'])
