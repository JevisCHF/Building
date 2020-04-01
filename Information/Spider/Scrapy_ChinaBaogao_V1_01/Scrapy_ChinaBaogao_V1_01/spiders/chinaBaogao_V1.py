# -*- coding: utf-8 -*-
import scrapy, re
from Scrapy_ChinaBaogao_V1_01.items import ScrapyChinabaogaoV101Item
import time
from scrapy.utils import request
from Scrapy_ChinaBaogao_V1_01.start_urls import urls


class ChinabaogaoV1Spider(scrapy.Spider):
    name = 'chinaBaogao_V1'
    allowed_domains = ['news.chinabaogao.com/', 'market.chinabaogao.com/', 'zhengce.chinabaogao.com/']
    # start_urls = ['http://123/']
    base_url = 'http://news.chinabaogao.com/'

    def start_requests(self):

        for url, cate in urls.items():
            cates = cate.split('-')
            page = cates[2]
            # for i in range(1, 5):
            for i in range(1, int(page)):
                link = url.replace(url[-6:-4], f'{i}.')
                i += 1
                print(link)

                yield scrapy.Request(url=link, callback=self.parse,
                                     meta={'cate': cates[1], 'industry_Lcategories': cates[0]}, dont_filter=True)
                self.logger.info("cate({})".format(cate[:4]))

    def parse(self, response):
        # pass
        cate = response.meta['cate']

        config_list = response.xpath('//ul[@class="pagelist"]/li')
        # print(len(config_list))
        n = [10, 21, 32]
        m = 0
        for config in config_list:
            # print(config)
            if m not in n:
                # print(m)
                item = ScrapyChinabaogaoV101Item()
                title = config.xpath('./h3/a/text()').extract_first()
                link = config.xpath('./h3/a/@href').extract_first()
                issue_time = config.xpath('./span/text()').extract_first()

                item['title'] = title
                item['issue_time'] = issue_time
                item['content_url'] = link
                item['information_categories'] = cate
                item['title_images'] = None
                # print(item)

                req = scrapy.Request(url=link, callback=self.parse2,
                                     meta={'item': item, 'industry_Lcategories': response.meta['industry_Lcategories']},
                                     dont_filter=True)
                item['id'] = request.request_fingerprint(req)
                yield req
            m += 1

    def parse2(self, response):

        item = response.meta['item']
        content = response.xpath('//div[@id="content-body"]').extract_first()

        images = response.xpath('//div[@id="content-body"]//img/@src').extract()
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
        item['industry_Lcategories'] = response.meta['industry_Lcategories']
        item['industry_Mcategories'] = None
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '中国报告网'

        # source1 = response.xpath('//div[@class="detail"]/ul/li[@class="fl"]/text()').extract()[1].strip()
        # source2 = re.search(r'来源：(.+)', source1).group(1).strip()
        item['source'] = '中国报告网'

        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        # item['images'] = None
        item['author'] = None
        item['content'] = content
        if content:
            yield item
            self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'chinaBaogao_V1'])
