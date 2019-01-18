# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import base64
from fontTools.ttLib import TTFont
from io import BytesIO


class Crawl58SpiderPipeline(object):

    def __init__(self):
        self.crypt_list = []
        # self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='pyspider', charset='utf8')
        # self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        script_text = item.get('crypt')
        self.make_font(script_text)
        title = item.get('title')
        price = item.get('price')
        payment = item.get('payment')
        house_type = item.get('type')
        house = item.get('house')
        cover = item.get('cover')
        title = self.parse_crypt_text(title)
        price = self.parse_crypt_text(price)
        house_type = self.parse_crypt_text(house_type)
        print(title,'-',price,'-',payment,'-',house_type,'-',house,'-',cover)
        # sql = "insert info renting58(title,image,building,address,source,money) values(%s, %s,%s,%s,%s,%s,)"
        # self.cur.execute(sql, (item['title']), item['image'], item['building'], item['address'],item['source'],item['money'])
        # self.conn.commit()
        return item
    
    
    def make_font(self, base64_text):
        font = TTFont(BytesIO(base64.decodebytes(base64_text.encode())))

        # 转换格式
        self.crypt_list = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap

    def parse_crypt_text(self, string):
        ret_list = []
        for char in string:
            decode_str = ord(char)
            if decode_str in self.crypt_list:
                crypt_str = self.crypt_list[decode_str]
                real_str = str(int(crypt_str[-2:]) - 1)
            else:
                real_str = char
            ret_list.append(real_str)
        return ''.join(ret_list)

    def close_spider(self, spider):
        pass
        # self.cur.close()
        # self.conn.close()
