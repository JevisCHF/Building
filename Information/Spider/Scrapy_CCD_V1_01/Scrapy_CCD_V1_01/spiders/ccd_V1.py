# -*- coding: utf-8 -*-
import scrapy, re
from Scrapy_CCD_V1_01.items import ScrapyCcdV101Item
import time
from scrapy.utils import request
from Scrapy_CCD_V1_01.start_urls import urls
from Scrapy_CCD_V1_01.settings import DOWNLOAD_DELAY


class CcdV1Spider(scrapy.Spider):
    name = 'ccd_V1'
    allowed_domains = ['news.ccd.com.cn']
    # start_urls = ['http://123/']
    base_url = 'http://news.ccd.com.cn/'

    def start_requests(self):

        for url, cate in urls.items():
            page = cate[4:]
            for i in range(1, 4):
            # for i in range(1, int(page)):
                link = url.replace(url[-7:-5], f'{i}.')
                i += 1
                print(DOWNLOAD_DELAY)
                print(link)

                yield scrapy.Request(url=link, callback=self.parse, meta={'cate': cate[:4]}, dont_filter=True, )
                self.logger.info("cate({})".format(cate[:4]))
                # time.sleep(30)

    def parse(self, response):
        # DOWNLOAD_DELAY = 1
        cate = response.meta['cate']

        config_list = response.xpath('//div[@class="channel-left"]/ul/li')

        for config in config_list:
            item = ScrapyCcdV101Item()
            # title_img = config.xpath('./div[@class="left"]/a/img/@src').extract_first()
            title = config.xpath('./span[@class="list-con"]/a/text()').extract_first()
            link = config.xpath('./span[@class="list-con"]/a/@href').extract_first()
            issue_time = config.xpath(
                './span[@class="list-date"]/text()').extract_first()
            # tags = config.xpath('./div[@class="right"]/ul/li/a/text()').extract()

            item['title'] = title
            item['issue_time'] = issue_time
            item['content_url'] = link
            item['information_categories'] = cate
            item['title_images'] = None
            print(item)
            DOWNLOAD_DELAY = 1
            req = scrapy.Request(url=link, callback=self.parse2,
                                 meta={'item': item},
                                 dont_filter=True)
            item['id'] = request.request_fingerprint(req)

            yield req

    def parse2(self, response):
        print(1)
        # item = response.meta['item']
        # content = response.xpath('//div[@class="info_content"]').extract_first()
        #
        # images = response.xpath('//div[@class="info_content"]//img/@src').extract()
        # if images:
        #     images_url = []
        #     for img in images:
        #         if 'http' in img:
        #             images_url.append(img)
        #         else:
        #             image = f'{self.base_url}{img}'
        #             images_url.append(image)
        #     images_urls = '; '.join(images_url)
        #     item['images'] = images_urls if images_urls else None
        # else:
        #     item['images'] = None
        #
        # item['tags'] = None
        #
        # item['industry_categories'] = 'E'
        # item['industry_Lcategories'] = None
        # item['industry_Mcategories'] = None
        # item['industry_Scategories'] = None
        # item['sign'] = '19'
        # item['update_time'] = str(int(time.time() * 1000))
        # item['information_source'] = '土木商易宝'
        #
        # source1 = response.xpath('//div[@class="info_title"]/span[2]/a/text()').extract_first().strip()
        # item['source'] = source1 if source1 else '土木商易宝'
        #
        # item['area'] = None
        # item['address'] = None
        # item['attachments'] = None
        # # item['images'] = None
        #
        # author = response.xpath('//div[@class="info_title"]/span[3]/text()').extract_first()[3:].strip()
        # item['author'] = author
        # item['content'] = content
        # yield item
        # print(item)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'ccd_V1'])
