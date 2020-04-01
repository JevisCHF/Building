# -*- coding: utf-8 -*-
import scrapy
import re
import time
from Scrapy_Crcc_V1.items import ScrapyCrccV1Item
from scrapy.utils import request
from Scrapy_Crcc_V1.start_urls import urls
from lxml import etree


class CrccV1Spider(scrapy.Spider):
    name = 'crcc_V1'
    # allowed_domains = ['www.crcc.cn']
    # start_urls = ['http://www.crcc.cn/']
    base_url = 'http://www.crcc.cn'

    # 获取发布文章列表
    def start_requests(self):
        for c, u in urls.items():
            cs = c.split('-')
            form_data = {
                'col': '1',
                'appid': '1',
                'webid': '1',
                'path': '/',
                'columnid': cs[0],
                'sourceContentType': '1',
                'unitid': '12006',
                'webname': '中国铁建股份有限公司',
                'permissiontype': '0',
            }
            for i in range(150):
                startrecord = 1 + i * 120
                enddrecord = (i + 1) * 120

                if enddrecord < int(cs[2]):
                    url = u.replace('startrecord=1&endrecord=120', f'startrecord={startrecord}&endrecord={enddrecord}')
                    req = scrapy.FormRequest(url=url, callback=self.parse, formdata=form_data, meta={'cate': cs[1]})
                    req.headers[
                        'Cookie'] = 'JSESSIONID=F3DA13DF01E13EDDC163B5FC5904ADF2; nS_wcI_5f=' \
                                    '/8yGMn7arWzQoLXGytgXtfPVcGocZfj0PFs6BA==; JSESSIONID=E96F0A9E86825932891F3202FB26DF3C'
                    yield req
                else:
                    url = u.replace('startrecord=1&endrecord=120', f'startrecord={startrecord}&endrecord={cs[2]}')

                    req = scrapy.FormRequest(url=url, callback=self.parse, formdata=form_data, meta={'cate': cs[1]})
                    req.headers[
                        'Cookie'] = 'JSESSIONID=F3DA13DF01E13EDDC163B5FC5904ADF2; nS_wcI_5f=' \
                                    '/8yGMn7arWzQoLXGytgXtfPVcGocZfj0PFs6BA==; JSESSIONID=E96F0A9E86825932891F3202FB26DF3C'
                    yield req
                    return

    # 处理返回信息，提取文章详情链接：http://www.crcc.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=60&perpage=20
    def parse(self, response):
        config = re.findall(r'<recordset>(.+)</recordset>', response.text)[0]
        lis = config.replace(r'<record><![CDATA[', '').replace(r']]></record>', '')
        html = etree.HTML(lis)
        li = html.xpath('//li')
        # print(len(li))
        for i in range(len(li) - 1):
            issue_time = li[i].xpath('./span/text()')[0]
            link = li[i].xpath('./a/@href')[0]
            title = li[i].xpath('./a/text()')[0]
            # print(link)
            # 国务院
            if ('www.sasac.gov.cn' in link) and ('content' in link):
                item = ScrapyCrccV1Item()
                # print(link)

                item['content_url'] = link
                req = scrapy.Request(url=link, callback=self.parse2, meta={'item': item})
                item['id'] = request.request_fingerprint(req)
                item['issue_time'] = issue_time
                item['information_categories'] = response.meta['cate']
                yield req

            # 中国铁建
            elif 'art' in link:
                item = ScrapyCrccV1Item()
                url = self.base_url + link
                req = scrapy.Request(url=url, callback=self.parse4, meta={'item': item})
                item['content_url'] = url

                item['id'] = request.request_fingerprint(req)
                item['issue_time'] = issue_time
                item['information_categories'] = response.meta['cate']

                yield req

    # 处理title函数
    def merge(self, data):
        a = ''
        for i in data:
            a += i.strip()
        return a

    # 国务院的文章详情
    def parse2(self, response):
        base_url = 'http://www.sasac.gov.cn'
        item = response.meta['item']
        content = response.xpath('//div[@class="zsy_comain"]').extract_first()
        cotitle = response.xpath('//div[@class="zsy_cotitle"]/text()').extract()
        title = self.merge(cotitle)
        source = response.xpath('//div[@class="zsy_cotitle"]/p/text()').extract_first()
        item['source'] = re.search(r'文章来源：(.+)发布时间', source).group(1).strip()

        images = response.xpath('//div[@class="zsy_comain"]//img/@src').extract()
        if images:
            images_url = []
            for img in images:
                if 'http' in img:
                    images_url.append(img)
                else:
                    img = img.replace('../../..', '')
                    image = f'{base_url}{img}'
                    images_url.append(image)
            images_urls = '; '.join(images_url)
            item['images'] = images_urls if images_urls else None
        else:
            item['images'] = None

        item['content'] = content
        item['tags'] = None
        item['industry_categories'] = 'E'
        item['industry_Lcategories'] = '48'
        item['industry_Mcategories'] = '481'
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '中国铁建股份有限公司'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['title'] = title
        item['title_images'] = None
        item['author'] = None
        # print(item)
        if content:
            yield item
            self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))

    # 中国铁建的文章详情
    def parse4(self, response):
        # pass
        item = response.meta['item']
        content = response.xpath('//div[@id="zoom"]').extract_first()
        title = response.xpath('//div[@class="article_title"]/h1/text()').extract_first()
        source1 = response.xpath('////div[@class="source"]/p/span[1]/text()').extract()
        author1 = response.xpath('//div[@class="source"]/p/span[2]/text()').extract()
        source2 = self.merge(source1)
        author2 = self.merge(author1)

        item['source'] = source2[3:] if source2 else None
        if '本站原创' in item['source']:
            item['source'] = '中国铁建股份有限公司'
        item['author'] = author2[3:] if author2 else None

        # print(source2, author2)
        # print('中国铁建', title, author)

        images = response.xpath('//div[@id="zoom"]//img/@src').extract()
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

        item['content'] = content
        item['tags'] = None
        item['industry_categories'] = 'E'
        item['industry_Lcategories'] = '48'
        item['industry_Mcategories'] = '481'
        item['industry_Scategories'] = None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '中国铁建股份有限公司'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['title'] = title
        item['title_images'] = None
        if content:
            yield item
            self.logger.info("title({}), issue_time({})".format(item['title'], item['issue_time']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'crcc_V1'])
