# -*- coding: utf-8 -*-
import re
import scrapy
import traceback
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from crawl58_spider.items import Crawl58SpiderItem, MyItemLoader


class BjzhufangSpider(CrawlSpider):
    name = 'bjzhufang'
    # allowed_domains = ['bj.58.com/chuzu']
    start_urls = ['https://bj.58.com/chuzu/']
    # redis_key = 'bjzhufang:start_urls'
    # 链接提取器
    link = LinkExtractor(allow=r'(pn(\d+)?/)?')
    rules = (
        # 规则解析器
        # callback： 指定解析回调
        # follow: 是否将链接提取器继续作用在提取出的链接页面中
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath('//div[@class="mainbox"]/div/div[@class="content"]/div[@class="listBox"]/ul/li')
        print(response.url, len(li_list))
        for i, li_item in enumerate(li_list, 1):
            detail_url = li_item.xpath('./div[@class="des"]/h2/a/@href').extract_first().strip()
            print('detail_url:>>', detail_url)
            if detail_url:
                yield scrapy.Request(url='https:'+detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        _loader = MyItemLoader(item=Crawl58SpiderItem(), response=response)
        _loader.add_value('proxy', response.meta['proxy'])
        _loader.add_xpath('crypt', '//head/script[1]/text()')
        _loader.add_css('cover', '#smainPic::attr(src)')
        _loader.add_css('title', 'div.house-title h1::text')
        _loader.add_css('price', 'div.house-pay-way span:nth-child(1) b::text')
        _loader.add_css('payment', 'div.house-pay-way span:nth-child(2)::text')
        _loader.add_css('mode', 'div.house-desc-item ul li:nth-child(1) span:nth-child(2)::text')
        _loader.add_css('house', 'div.house-desc-item ul li:nth-child(2) span:nth-child(2)::text')
        _loader.add_css('position', 'div.house-desc-item ul li:nth-child(3) span:nth-child(2)::text')
        _loader.add_css('address', 'span.dz::text')
        _loader.add_css('phone', 'span.house-chat-txt::text')
        _loader.add_css('source', 'p.agent-subgroup::text')
        _loader.add_css('info', 'ul.introduce-item li:nth-child(2) span:nth-child(2)::text')
        _loader.add_css('images', '#housePicList li img::attr(lazy_src)')
        renting_info = _loader.load_item()
        # renting_info = Crawl58SpiderItem()
        # renting_info['proxy'] = response.meta['proxy']
        # renting_info['crypt'] = ''
        # try:
        #     script_text = response.xpath('//head/script[1]/text()').extract_first()
        #     if script_text:
        #         renting_info['crypt'] = re.findall("src:url\('.*charset=utf-8;base64,(.*)'\) format", script_text)[0]
        #     cover = response.css('#smainPic::attr(src)').extract_first()
        #     renting_info['cover'] = cover.strip() if cover else ''
        #     title = response.css('div.house-title h1::text').extract_first()
        #     renting_info['title'] = title.strip() if title else ''
        #     price = response.css('div.house-pay-way span:nth-child(1) b::text').extract_first()
        #     renting_info['price'] = price.strip() if price else ''
        #     payment = response.css('div.house-pay-way span:nth-child(2)::text').extract_first()
        #     renting_info['payment'] = payment.strip() if payment else ''
        #     mode = response.css('div.house-desc-item ul li:nth-child(1) span:nth-child(2)::text').extract_first()
        #     renting_info['mode'] = mode.strip() if mode else ''
        #     house = response.css('div.house-desc-item ul li:nth-child(2) span:nth-child(2)::text').extract_first()
        #     renting_info['house'] = house.strip() if house else ''
        #     position = response.css('div.house-desc-item ul li:nth-child(3) span:nth-child(2)::text').extract_first()
        #     renting_info['position'] = position.strip() if position else ''
        #     address = response.css('span.dz::text').extract_first()
        #     renting_info['address'] = address.strip() if address else ''
        #     phone = response.css('span.house-chat-txt::text').extract_first()
        #     renting_info['phone'] = phone.strip() if phone else ''
        #     source = response.css('p.agent-subgroup::text').extract_first()
        #     renting_info['source'] = source.strip() if source else ''
        #     info = response.css('ul.introduce-item li:nth-child(2) span:nth-child(2)::text').extract_first()
        #     renting_info['info'] = info.strip() if info else ''
        #     house_image = []
        #     image_eles = response.css('#housePicList li')
        #     if image_eles:
        #         for img in image_eles:
        #             _path = img.css('img::attr(lazy_src)').extract_first()
        #             if not _path:
        #                 continue
        #             house_image.append(_path)
        #
        #     renting_info['images'] = house_image
        # except Exception as e:
        #     print(traceback.print_exc(), e)
        yield renting_info

