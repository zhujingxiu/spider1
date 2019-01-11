# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Id97Pipeline(object):
    fp = None
    def open_spider(self, spider):
        print("--------pipeline启动，开始爬虫----------")
        self.fp = open('id97.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        detail = "%s\n%s\n%s\n%s\n%s\n\n\n" % (item['title'],item['tag'],item['director'],item['actor'],item['score'])
        print(detail)
        try:
            self.fp.write(detail)
        except Exception as e:
            print(e)
        return item

    def close_spider(self,spider):
        print("--------pipeline启动，爬虫结束----------")
        self.fp.close()
