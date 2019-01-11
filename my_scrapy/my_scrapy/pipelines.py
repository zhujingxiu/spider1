# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import redis
import json

class MyScrapyRedis(object):
    redis = None

    def open_spider(self, spider):
        print("开始Redis爬虫")
        self.redis = redis.Redis(host='127.0.0.1', port=6379)

    def process_item(self, item, spider):
        author = item['author']
        content = item['content']
        print(spider)
        try:
            ret = self.redis.lpush('joy', json.dumps({'author': author, 'content': content}).encode('utf-8'))
            print('"redis-push:', ret)
        except Exception as e:
            print(e)
        return item

    def close_spider(self, spider):
        print("结束Redis爬虫")


class MyScrapyPipeline(object):
    fp = None
    db = None

    db_cfg = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': '123456', 'db': 'pydb'}

    def open_spider(self, spider):
        print("开始爬虫")
        self.fp = open('./qiubai_pipe.txt', 'w', encoding='utf-8')
        self.db = pymysql.connect(**self.db_cfg)

    def process_item(self, item, spider):
        author = item['author']
        content = item['content']
        ########### 文件存储
        self.fp.write("作者:%s\n%s\n\n\n" % (author, content))
        ########### 数据库存储
        sql = '''
            INSERT INTO `joy` (`author`,`content`) VALUES ("%s","%s")
            ''' % (author, content)
        print(sql)
        try:
            self.db.cursor().execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        return item

    def close_spider(self, spider):
        print("结束爬虫")
        self.fp.close()
        self.db.cursor().close()
        self.db.close()

