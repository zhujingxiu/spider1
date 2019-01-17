# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from crawl58_spider.items import Crawl58SpiderItem
import base64
import re
from fontTools.ttLib import TTFont
from io import BytesIO


class BjzhufangSpider(CrawlSpider):
    name = 'bjzhufang'
    crypt_font = []
    # allowed_domains = ['bj.58.com/chuzu/']
    start_urls = ['https://bj.58.com/chuzu/']
    # redis_key = 'bjzhufang'
    # 链接提取器
    link = LinkExtractor(allow=r'pn(\d+)?/')
    rules = (
        # 规则解析器
        # callback： 指定解析回调
        # follow: 是否将链接提取器继续作用在提取出的链接页面中
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        page_info = {}
        script_text = response.xpath('//head/script[6]/text()').extract_first()
        if script_text:
            self.make_font(script_text)

        li_list = response.xpath('//div[@class="mainbox"]/div/div[@class="content"]/div[@class="listBox"]/ul/li')
        print(response.url, len(li_list))
        for i, li_item in enumerate(li_list, 1):
            renting_info = Crawl58SpiderItem()
            image = li_item.xpath('./div[@class="img_list"]/a/img/@src').extract_first().strip()
            title = li_item.xpath('./div[@class="des"]/h2/a/text()').extract_first().strip()
            building = li_item.xpath('./div[@class="des"]/p[@class="room"]/text()').extract_first().strip()
            address = li_item.xpath('./div[@class="des"]/p[@class="add"]/text()').extract_first().strip()
            source = li_item.xpath('./div[@class="des"]/div[@class="jjr"]/span[@class="jjr_par"]/text()').extract_first().strip()
            money = li_item.xpath('./div[3]/div[2]/b/text()').extract_first().strip()
            info = {
                'img': image,
                'title': self.parse_crypt_text(title),
                'building': self.parse_crypt_text(building),
                'addr': self.parse_crypt_text(address),
                'source': source,
                'money': self.parse_crypt_text(money),
            }
            renting_info['title'] = self.parse_crypt_text(title)
            renting_info['building'] = self.parse_crypt_text(building)
            renting_info['address'] = self.parse_crypt_text(address)
            renting_info['source'] = self.parse_crypt_text(source)
            renting_info['money'] = self.parse_crypt_text(money)
            print(i, info)
        return page_info

    def make_font(self, script_text):
        base64_text = re.findall("src:url\('.*charset=utf-8;base64,(.*)'\) format", script_text)[0]
        if not base64_text:
            return False
        font = TTFont(BytesIO(base64.decodebytes(base64_text.encode())))

        # 转换格式
        self.crypt_font = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap

    def parse_crypt_text(self, string):
        ret_list = []
        for char in string:
            decode_str = ord(char)
            if decode_str in self.crypt_font:
                crypt_str = self.crypt_font[decode_str]
                real_str = str(int(crypt_str[-2:]) - 1)
            else:
                real_str = char
            ret_list.append(real_str)
        return ''.join(ret_list)
