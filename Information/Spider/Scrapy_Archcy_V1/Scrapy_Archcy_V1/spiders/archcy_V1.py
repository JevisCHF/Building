# -*- coding: utf-8 -*-
import scrapy
import re
from Scrapy_Archcy_V1.items import ScrapyArchcyV1Item
import time
from scrapy.utils import request
from Scrapy_Archcy_V1.start_urls import url1


class ArchcyV1Spider(scrapy.Spider):
    name = 'archcy_V1'
    allowed_domains = ['www.archcy.com']
    # start_urls = ['http://www.archcy.com/']
    base_url = 'http://www.archcy.com'

    def start_requests(self):
        for c, u in url1.items():
            cs = c.split('-')

            for i in range(int(cs[2])):
            # for i in range(3):
                url = f'{u}{i + 1}'
                req = scrapy.Request(url=url, callback=self.parse, meta={'industry_Lcategories': cs[0], 'information_categories': cs[1]})

                yield req

    def parse(self, response):
        config_list = response.xpath('//div[@class="mdiv clearfix"]/div/div[@class="clearfix"]')
        for con in config_list:
            item = ScrapyArchcyV1Item()

            title = con.xpath('./div/p[@class="link text2"]/a[@class="postHeader"]/text()').extract_first()
            link = self.base_url + con.xpath('./div/p[@class="link text2"]/a[@class="postHeader"]/@href').extract_first()
            title_iamges = self.base_url + con.xpath('./a/img/@src').extract_first()
            issue_time = con.xpath('./div/p[@class="text3"]/text()').extract_first()
            if issue_time:
                issue_time = issue_time[5:].strip()
            # print(title, title_iamges, issue_time, link)

            req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

            item['id'] = request.request_fingerprint(req)
            item['title'] = title
            item['title_images'] = title_iamges if title_iamges else None
            item['content_url'] = link
            item['issue_time'] = issue_time
            item['industry_categories'] = 'E'
            item['industry_Lcategories'] = response.meta['industry_Lcategories']
            item['industry_Mcategories'] = None
            item['industry_Scategories'] = None
            item['information_categories'] = response.meta['information_categories']

            yield req

    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@class="ti nltext"]').extract_first()

        images = response.xpath('//div[@class="ti nltext"]//img/@src').extract()
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

        item['source'] = '建筑畅言网'
        item['author'] = None
        item['information_source'] = '建筑畅言网'
        item['content'] = content
        item['attachments'] = None
        item['area'] = None
        item['address'] = None
        item['tags'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        # print(item)
        if content:
            yield item
            self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'archcy_V1'])
