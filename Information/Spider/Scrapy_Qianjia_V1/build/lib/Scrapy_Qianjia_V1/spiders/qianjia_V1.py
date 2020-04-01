# -*- coding: utf-8 -*-
import scrapy
import re
import json
from Scrapy_Qianjia_V1.items import ScrapyQianjiaV1Item
import time
from scrapy.utils import request
from Scrapy_Qianjia_V1.start_urls import url1


class QianjiaV1Spider(scrapy.Spider):
    name = 'qianjia_V1'
    # allowed_domains = ['www.qianjia.com']
    # start_urls = ['http://www.qianjia.com/']
    base_url = 'http://www.qianjia.com/'

    def start_requests(self):
        for c, u in url1.items():
            cs = c.split('-')
            for i in range(int(cs[2])):
                url = f'{u}{i + 1}'
                req = scrapy.Request(url=url, callback=self.parse, meta={'industry_Lcategories': cs[0], 'information_categories': cs[1]})
                yield req

    def parse(self, response):
        config_list = json.loads(response.text)
        Table = config_list['Data']['Table']
        # print(len(Table))
        for t in Table:
            item = ScrapyQianjiaV1Item()

            title = t['Title']
            title_images = t['TitleImage']
            issue_time = t['DateAndTime']
            link = t['LinkUrl']
            tags = t['LabelName']
            source = t['Source']
            author = t['Author']

            if link:
                req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

                item['id'] = request.request_fingerprint(req)
                item['title'] = title
                item['title_images'] = title_images if title_images else None
                item['issue_time'] = issue_time[:10] if issue_time else None
                item['tags'] = tags if tags else None
                item['source'] = source if source else '千家智能照明网'
                item['author'] = author if author else None
                item['industry_categories'] = 'E'
                item['industry_Lcategories'] = response.meta['industry_Lcategories']
                item['industry_Mcategories'] = None
                item['industry_Scategories'] = None
                item['information_categories'] = response.meta['information_categories']
                item['content_url'] = link

                yield req

    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@class="article-text"]/article').extract_first()
        images = response.xpath('//div[@class="article-text"]/article//img/@src').extract()
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

        item['information_source'] = '千家智能照明网'
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
    cmdline.execute(['scrapy', 'crawl', 'qianjia_V1'])
