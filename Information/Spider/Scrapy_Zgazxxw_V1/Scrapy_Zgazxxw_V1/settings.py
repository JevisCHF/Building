# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_Zgazxxw_V1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_Zgazxxw_V1'

SPIDER_MODULES = ['Scrapy_Zgazxxw_V1.spiders']
NEWSPIDER_MODULE = 'Scrapy_Zgazxxw_V1.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_Zgazxxw_V1 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

import random

DOWNLOAD_DELAY = random.uniform(5, 10)

DOWNLOADER_MIDDLEWARES = {
    'Scrapy_Zgazxxw_V1.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_Zgazxxw_V1.middlewares.MyRetryMiddleware': 533,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Scrapy_Zgazxxw_V1.pipelines.MongoPipeline': 301,
}

# 正式集
# MONGO_URI = '192.168.0.11'
# MONGO_DATABASE = 'industry'

# 测试集
MONGO_URI = '127.0.0.1'
MONGO_DATABASE = 'Building_new'

# 日志文件等级
LOG_LEVEL = 'INFO'

# 重试设置
RETRY_ENABLED = True  # 默认开启失败重试，一般关闭
RETRY_TIMES = 3  # 失败后重试次数，默认两次
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]  # 碰到这些验证码，才开启重试
