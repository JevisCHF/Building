# -*- coding: utf-8 -*-

from scrapy import signals
# from fake_useragent import UserAgent
import logging
import time
import requests
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)


class Proxy():
    def __init__(self):
        self.url = 'http://192.168.0.11:5010/get/'
        self.del_url = "http://192.168.0.11:5010/delete?proxy={}"
        # 网站是http的就改成http，网站是https的就改成https
        self.proxy_header = 'http://'

    def get_proxy(self):
        proxy = self.proxy_header + requests.get(self.url).json().get('proxy', False)
        return proxy

    def del_proxy(self, proxy):
        # 删除代理池的ip，慎用
        requests.get(self.del_url.format(proxy.lstrip(self.proxy_header)))


class AddProxyMiddlewares():
    def __init__(self):
        # 失效代理的集合
        self.invalid_proxy = set()
        self.proxy = Proxy().get_proxy()

    def process_request(self, request, spider):
        # request.meta['HTTP_USER_AGENT'] = UserAgent().chrome
        # 清空无效代理
        if len(self.invalid_proxy) > 10:
            self.invalid_proxy.clear()
        request.meta["proxy"] = self.proxy
        request.meta['downloader_timeout'] = 20
        return None

    def process_response(self, request, response, spider):
        logger.info("responese:{}".format(request.meta))
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            # 获取失效代理并收集,重新获取一个代理
            NgProxy = request.meta['proxy']
            self.invalid_proxy.add(NgProxy)
            self.proxy = Proxy().get_proxy()
            logger.warning('代理中间件响应报错，状态码为 {},请求新的代理 {}'.format(str(response.status), self.proxy))
        return response

    def process_exception(self, request, exception, spider):
        # 进入异常模块，
        NgProxy = request.meta['proxy']

        self.invalid_proxy.add(NgProxy)
        self.proxy = Proxy().get_proxy()
        request.dont_filter = True
        logger.warning('代理中间件异常模块，异常为{}，新的代理为 {},'.format(exception, self.proxy))


class MyRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            logger.warning('返回值异常, 进行重试...')

            with open(str(spider.name) + ".txt", "a") as f:
                f.write(str(request) + "\n")
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            logger.warning('MyRetryMiddleware 连接异常, 加入重试队列...')
            with open(str(spider.name) + ".txt", "a") as f:
                f.write(str(request) + "\n")
            return self._retry(request, exception, spider)
