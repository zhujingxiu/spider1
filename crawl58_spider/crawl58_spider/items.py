# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawl58SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    building = scrapy.Field()
    address = scrapy.Field()
    source = scrapy.Field()
    money = scrapy.Field()
