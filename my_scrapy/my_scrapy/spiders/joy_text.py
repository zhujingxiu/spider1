# -*- coding: utf-8 -*-
import scrapy
from my_scrapy.items import MyScrapyItem

class JoyTextSpider(scrapy.Spider):
    name = 'joy_text'
    # allowed_domains = ['www.qiushibaike.com/text']
    start_urls = ['https://www.qiushibaike.com/text/']
    page_num = 1
    # scrapy 集成了xpath的解析接口
    def parse(self, response):
        joy_list = response.xpath('//div[@id="content-left"]/div')
        data = []
        for div in joy_list:
            # author = div.xpath('./div/a[2]/h2/text()').extract()
            # content = div.xpath('.//div[@class="content"]/span/text()').extract()
            author = div.xpath('./div/a[2]/h2/text()').extract_first()
            content = div.xpath('.//div[@class="content"]/span/text()').extract_first()
            # 1. 基于命令存储
            # _article = {
            #     'author': author.strip(),
            #     'content': content.strip(),
            # }
            # data.append(_article)
            # print(_article)
            print(author)
            # 2.基于管道
            item = MyScrapyItem()
            item['author'] = author.strip()
            item['content'] = content.strip()
            yield item
        # return data
        if self.page_num <= 13:
            self.page_num += 1
            url = 'https://www.qiushibaike.com/text/page/%d' % self.page_num
            print('爬取第%d页数据，页面URL：%s'%(self.page_num, url))
            yield scrapy.Request(url=url,callback=self.parse)