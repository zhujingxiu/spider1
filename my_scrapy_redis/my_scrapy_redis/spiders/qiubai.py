# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

class QiubaiSpider(RedisCrawlSpider):
    name = 'qiubai'
    # allowed_domains = ['www.qiushibaike.com']
    # start_urls = ['https://www.qiushibaike.com/']
    # 调度器队列
    redis_key = 'qiubai_spider'
    link = LinkExtractor(allow=r'Items/')
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
