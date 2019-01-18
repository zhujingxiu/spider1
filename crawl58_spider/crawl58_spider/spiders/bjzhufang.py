# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from crawl58_spider.items import Crawl58SpiderItem
import base64
import re
import traceback


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

    # def parse_list(self, response):
    #
    #     renting_info = Crawl58SpiderItem()
    #     image = li_item.xpath('./div[@class="img_list"]/a/img/@src').extract_first().strip()
    #     print('image',image)
    #     title = li_item.xpath('./div[@class="des"]/h2/a/text()').extract_first().strip()
    #     print('title',title)
    #     building = li_item.xpath('./div[@class="des"]/p[1]/text()').extract_first().strip()
    #     print('building:',building)
    #     address = li_item.xpath('./div[@class="des"]/p[2]/a[1]/text()').extract_first().strip()
    #     print('address:',address)
    #
    #     money = li_item.xpath('./div[3]/div[2]/b/text()').extract_first().strip()
    #     print('money',money)
    #     info = {
    #         'img': image,
    #         'title': self.parse_crypt_text(title),
    #         'building': self.parse_crypt_text(building),
    #         'addr': self.parse_crypt_text(address),
    #         'money': self.parse_crypt_text(money),
    #     }
    #     renting_info['title'] = self.parse_crypt_text(title)
    #     renting_info['building'] = self.parse_crypt_text(building)
    #     renting_info['address'] = self.parse_crypt_text(address)
    #     renting_info['money'] = self.parse_crypt_text(money)

    def parse_item(self, response):
        li_list = response.xpath('//div[@class="mainbox"]/div/div[@class="content"]/div[@class="listBox"]/ul/li')
        print(response.url, len(li_list))
        for i, li_item in enumerate(li_list, 1):

            detail_url = li_item.xpath('./div[@class="des"]/h2/a/@href').extract_first().strip()
            if detail_url:
                yield scrapy.Request(url='https:'+detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        renting_info = Crawl58SpiderItem()
        renting_info['crypt'] = ''
        try:
            script_text = response.xpath('//head/script[1]/text()').extract_first()
            if script_text:
                renting_info['crypt'] = re.findall("src:url\('.*charset=utf-8;base64,(.*)'\) format", script_text)[0]
            cover = response.css('#smainPic::attr(src)').extract_first()
            renting_info['cover'] = cover.strip() if cover else ''
            title = response.css('div.house-title h1::text').extract_first()
            renting_info['title'] = title.strip() if title else ''
            price = response.css('div.house-pay-way span:nth-child(1) b::text').extract_first()
            renting_info['price'] = price.strip() if price else ''
            payment = response.css('div.house-pay-way span:nth-child(2)::text').extract_first()
            renting_info['payment'] = payment.strip() if payment else ''
            mode = response.css('div.house-desc-item ul li:nth-child(1) span:nth-child(2)::text').extract_first()
            renting_info['mode'] = mode.strip() if mode else ''
            house = response.css('div.house-desc-item ul li:nth-child(2) span:nth-child(2)::text').extract_first()
            renting_info['house'] = house.strip() if house else ''
            position = response.css('div.house-desc-item ul li:nth-child(3) span:nth-child(2)::text').extract_first()
            renting_info['position'] = position.strip() if position else ''
            address = response.css('span.dz::text').extract_first()
            renting_info['address'] = address.strip() if address else ''
            phone = response.css('span.house-chat-txt::text').extract_first()
            renting_info['phone'] = phone.strip() if phone else ''
            source = response.css('p.agent-subgroup::text').extract_first()
            renting_info['source'] = source.strip() if source else ''
            info = response.css('ul.introduce-item li:nth-child(2) span:nth-child(2)::text').extract_first()
            renting_info['info'] = info.strip() if info else ''
            # renting_info['cover'] = response.xpath('//img[@id="smainPic"]/@src').extract_first()
            # renting_info['title'] = response.xpath('//div[@class="main-wrap"]/div[1]/h1/text()').extract_first()
            # renting_info['price'] = response.xpath('//div[@class="main-wrap"]/div[2]/div[2]/div[1]/div[1]/div/span[1]/b/text()').extract_first()
            # renting_info['payment'] = response.xpath('//div[@class="main-wrap"]/div[2]/div[2]/div[1]/div[1]/div/span[2]/text()').extract_first()
            # renting_info['mode'] = response.xpath('//div[@class="main-wrap"]/div[2]/div[2]/div[1]/div[1]/ul/li[1]/span[2]/text()').extract_first()
            # renting_info['house'] = response.xpath('//div[@class="main-wrap"]/div[2]/div[2]/div[1]/div[1]/ul/li[2]/span[2]/text()').extract_first()
            # renting_info['phone'] = response.xpath('//div[@class="main-wrap"]/div[2]/div[2]/div[2]/div[1]/span/text()').extract_first()
            # renting_info['address'] = response.xpath('//div[@class="main-wrap"]/div[2]/div[2]/div[1]/div[1]/ul/li[6]/span[2]/text()').extract_first()
            # renting_info['info'] = response.xpath('//div[@class="main-wrap"]/div[3]/div[1]/div[2]/ul/li[2]/span[2]/text()').extract_first()
            house_image = []
            image_eles = response.css('#housePicList li')
            if not image_eles:
                for img in image_eles:
                    _path = img.css('img::attr(lazy_src)').extract_first()
                    if not _path:
                        continue
                    house_image.append(_path)

            renting_info['images'] = house_image
        except Exception as e:
            print(traceback.print_exc(), e)
        yield renting_info

