# -*- coding: utf-8 -*-
import scrapy
import re
import time
from Scrapy_CCbuild_V1.items import ScrapyCcbuildV1Item
from scrapy.utils import request
from Scrapy_CCbuild_V1.start_urls import urls
from lxml import etree


class ScrapyCcbuildV1Spider(scrapy.Spider):
    name = 'Scrapy_ccBuild_V1'
    allowed_domains = ['www.ccbuild.com']
    base_url = 'http://www.ccbuild.com/'
    # start_urls = ['http://www.ccbuild.com/']

    def start_requests(self):
        for c, u in urls.items():
            cs = c.split('-')
            for i in range(int(cs[2])):
                url = u + str(i + 1)
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        config_list = response.xpath('//div[@class="wonderful"]/ul/li')
        for config in config_list:
            item = ScrapyCcbuildV1Item()
            link = config.xpath('./a/@href').extract_first()
            # print(link)
            req = scrapy.Request(url=link, callback=self.parse_peple, dont_filter=True, meta={'item': item})

            item['content_url'] = link
            item['id'] = request.request_fingerprint(req)
            title_images = config.xpath('./a/img/@src').extract_first()
            if title_images:
                if 'http' in title_images:
                    item['title_images'] = title_images
                else:
                    item['title_images'] = self.base_url + title_images
            else:
                item['title_images'] = None

            item['issue_time'] = config.xpath('./a/article/div/span[2]/text()').extract_first()[:9]
            item['tags'] = config.xpath('./a/article/div/span[1]/text()').extract_first()

            yield req

    def parse_peple(self, response):
        content = response.xpath('//td[@id="article_content"]').extract_first()
        title = response.xpath('//div[@class="h hm"]/h1/text()').extract_first()
        author = response.xpath(
            '//div[@id="ct"]/div[@class="mn"]/div[@class="bm vw"]/div[@class="h hm"]/p/a/text()').extract_first()

        item = response.meta['item']

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

        item['information_categories'] = '风云人物'
        item['source'] = '建筑时空'
        item['content'] = content
        item['industry_categories'] = 'E'
        item['industry_Lcategories'] = '47'
        item['industry_Mcategories'] = None
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '建筑时空'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['title'] = title
        item['author'] = author if author else None
        # print(item)
        if content:
            yield item
            self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'Scrapy_ccBuild_V1'])
