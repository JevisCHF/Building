# -*- coding: utf-8 -*-
import scrapy, re
from Scrapy_Biz_V1_01.items import ScrapyBizV101Item
import time
from scrapy.utils import request
from Scrapy_Biz_V1_01.start_urls import urls


class BizV1Spider(scrapy.Spider):
    name = 'biz_V1'
    allowed_domains = ['biz.co188.com']
    # start_urls = ['http://123/']
    base_url = 'http://biz.co188.com'

    def start_requests(self):

        for url, cate in urls.items():
            page = cate[4:]
            # for i in range(1, 4):
            for i in range(1, int(page)):
                link = url.replace(url[-6:-4], f'{i}.')
                i += 1
                print(link)

                yield scrapy.Request(url=link, callback=self.parse, meta={'cate': cate[:4]}, dont_filter=True)
                self.logger.info("cate({})".format(cate[:4]))

    def parse(self, response):

        cate = response.meta['cate']

        config_list = response.xpath('//div[@id="ui_main"]/div')
        a = 1
        for config in config_list:
            # print(config)

            if a < 11:
                item = ScrapyBizV101Item()
                title_img = config.xpath('./div[@class="left"]/a/img/@src').extract_first()
                title = config.xpath('./div[@class="navs_head add_height"]/a/text()').extract_first()
                link = self.base_url + config.xpath('./div[@class="navs_head add_height"]/a/@href').extract_first()
                issue_time = config.xpath('./div[@class="navs_head add_height"]/span[@class="head_right"]/text()').extract_first().replace('年', '-').replace(
                    '月', '-').replace('日', '')
                # tags = config.xpath('./div[@class="right"]/ul/li/a/text()').extract()

                item['title'] = title
                item['issue_time'] = issue_time
                item['content_url'] = link
                item['information_categories'] = cate
                item['title_images'] = title_img if title_img else None
                # print(item)

                req = scrapy.Request(url=link, callback=self.parse2,
                                     meta={'item': item},
                                     dont_filter=True)
                item['id'] = request.request_fingerprint(req)

                yield req
            a += 1

    def parse2(self, response):

        item = response.meta['item']
        content = response.xpath('//div[@class="info_content"]').extract_first()

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

        item['tags'] = None

        item['industry_categories'] = 'E'
        item['industry_Lcategories'] = '48'
        item['industry_Mcategories'] = None
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '土木商易宝'
        try:
            source1 = response.xpath('//div[@class="info_title"]/span[2]/a/text()').extract_first().strip()
        except:
            source1 = None
        item['source'] = source1 if source1 else '土木商易宝'

        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        # item['images'] = None
        try:
            author = response.xpath('//div[@class="info_title"]/span[3]/text()').extract_first()[3:].strip()
        except:
            author = None
        item['author'] = author
        item['content'] = content
        yield item
        # print(item)

        # self.logger.info("information_source({})".format(item['information_source']))

        self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'biz_V1'])
