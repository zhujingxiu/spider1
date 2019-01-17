# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class Crawl58SpiderPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='pyspider', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "insert info renting58(title,image,building,address,source,money) values(%s, %s,%s,%s,%s,%s,)"
        self.cur.execute(sql, (item['title']), item['image'], item['building'], item['address'],item['source'],item['money'])
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
