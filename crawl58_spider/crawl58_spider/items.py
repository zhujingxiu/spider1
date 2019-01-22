# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class MyItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def parse_crypt(value):
    import re
    return re.findall("src:url\('.*charset=utf-8;base64,(.*)'\) format", value)[0]


def return_value(value):
    return value


def json_images(value):
    import json
    return json.dumps(value)


class Crawl58SpiderItem(scrapy.Item):
    # define the fields for your item here like:

    # title = scrapy.Field()
    # cover = scrapy.Field()
    # mode = scrapy.Field()
    # house = scrapy.Field()
    # crypt = scrapy.Field()
    # price = scrapy.Field()
    # payment = scrapy.Field()
    # info = scrapy.Field()
    # phone = scrapy.Field()
    # address = scrapy.Field()
    # position = scrapy.Field()
    # source = scrapy.Field()
    # images = scrapy.Field()
    # proxy = scrapy.Field()

    title = scrapy.Field()
    cover = scrapy.Field()
    mode = scrapy.Field()
    house = scrapy.Field()
    crypt = scrapy.Field(input_processor=MapCompose(parse_crypt))
    price = scrapy.Field()
    payment = scrapy.Field()
    info = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    position = scrapy.Field()
    source = scrapy.Field()
    images = scrapy.Field(input_processor=MapCompose(json_images))
    proxy = scrapy.Field()
