# -*- coding: utf-8 -*-
import scrapy, re
from Scrapy_100njz_V1_01.items import Scrapy100NjzV101Item
import time
from scrapy.utils import request
from Scrapy_100njz_V1_01.start_urls import urls


class A100njzV1Spider(scrapy.Spider):
    name = '100njz_V1'
    allowed_domains = ['www.100njz.com']
    # start_urls = ['http://123/']
    base_url = 'http://www.100njz.com'

    def start_requests(self):

        for url, cate in urls.items():

            page = cate[4:]
            # for i in range(1, 4):
            for i in range(1, int(page)):
                link = url.replace(url[-6:-4], f'{i}.')
                i += 1
                # print(link)

                yield scrapy.Request(url=link, callback=self.parse, meta={'cate': cate[:4]}, dont_filter=True)
                self.logger.info("cate({})".format(cate[:4]))

    def parse(self, response):

        cate = response.meta['cate']

        config_list = response.xpath('//ul[@id="list"]/li')

        for config in config_list:
            # print(config)
            link = config.xpath('./h3/a/@href').extract_first()
            if 'http' in link:
                item = Scrapy100NjzV101Item()
                # title_img = config.xpath('./a/img/@src').extract_first()
                title = config.xpath('./h3/a/text()').extract_first()
                # issue_time = config.xpath('./p[@class="date"]/text()').extract()[1][:10]
                # print(issue_time)

                item['title'] = title
                # item['issue_time'] = issue_time
                item['content_url'] = link
                item['information_categories'] = cate
                item['title_images'] = None
                # print(item)

                req = scrapy.Request(url=link, callback=self.parse2,
                                     meta={'item': item},
                                     dont_filter=True)
                item['id'] = request.request_fingerprint(req)

                yield req

    def parse2(self, response):

        item = response.meta['item']
        content = response.xpath('//div[@id="text"]').extract_first()

        images = response.xpath('//div[@id="text"]//img/@original').extract()
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

        # key_word = response.xpath('//div[@class="keyword"]/ul/li/a/text()').extract()
        # tags = ';'.join(key_word)
        # item['tags'] = tags if tags else None

        item['tags'] = None
        item['industry_categories'] = 'E'
        item['industry_Lcategories'] = '48'
        item['industry_Mcategories'] = None
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '百年建筑'

        source1 = response.xpath('//div[@class="article-infor"]/span[@class="source"]/a/text()').extract_first()
        try:
            source2 = response.xpath('//div[@class="article-infor"]/span[@class="source"]/text()').extract_first()[
                      3:].strip()
        except:
            source2 = None

        if source1:
            item['source'] = source1
        elif source2:
            item['source'] = source2
        else:
            item['source'] = None

        issue_time = response.xpath('//div[@class="article-infor"]/span[@class="upDate"]/text()').extract_first()[:10]
        item['issue_time'] = issue_time

        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        # item['images'] = None
        item['author'] = None
        item['content'] = content

        if content:
            yield item
            self.logger.info(
                "title({}), issue_time({}), url({})".format(item['title'], item['issue_time'], item['content_url']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', '100njz_V1'])
