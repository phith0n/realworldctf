# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis


class WebpagePipeline(object):
    def __init__(self, redis_url):
        self.redis_url = redis_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(redis_url=crawler.settings.get('REDIS_URL'))

    def open_spider(self, spider):
        self.redis = redis.from_url(self.redis_url)

    def close_spider(self, spider):
        self.redis.close()

    def process_item(self, item, spider):
        self.redis.sadd(item['base'], item['link'])
        return item
