# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import base64
from fontTools.ttLib import TTFont
from io import BytesIO
import json
import datetime


class Crawl58SpiderPipeline(object):

    def __init__(self):
        self.crypt_list = []
        self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='pyspider', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            proxy = item.get('proxy')
            print(proxy)
            script_text = item.get('crypt')
            self.make_font(script_text)
            cover = item.get('cover')
            title = item.get('title')
            price = item.get('price')
            payment = item.get('payment')
            mode = item.get('mode')
            house = item.get('house')
            position = item.get('position')
            address = item.get('address')
            phone = item.get('phone')
            info = item.get('info')
            source = item.get('source')
            images = item.get('images')

            title = self.parse_crypt_text(title)
            price = self.parse_crypt_text(price)
            mode = self.parse_crypt_text("".join(mode.split()))
            house = self.parse_crypt_text("".join(house.split()))
            position = self.parse_crypt_text("".join(position.split()))
            address = self.parse_crypt_text("".join(address.split()))
            phone = self.parse_crypt_text("".join(phone.split()))
            field = {
                'cover': cover,
                'title': title,
                'price': price,
                'payment': payment,
                'mode': mode,
                'house': house,
                'position': position,
                'address': address,
                'phone': phone if phone.isnumeric() else '',
                'source': source,
                'info': info,
                'images': json.dumps(images),
                'proxy': proxy,
                'addtime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            sql = 'INSERT INTO renting58(%s) VALUES (%s)' \
                  % (', '.join(["`%s`" % str(_key) for _key in field.keys()]),
                     ', '.join(["'%s'" % str(_val) for _val in field.values()]))
            ret = self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        return item

    def make_font(self, base64_text):
        font = TTFont(BytesIO(base64.decodebytes(base64_text.encode())))
        # 转换格式
        self.crypt_list = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap

    def parse_crypt_text(self, string, debug=False):
        ret_list = []
        for char in string:
            decode_str = ord(char)
            if decode_str in self.crypt_list:
                crypt_str = self.crypt_list[decode_str]
                real_str = str(int(crypt_str[-2:]) - 1)
            else:
                real_str = char
            ret_list.append(real_str)
        if debug:
            print('debug>>:',ret_list)
        return ''.join(ret_list)

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
