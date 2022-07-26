# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


import aiohttp
import logging


class AuthorizationDownloadMiddleware(object):
    # authorization = 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJhZG1pbjgiLCJleHAiOjE2NTQwOTkyMzksImVtYWlsIjoiIiwib3JpZ19pYXQiOjE2NTQwNTYwMzl9.CQvoTyHG2V2xR9LVKJDYpN3wya1G_9HWVfJcD2Kzvkc'
    #
    # def process_request(self, request, spider):
    #     request.headers['authorization'] = self.authorization

    accountpool_url = 'http://192.168.31.54:6789/antispider7/random'
    logger = logging.getLogger('middleware.authorization')

    async def process_request(self, request, spider):
        async with aiohttp.ClientSession() as client:
            response = await client.get(self.accountpool_url)
            if not response.status == 200:
                return
            credential = await response.text()
            authorization = f'jwt {credential}'
            self.logger.debug(f'set authorization {authorization}')
            request.headers['authorization'] = authorization


class ProxyDownloadMiddleware(object):
    # 代理池地址
    proxypool_url = 'http://192.168.31.54:5555/random'
    logger = logging.getLogger('middlewares.proxy')

    # 异步请求，获取代理，配置settings.py以支持asyncio
    async def process_request(self, request, spider):
        async with aiohttp.ClientSession() as client:
            response = await client.get(self.proxypool_url)
            if not response.status == 200:
                return
            proxy = await response.text()
            self.logger.debug(f'set proxy {proxy}')
            # 设置网络代理
            request.meta['proxy'] = f'http://{proxy}'



