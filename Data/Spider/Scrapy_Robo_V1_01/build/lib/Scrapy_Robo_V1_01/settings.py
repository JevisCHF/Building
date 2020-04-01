# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_Robo_V1_01 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_Robo_V1_01'

SPIDER_MODULES = ['Scrapy_Robo_V1_01.spiders']
NEWSPIDER_MODULE = 'Scrapy_Robo_V1_01.spiders'

ROBOTSTXT_OBEY = False

import random
DOWNLOAD_DELAY = random.uniform(9, 11)
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "Building_new"  # 库名
RETRY_ENABLED = True  # 打开重试开关
RETRY_TIMES = 3  # 重试次数
DOWNLOAD_TIMEOUT = 10  # 超时
RETRY_HTTP_CODES = [503, 500, 502, 404, 400, 403]

SPIDER_MIDDLEWARES = {
    # 'Scrapy_Robo_V1_01.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_RoBoDatabase_V1_15.middlewares.ScrapyRobodatabaseV115SpiderMiddleware': 543,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'Scrapy_Robo_V1_01.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_RoBoDatabase_V1_15.middlewares.ScrapyRobodatabaseV115DownloaderMiddleware': 543,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

}

ITEM_PIPELINES = {
    'Scrapy_Robo_V1_01.pipelines.ScrapyRobodataV102Pipeline': 300,
}

base_url = ['https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=',  # 输入关键字
            # 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=%E7%94%B5%E5%8A%9B&macro=%E8%A1%8C%E4%B8%9A%E7%BB%8F%E6%B5%8E&catelog=2000000001-2020000001-2020000002-2020001492-2020001510',
            'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/',  # 输入编号
            'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=电力&macro=国际宏观&catelog=',
            'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=电力&macro=特色数据&catelog=']

# 关键字爬取列表
cate = {
    # key, value（id，title）
    '房屋建筑': '5001002房屋建筑业',
    '土木工程 海洋工程 水利工程 节能环保 电力工程': '5002002土木工程建筑业',
    '建筑安装': '5003002建筑安装业',
    '建筑装饰 装修 装潢': '5004002建筑装饰、装修和其他建筑业',
}

# 根据萝卜投研的网址分类来爬取
cate2 = {
    # 行业经济
    '4-建材-286116': '5004002建筑装饰、装修和其他建筑业',

    # 公司数据
    '5-建筑材料-RRP243511': '5004002建筑装饰、装修和其他建筑业',
    '6-建筑装饰-RRP272052': '5004002建筑装饰、装修和其他建筑业',

    # 中国宏观
    '2-房地产及建筑业-806114': '5001002房屋建筑业',

    # 国际宏观
    '3-房地产及建筑业-1138921': '5001002房屋建筑业',
}

urls = {}

# 日志等级
LOG_LEVEL = 'INFO'
