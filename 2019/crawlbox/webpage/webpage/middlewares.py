# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import asyncio
from scrapy import signals
from pyppeteer import connect
from pyppeteer.page import Page
from scrapy.http import Request, HtmlResponse


DEFAULT_ARGS = [
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-breakpad',
    '--disable-browser-side-navigation',
    '--disable-client-side-phishing-detection',
    '--disable-default-apps',
    '--disable-dev-shm-usage',
    '--disable-extensions',
    '--disable-features=site-per-process',
    '--disable-hang-monitor',
    '--disable-popup-blocking',
    '--disable-prompt-on-repost',
    '--disable-sync',
    '--disable-translate',
    '--metrics-recording-only',
    '--no-first-run',
    '--safebrowsing-disable-auto-update',
    '--enable-automation',
    '--password-store=basic',
    '--use-mock-keychain',
    '--headless',
    '--hide-scrollbars',
    '--mute-audio',
    '--no-sandbox',
    '--disable-gpu',
]
loop = asyncio.get_event_loop()


class WebpageSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BrowserMiddleware(object):
    def __init__(self):
        # option = webdriver.ChromeOptions()
        # for arg in DEFAULT_ARGS:
        #     option.add_argument(arg)
        # self.browser = webdriver.Remote(
        #     command_executor=ChromeRemoteConnection(
        #         remote_server_addr='http://127.0.0.1:48192',
        #         keep_alive=True
        #     ),
        #     desired_capabilities=option.to_capabilities()
        # )
        base = 'http://127.0.0.1:21218'
        data = requests.get(f'{base}/json/version').json()

        self.browser = loop.run_until_complete(connect(browserWSEndpoint=data['webSocketDebuggerUrl'], logLevel='WARNING'))

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    async def request_url(self, url):
        page: Page = await self.browser.newPage()
        await page.goto(url)
        await asyncio.sleep(5)
        data = await page.content()
        await page.close()
        return data

    def process_request(self, request, spider):
        data = loop.run_until_complete(self.request_url(request.url))

        return HtmlResponse(url=request.url, body=data.encode(), request=request, encoding='utf-8')

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider, reason):
        spider.logger.info('Close browser')
        # self.browser.quit()
