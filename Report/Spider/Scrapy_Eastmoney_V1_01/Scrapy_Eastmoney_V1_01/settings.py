# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_Eastmoney_V1_01 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_Eastmoney_V1_01'

SPIDER_MODULES = ['Scrapy_Eastmoney_V1_01.spiders']
NEWSPIDER_MODULE = 'Scrapy_Eastmoney_V1_01.spiders'

ROBOTSTXT_OBEY = False

# 文件下载路径
FILES_STORE = 'E:\\报告\\爬虫\\建筑行业\\Building Report'

# 环保工程 工程建设 水泥建材 装修装饰
CATES_DICT = {

    # kye(id, menu), value(页数)
    '5002-土木工程建筑业': {
        '001-环保工程-29': 'http://reportapi.eastmoney.com/report/list?cb=datatable1567473&industryCode=728&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2018-02-25&endTime=2020-02-25&pageNo=1&fields=&qType=1&orgCode=&rcode=&_=1582619141543',
        '002-工程建设-11': 'http://reportapi.eastmoney.com/report/list?cb=datatable2701604&industryCode=425&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2018-02-25&endTime=2020-02-25&pageNo=1&fields=&qType=1&orgCode=&rcode=&_=1582619141557',
    },

    # '5003-建筑安装业': 1,

    '5004-建筑装饰、装修和其他建筑业': {
        '001-水泥建材-29': 'http://reportapi.eastmoney.com/report/list?cb=datatable4027341&industryCode=424&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2018-02-25&endTime=2020-02-25&pageNo=1&fields=&qType=1&orgCode=&rcode=&_=1582619141559',
        '002-装饰装修-8': 'http://reportapi.eastmoney.com/report/list?cb=datatable6618729&industryCode=725&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2018-02-25&endTime=2020-02-25&pageNo=1&fields=&qType=1&orgCode=&rcode=&_=1582619141561',
    },
}

# 日志文件等级
LOG_LEVEL = 'INFO'

# 重试设置
RETRY_ENABLED = True  # 开始失败重试，默认关闭
RETRY_TIMES = 4
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 404]  # 遇到这一类状态码，重试

# 测试集
MONGO_URI = '127.0.0.1:27017'
MONGO_DB = 'Building_new'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
import random

DOWNLOAD_DELAY = random.uniform(2, 6)
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'Scrapy_WkAskci_V1_01.middlewares.ScrapyWkaskciV101SpiderMiddleware': 543,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'Scrapy_Eastmoney_V1_01.middlewares.AddProxyMiddlewares': 543,
    # 'Scrapy_Eastmoney_V1_01.middlewares.MyRetryMiddleware': 533,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Scrapy_Eastmoney_V1_01.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
