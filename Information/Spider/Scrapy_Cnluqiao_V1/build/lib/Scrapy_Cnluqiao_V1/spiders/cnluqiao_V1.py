# -*- coding: utf-8 -*-
import scrapy
import re
import json
from Scrapy_Cnluqiao_V1.items import ScrapyCnluqiaoV1Item
import time
from scrapy.utils import request
from Scrapy_Cnluqiao_V1.start_urls import url1


class CnluqiaoV1Spider(scrapy.Spider):
    name = 'cnluqiao_V1'
    # allowed_domains = ['123']
    # start_urls = ['http://123/']
    base_url = 'http://www.cnluqiao.com/'

    def start_requests(self):
        for i in range(643):
            url = f'http://www.cnluqiao.com/portal.php?mod=list&catid=1&page={i + 1}'
            req = scrapy.Request(url=url, callback=self.parse)
            yield req

    def parse(self, response):
        config_list = response.xpath('//div[@class="nex_artice"]/ul/li')
        # print(len(config_list))
        if config_list:
            for con in config_list:
                item = ScrapyCnluqiaoV1Item()

                nex_articer = con.xpath('./div[@class="nex_articer"]')
                nex_articer_tl = con.xpath('./div[@class="nex_articer_tl"]')

                if nex_articer:

                    title = con.xpath('./div[@class="nex_articer"]/h5/a/text()').extract_first()
                    link = con.xpath('./div[@class="nex_articer"]/h5/a/@href').extract_first()
                    title_images = con.xpath('.//div[@class="nex_articel"]//img/@src').extract_first()

                    # print(title, link, title_images)

                elif nex_articer_tl:
                    title = con.xpath('.//div[@class="nex_attltop"]/a/text()').extract_first()
                    link = con.xpath('.//div[@class="nex_attltop"]/a/@href').extract_first()
                    title_images = None

                    # print(title, link)

                author = con.xpath('.//div[@class="nex_atctl"]/span/text()').extract_first()
                issue_time = con.xpath('.//div[@class="nex_atmoresd"]/span[1]/text()').extract_first()

                req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

                item['id'] = request.request_fingerprint(req)
                item['title'] = title
                item['title_images'] = title_images
                item['tags'] = None
                item['author'] = author
                item['industry_categories'] = 'E'
                item['industry_Lcategories'] = '48'
                item['industry_Mcategories'] = '481'
                item['industry_Scategories'] = None
                item['information_categories'] = '行业资讯'
                item['content_url'] = link
                item['issue_time'] = issue_time[3:12] if issue_time else None

                yield req

    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath('//td[@id="article_content"]').extract_first()
        images = response.xpath('//td[@id="article_content"]//img/@src').extract()
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

        item['source'] = '路桥技术网'
        item['information_source'] = '路桥技术网'
        item['content'] = content
        item['attachments'] = None
        item['area'] = None
        item['address'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        # print(item)
        if content:
            yield item
            self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'cnluqiao_V1'])
