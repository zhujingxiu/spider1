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
    cover = scrapy.Field()
    mode = scrapy.Field()
    house = scrapy.Field()
    crypt = scrapy.Field()
    price = scrapy.Field()
    payment = scrapy.Field()
    info = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    position = scrapy.Field()
    source = scrapy.Field()
    images = scrapy.Field()
