# -*- coding: utf-8 -*-
import scrapy
import re
import json
from Scrapy_Zgazxxw_V1.items import ScrapyZgazxxwV1Item
import time
from scrapy.utils import request
from Scrapy_Zgazxxw_V1.start_urls import url1


class ZgazxxwV1Spider(scrapy.Spider):
    name = 'zgazxxw_V1'
    allowed_domains = ['www.zgazxxw.com']
    # start_urls = ['http://www.zgazxxw.com/']
    base_url = 'http://www.zgazxxw.com'

    def start_requests(self):
        for c, u in url1.items():
            cs = c.split('-')
            for i in range(int(cs[2])):

                if i == 0:
                    url = f'{u}index.html'
                    req = scrapy.Request(url=url, callback=self.parse, meta={'industry_Lcategories': cs[0], 'information_categories': cs[1]})
                    yield req
                else:
                    url = f'{u}index_{i + 1}.html'
                    req = scrapy.Request(url=url, callback=self.parse, meta={'industry_Lcategories': cs[0], 'information_categories': cs[1]})
                    req.headers['referer'] = 'http://www.zgazxxw.com/news/gszx/index.html'
                    yield req

    def parse(self, response):
        # print(response.text)
        config_list = response.xpath('//div[@class="w_list fl"]/div[@class="list_con zx_marb"]')
        # print(len(config_list))

        for con in config_list:
            item = ScrapyZgazxxwV1Item()
            issue_time = con.xpath('./p[@class="fr"]/text()').extract_first()
            title = con.xpath('./p[@class="lt_title fl zx"]/a[last()]/text()').extract_first()
            title_images = None
            link = con.xpath('./p[@class="lt_title fl zx"]/a[last()]/@href').extract_first()

            # print(title, link, issue_time)

            if link:
                link = self.base_url + link
                # print(link)
                req = scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})
                item['id'] = request.request_fingerprint(req)
                item['title'] = title
                item['title_images'] = title_images if title_images else None
                item['issue_time'] = issue_time[:10] if issue_time else None
                item['tags'] = None
                item['source'] = '安装信息网'
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
        content = response.xpath('//div[@class="zhengwen"]').extract_first()
        images = response.xpath('//div[@class="zhengwen"]//img/@src').extract()
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

        item['information_source'] = '安装信息网'
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
    cmdline.execute(['scrapy', 'crawl', 'zgazxxw_V1'])
