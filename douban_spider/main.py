#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2019/1/9


from requests_4_douban import Douban

if __name__ == '__main__':
    '''
    0.把下载下来的phantomjs.exe移到你所用python文件夹下的Script中就可以使用了
    1.使用任意代理IP进行如下操作
    2.使用requests模块进行豆瓣电影的个人用户登录操作
    3.使用requests模块访问个人用户的电影排行榜->分类排行榜->任意分类对应的子页面
    4.爬取需求3对应页面的电影详情数据
    5.爬取3对应页面中滚动条向下拉动2000像素后加载出所有电影详情数据，存储到本地json文件中或者相应数据库中
    【备注】电影详情数据包括：海报url、电影名称、导演、编剧、主演，类型，语言，上映日期，片长，豆瓣评分
    '''
    douban = Douban()
    # # 2.使用requests模块进行豆瓣电影的个人用户登录操作
    # response = douban.login()
    # douban.save_file('login_home.html', response.content)
    # # 3.使用requests模块访问个人用户的电影排行榜->分类排行榜->任意分类对应的子页面
    # response = douban.movies_rank()
    # douban.save_file('movies_rank.html', response.content)
    #
    # type_movies = douban.movies_rank_type()
    # movies = []
    # if type_movies:
    #     for item in type_movies:
    #         if item.get('url'):
    #             movie = douban.movie_detail(item.get('url'))
    #             print(movie)
    #             movies.append(movie)

    detail = douban.movie_detail('https://movie.douban.com/subject/30414462')
    print(detail)