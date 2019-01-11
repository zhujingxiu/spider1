# -*- coding: utf-8 -*-
import scrapy
from id97.items import Id97Item

class MovieSpider(scrapy.Spider):
    name = 'movie'
    # allowed_domains = ['www.55xia.com/']
    start_urls = ['http://www.55xia.com/movie/']
    def parse(self, response):
        div_list = response.xpath('/html/body/div[1]/div[1]/div[2]/div')
        for div in div_list:
            title = div.xpath('.//div[@class="meta"]/h1/a/text()').extract_first()
            if not title:
                continue
            url = div.xpath('.//div[@class="meta"]/h1/a/@href').extract_first()
            url = "http:%s" % url
            tag = div.xpath('.//div[@class="otherinfo"]/a/text()').extract()
            tag = ','.join(tag)
            print(title, tag)
            item = Id97Item()
            item['title'] = title
            item['url'] = url
            item['tag'] = tag
            yield scrapy.Request(url=url,callback=self.parseSubPage, meta={'item':item})

    def parseSubPage(self, response):
            item = response.meta['item']
            director = response.xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[2]/text()').extract_first()
            actor = response.xpath('//*[@id="casts"]/text()').extract_first()
            score = response.xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[10]/td[2]/text()').extract_first()

            item['director'] = director
            item['actor'] = actor
            item['score'] = score
            print(item)
            yield item