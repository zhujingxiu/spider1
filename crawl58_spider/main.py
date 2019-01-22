#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2019/1/21
from crawl58_spider import settings
from crawl58_spider import utils
from redis import Redis
from scrapy import cmdline

redis_key = 'bjzhufang:start_urls'
redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
start_url = redis_conn.lindex(redis_key, 0)
if not start_url:
    redis_conn.lpush(redis_key, 'https://bj.58.com/chuzu/')
    start_url = redis_conn.lindex(redis_key, 0)

print('localhost:%s | start-url:%s' % (utils.get_host_ip(), start_url))

cmdline.execute(['scrapy', 'crawl', 'bjzhufang', '--nolog'])