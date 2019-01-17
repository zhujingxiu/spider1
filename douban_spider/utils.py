#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2019/1/16

import time


def calcu_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        print('\033[0;36;40m', "进入%s方法：" % func.__name__, '\033[0m')
        result = func(*args, **kwargs)
        t2 = time.time()
        title = ''
        if isinstance(result, dict):
            title = result.get('title')

        print('\033[0;36;40m', "%s 执行时长: %s secs." % (title, int(t2 - t1)), '\033[0m')
        return result

    return wrapper