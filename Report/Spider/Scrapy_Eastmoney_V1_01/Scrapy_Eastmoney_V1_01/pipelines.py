# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, scrapy, os, logging, time
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)
from Scrapy_Eastmoney_V1_01.settings import FILES_STORE


class MongoPipeline(object):
    # collection_name = 'Building_Report'
    collection_name = '111'


    def __init__(self, mongo_uri, mongo_DB):
        self.mongo_uri = mongo_uri
        self.mongo_DB = mongo_DB

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_DB=crawler.settings.get('MONGO_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.DB = self.client[self.mongo_DB]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.DB[self.collection_name].update({'paper_url': item['paper_url']}, {'$set': item}, True)
        return item


class MyFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['paper_url'])

    def file_path(self, request, response=None, info=None):
        # 重命名模块
        path = os.path.join(FILES_STORE, response.meta.get("pcate") + request.url[-10:])

        logger.info("file_path:{}".format(response.meta.get("ctitle")))
        return path
