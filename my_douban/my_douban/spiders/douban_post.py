# -*- coding: utf-8 -*-
import scrapy


class DoubanPostSpider(scrapy.Spider):
    name = 'douban_post'
    # allowed_domains = ['www.douban.com/']
    start_urls = ['https://www.baidu.com/s?wd=ip']
    # 发起post
    # 1.将scrapy.Request中method参数指定为post
    # 2.使用FormRequest
    def start_requests(self):
        post_data = {
        #     'source': 'index_nav',
        #     'form_email': '18850911766',
        #     'form_password': 'zjx82122',
        }
        for item in self.start_urls:
            # yield scrapy.Request(url=item, callback=self.parse, method='post')
            yield scrapy.FormRequest(url=item, formdata=post_data, callback=self.parse)

    def parse(self, response):
        print(response.text)
