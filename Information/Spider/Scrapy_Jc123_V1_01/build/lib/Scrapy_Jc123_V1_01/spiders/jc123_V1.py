# -*- coding: utf-8 -*-
import scrapy, re
from Scrapy_Jc123_V1_01.items import ScrapyJc123V101Item
import time
from scrapy.utils import request
from Scrapy_Jc123_V1_01.start_urls import urls

class Jc123V1Spider(scrapy.Spider):
    name = 'jc123_V1'
    allowed_domains = ['www.jc123.com.cn/']
    # start_urls = ['http://123/']
    base_url = 'http://www.jc123.com.cn/'

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

        config_list = response.xpath('//div[@class="catlist"]/ul/li')
        m = [6, 12, 18, 24]
        n = 1
        for config in config_list:
            # print(config)
            if n not in m:
                item = ScrapyJc123V101Item()
                # title_img = config.xpath('./a/img/@src').extract_first()
                title = config.xpath('./a/text()').extract_first()
                link = config.xpath('./a/@href').extract_first()
                issue_time = config.xpath('./span/text()').extract_first()[:10]

                item['title'] = title
                item['issue_time'] = issue_time
                item['content_url'] = link
                item['information_categories'] = cate
                item['title_images'] = None
                # print(item)

                req = scrapy.Request(url=link, callback=self.parse2,
                                     meta={'item': item},
                                     dont_filter=True)
                item['id'] = request.request_fingerprint(req)
                # print(time, title, link)
                yield req
            n += 1

    def parse2(self, response):

        item = response.meta['item']
        content = response.xpath('//div[@id="article"]').extract_first()

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

        # key_word = response.xpath('//div[@class="keyword"]/ul/li/a/text()').extract()
        # tags = ';'.join(key_word)
        # item['tags'] = tags if tags else None

        item['tags'] = None
        item['industry_categories'] = 'E'
        item['industry_Lcategories'] = '50'
        item['industry_Mcategories'] = '501'
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '建筑材料网'

        # source1 = response.xpath('//div[@class="detail"]/ul/li[@class="fl"]/text()').extract()[1].strip()
        # source2 = re.search(r'来源：(.+)', source1).group(1).strip()
        item['source'] = '建筑材料网'

        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        # item['images'] = None
        item['author'] = None
        item['content'] = content
        yield item
        # print(item)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'jc123_V1'])