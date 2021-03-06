# -*- coding: utf-8 -*-
import scrapy
import re
from Scrapy_9to_V1.items import Scrapy9ToV1Item
import time
from scrapy.utils import request
from Scrapy_9to_V1.start_urls import url2


class ChinaluqiaoV1Spider(scrapy.Spider):
    name = 'chinaLuqiao_V2'
    allowed_domains = ['news.9to.com']
    # start_urls = ['http://news.9to.com/']
    base_url = 'http://news.9to.com/'

    def start_requests(self):
        for c, u in url2.items():
            cs = c.split('-')
            for i in range(int(cs[2])):
                url = u + f'{i + 1}/'
                req = scrapy.Request(url=url, callback=self.parse, meta={'industry_Lcategories': cs[0], 'information_categories': cs[1]})

                yield req

    def parse(self, response):
        config_list = response.xpath('//div[@class="catlist"]/ul/li')
        num = [5, 11, 17, 23]
        for i in range(len(config_list)):
            if i not in num:
                item = Scrapy9ToV1Item()
                link = config_list[i].xpath('./a/@href').extract_first()
                title = config_list[i].xpath('./a/text()').extract_first()
                issue_time = config_list[i].xpath('./i/text()').extract_first()
                # print(title, link, issue_time)
                req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

                item['id'] = request.request_fingerprint(req)
                item['title'] = title
                item['title_images'] = None
                item['content_url'] = link
                item['issue_time'] = issue_time[:10] if issue_time else None
                item['industry_categories'] = 'E'
                item['industry_Lcategories'] = response.meta['industry_Lcategories'][:2]
                item['industry_Mcategories'] = response.meta['industry_Lcategories']
                item['industry_Scategories'] = None
                item['information_categories'] = response.meta['information_categories']

                yield req

    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@id="article"]').extract_first()
        info = response.xpath('//div[@class="info"]/text()').extract_first()
        # print(info)
        source = re.search(r'来源：([^\x00-\xff]+)', info.strip())
        author = re.search(r'作者：(.+)', info.strip())

        item['source'] = source.group(1) if source else '中国路桥网'
        item['author'] = author.group(1).strip() if author else None
        item['information_source'] = '中国路桥网'
        item['content'] = content

        images = response.xpath('//div[@id="article"]//img/@original').extract()
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
    cmdline.execute(['scrapy', 'crawl', 'chinaLuqiao_V2'])
