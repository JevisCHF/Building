# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, datetime, time
import logging

logger = logging.getLogger(__name__)

COLLECTION_NAME = 'Building_data_qianzhan'
# COLLECTION_NAME = '123'


class ScrapyRobodataV102Pipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if self.db[COLLECTION_NAME].count_documents(
                {
                    'indic_name': item['indic_name'],
                    'frequency': item['frequency'],
                    'data_year': item['data_year'],
                    'data_month': item['data_month'],
                    'data_day': item['data_day'],
                    'data_source': item['data_source'],
                    'region': item['region'],
                    'country': item['country'],
                    'data_value': item['data_value'],
                    "create_time": item["create_time"],
                }
        ) == 0:
            self.db[COLLECTION_NAME].insert(dict(item))
            return item['indic_name']
        else:
            err = 'the data is repetition .' + item['indic_name']
            logger.info(err)
            return None
        # self.db[COLLECTION_NAME].insert(dict(item))
        # return item

    def close_spider(self, spider):
        self.client.close()
