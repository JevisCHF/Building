# -*- coding: utf-8 -*-
import scrapy
import re
import time
from Scrapy_CCbuild_V1.items import ScrapyCcbuildV1Item
from scrapy.utils import request
from Scrapy_CCbuild_V1.start_urls import urls_48
from lxml import etree


class ScrapyCcbuildV1Spider(scrapy.Spider):
    name = 'Scrapy_ccBuild_V3'
    allowed_domains = ['www.ccbuild.com']
    base_url = 'http://www.ccbuild.com/'

    # start_urls = ['http://www.ccbuild.com/']

    def start_requests(self):
        for c, u in urls_48.items():
            cs = c.split('-')
            for i in range(int(cs[2])):
                url = u + str(i + 1)
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                     meta={'information_categories': cs[1], 'industry_categories': cs[0]})

    def parse(self, response):
        industry_categories = response.meta['industry_categories']
        config_list = response.xpath('//div[@class="list_new"]/div')
        for config in config_list:
            item = ScrapyCcbuildV1Item()
            link = config.xpath('./div/div[@class="new_body"]/h2/a/@href').extract_first()
            title = config.xpath('./div/div[@class="new_body"]/h2/a/text()').extract_first()
            issue_time = config.xpath('./div/div[@class="new_body"]/div[@class="meta"]/span/text()').extract_first()
            if issue_time:
                issue_time = re.search(r'(.+) ', issue_time).group(1)

            title_images = config.xpath('./div/div[@class="new_pic"]/div/img/@src').extract_first()
            if title_images:
                title_images = self.base_url + title_images
            # print(link, title, title_images)

            req = scrapy.Request(url=link, callback=self.parse_peple, dont_filter=True, meta={'item': item})

            item['content_url'] = link
            item['id'] = request.request_fingerprint(req)
            item['title_images'] = title_images
            item['issue_time'] = issue_time if issue_time else None
            item['tags'] = None
            item['title'] = title
            item['information_categories'] = response.meta['information_categories']

            item['industry_categories'] = 'E'
            item['industry_Lcategories'] = industry_categories
            item['industry_Mcategories'] = None
            item['industry_Scategories'] = None
            # print(item)
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

        item['source'] = '建筑时空'
        item['content'] = content
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '建筑时空'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['author'] = author if author else None
        # print(item)
        if content:
            yield item
            self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'Scrapy_ccBuild_V3'])
