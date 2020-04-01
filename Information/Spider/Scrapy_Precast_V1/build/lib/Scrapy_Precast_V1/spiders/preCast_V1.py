# -*- coding: utf-8 -*-
import scrapy
import re
import json
from Scrapy_Precast_V1.items import ScrapyPrecastV1Item
import time
from scrapy.utils import request
from Scrapy_Precast_V1.start_urls import url1


class PrecastV1Spider(scrapy.Spider):
    name = 'preCast_V1'
    # allowed_domains = ['www.precast.com']
    # start_urls = ['http://www.precast.com/']
    base_url = 'http://www.precast.com.cn'

    def start_requests(self):
        for c, u in url1.items():
            cs = c.split('-')
            for i in range(int(cs[2])):

                url = f'{u}{i + 1}'
                req = scrapy.Request(url=url, callback=self.parse, meta={'industry_Lcategories': cs[0], 'information_categories': cs[1]})
                yield req

    def parse(self, response):
        config_list = response.xpath('//div[@class="zx-d z clearfix"]/div[@class="box"]')
        # print(len(config_list))
        if config_list:
            for con in config_list:
                item = ScrapyPrecastV1Item()
                title = con.xpath('./a[@class="p1"]/text()').extract_first()
                link = self.base_url + con.xpath('./a[@class="p1"]/@href').extract_first()

                # print(title, link)

                req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

                item['id'] = request.request_fingerprint(req)
                item['title'] = title
                item['title_images'] = None
                item['tags'] = None
                item['author'] = None
                item['industry_categories'] = 'E'
                item['industry_Lcategories'] = response.meta['industry_Lcategories']
                item['industry_Mcategories'] = None
                item['industry_Scategories'] = None
                item['information_categories'] = response.meta['information_categories']
                item['content_url'] = link

                yield req

        ul_list = response.xpath('//ul[@class="zxd-ul"]/li')
        # print(len(ul_list))
        if ul_list:
            for li in ul_list:
                item = ScrapyPrecastV1Item()
                title = li.xpath('./a/text()').extract_first()
                link = self.base_url + li.xpath('./a/@href').extract_first()

                req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

                item['id'] = request.request_fingerprint(req)
                item['title'] = title
                item['title_images'] = None
                item['tags'] = None
                item['author'] = None
                item['industry_categories'] = 'E'
                item['industry_Lcategories'] = response.meta['industry_Lcategories']
                item['industry_Mcategories'] = None
                item['industry_Scategories'] = None
                item['information_categories'] = response.meta['information_categories']
                item['content_url'] = link

                yield req

    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@class="box1"]').extract_first()
        images = response.xpath('//div[@class="box1"]//img/@src').extract()
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

        issue_time = response.xpath('//div[@class="title-box"]/p[1]/text()').extract_first()
        source = response.xpath('//div[@class="title-box"]/p[2]/a[last()]/text()').extract_first()

        item['issue_time'] = issue_time.replace('年', '-').replace('月', '-').replace('日', '') if issue_time else None
        item['source'] = source if source else '预制建设网'
        item['information_source'] = '预制建设网'
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
    cmdline.execute(['scrapy', 'crawl', 'preCast_V1'])
