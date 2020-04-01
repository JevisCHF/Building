# -*- coding: utf-8 -*-
import scrapy, re
from Scrapy_Cacem_V1_01.items import ScrapyCacemV101Item
import time
from scrapy.utils import request
from Scrapy_Cacem_V1_01.start_urls import urls


class CacemV1Spider(scrapy.Spider):
    name = 'cacem_V1'
    # allowed_domains = ['cacem.com.cn']
    # start_urls = ['http://123/']
    base_url = 'http://cacem.com.cn'

    def start_requests(self):
        n = 1

        for url, cate in urls.items():

            page = cate[8:]
            # print(page)

            a = int(page)

            if n == 1:
                # isFirst 判断是不是首页
                yield scrapy.Request(url='http://cacem.com.cn/n178/index.html', callback=self.parse,
                                     meta={'cate': cate[3:7], 'industry_Lcategories': cate[:2], 'isFirst': 1},
                                     dont_filter=True)
                yield scrapy.Request(url='http://cacem.com.cn/n179/index.html', callback=self.parse,
                                     meta={'cate': cate[3:7], 'industry_Lcategories': cate[:2], 'isFirst': 1},
                                     dont_filter=True)
                n += 1

            for i in range(1, int(page)):
                a = a - 1

                link = url.replace(url[-6:-4], f'{a}.')

                yield scrapy.Request(url=link, callback=self.parse,
                                     meta={'cate': cate[3:7], 'industry_Lcategories': cate[:2], 'isFirst': 0},
                                     dont_filter=True)
                self.logger.info("cate({})".format(cate[3:7]))

    def parse(self, response):

        cate = response.meta['cate']
        industry_Lcategories = response.meta['industry_Lcategories']
        isFirst = response.meta['isFirst']

        # print(cate)

        if isFirst:
            # print(isFirst)
            config_list = response.xpath('//div[@class="common_bd"]/span[@id="comp_335"]/ul/li')

            for config in config_list:
                # print(1)
                item = ScrapyCacemV101Item()
                # title_img = config.xpath('./a/img/@src').extract_first()
                # title = config.xpath('./a/text()').extract_first()
                link = self.base_url + config.xpath('./a/@href').extract_first().replace('..', '')
                issue_time = config.xpath('.//span[@class="date_item_list"]/text()').extract_first().strip()
                # print(issue_time)

                # item['title'] = title
                item['issue_time'] = issue_time
                item['content_url'] = link
                item['information_categories'] = cate
                item['title_images'] = None
                # print(item)

                req = scrapy.Request(url=link, callback=self.parse2,
                                     meta={'item': item, 'industry_Lcategories': industry_Lcategories},
                                     dont_filter=True)
                item['id'] = request.request_fingerprint(req)

                yield req
        else:
            # print(isFirst)

            config_list = response.xpath('//div[@class="common_bd"]/ul/li')

            for config in config_list:
                # print(config)

                item = ScrapyCacemV101Item()
                # title_img = config.xpath('./a/img/@src').extract_first()
                # title = config.xpath('./h3/a/text()').extract_first()
                link = self.base_url + config.xpath('./a/@href').extract_first().replace('..', '')
                issue_time = config.xpath('.//span[@class="date_item_list"]/text()').extract_first().strip()

                # print(issue_time)

                # item['title'] = title
                item['issue_time'] = issue_time
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
        content = response.xpath('//div[@class="article_doc"]').extract_first()

        title = response.xpath('//div[@class="article"]/h2/text()').extract_first()
        item['title'] = title

        images = response.xpath('//div[@class="article_doc"]//img/@original').extract()
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
        item['information_source'] = '中国施工企业管理协会'

        source = response.xpath('//div[@class="article_info"]/text()').extract_first()

        try:
            source = re.search(r'来源：(.+)', source).group(1).strip()
        except:
            source = '中国施工企业管理协会'

        item['source'] = source

        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        # item['images'] = None
        item['author'] = None
        item['content'] = content
        yield item

        self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'cacem_V1'])
