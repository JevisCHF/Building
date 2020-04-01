# -*- coding: utf-8 -*-
import scrapy, re
from Scrapy_Mysteel_V1_01.items import ScrapyMysteelV101Item
import time
from scrapy.utils import request
from Scrapy_Mysteel_V1_01.start_urls import urls


class MysteelV1Spider(scrapy.Spider):
    name = 'mySteel_V1'
    allowed_domains = ['news.mysteel.com']
    # start_urls = ['http://123/']
    base_url = 'https://news.mysteel.com'

    def start_requests(self):

        for url, cate in urls.items():

            page = cate[8:]
            # print(page)
            # for i in range(1, 4):
            for i in range(1, int(page)):
                link = url.replace(url[-6:-4], f'{i}.')
                i += 1
                # print(link)

                yield scrapy.Request(url=link, callback=self.parse,
                                     meta={'cate': cate[3:7], 'industry_Lcategories': cate[:2]}, dont_filter=True)
                self.logger.info("cate({})".format(cate[3:7]))

    def parse(self, response):

        cate = response.meta['cate']
        industry_Lcategories = response.meta['industry_Lcategories']
        # print(cate)
        config_list = response.xpath('//ul[@id="news"]/li')

        for config in config_list:
            # print(config)
            issue_time = config.xpath('.//p[@class="date"]/text()').extract_first()
            # print(issue_time)

            if '-' in issue_time:
                item = ScrapyMysteelV101Item()
                # title_img = config.xpath('./a/img/@src').extract_first()
                title = config.xpath('./h3/a/text()').extract_first()
                link = config.xpath('./h3/a/@href').extract_first()
                if 'http' in link:
                    link = link
                else:
                    link = f'https:' + config.xpath('./h3/a/@href').extract_first()
                # print(issue_time)

                item['title'] = title
                item['issue_time'] = issue_time[:10]
                item['content_url'] = link
                item['information_categories'] = cate
                item['title_images'] = None
                # print(item)

                req = scrapy.Request(url=link, callback=self.parse2,
                                     meta={'item': item, 'industry_Lcategories': industry_Lcategories},
                                     dont_filter=True)
                item['id'] = request.request_fingerprint(req)

                yield req

    def parse2(self, response):
        industry_Lcategories = response.meta['industry_Lcategories']
        item = response.meta['item']
        content = response.xpath('//div[@id="text"]').extract_first()

        images = response.xpath('//div[@id="text"]//img/@original').extract()
        if images:
            images_url = []
            for img in images:
                if 'http' in img:
                    images_url.append(img)
                else:
                    image = f'https:{img}'
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
        item['industry_Lcategories'] = industry_Lcategories
        item['industry_Mcategories'] = None
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '我的钢铁网'

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
            item['source'] = '我的钢铁网'

        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        # item['images'] = None
        item['author'] = None
        item['content'] = content
        yield item
        # print(item)
        self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'mySteel_V1'])
