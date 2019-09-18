# -*- coding: utf-8 -*-
import scrapy
from ..items import LinkItem


class PageSpider(scrapy.Spider):
    name = 'page'

    def start_requests(self):
        url = getattr(self, 'url', 'http://example.com')

        yield scrapy.Request(url)

    def parse(self, response: scrapy.http.Response):
        for query in response.css('a'):
            if 'href' in query.attrib:
                yield LinkItem(base=response.url, link=query.attrib['href'])
