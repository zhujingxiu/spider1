#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2019/1/8
import json
import random
import datetime
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
import settings
import utils


class Douban(object):
    login_url = 'https://accounts.douban.com/login'
    movies_url = 'https://movie.douban.com/chart'
    type_url = 'https://movie.douban.com/typerank'

    def __init__(self):
        self.request = requests.session()
        self.user = settings.DOUBAN_USER
        self.pwd = settings.DOUBAN_PWD
        self.captcha_solution = None
        self.captcha_id = None

    @property
    def login_data(self):
        data = {'source': 'index_nav', 'redir': 'https://www.douban.com', 'form_email': self.user,
                'form_password': self.pwd, 'login': '登录'}
        if self.captcha_solution:
            data['captcha-solution'] = self.captcha_solution

        if self.captcha_id:
            data['captcha-id'] = self.captcha_id

        return data

    @property
    def proxies(self):
        return random.choice(settings.PROXIES)

    @property
    def headers(self):
        return {'User-Agent': random.choice(settings.USER_AGENT)}

    def login(self):
        '''
        登录
        :return:
        '''
        response = self.request.post(url=self.login_url, data=self.login_data, headers=self.headers,
                                     proxies=self.proxies)
        content = response.text
        bsoup = bs(content, 'lxml')
        captcha = bsoup.find('img', id='captcha_image')
        if captcha:
            response = self.captcha_login(captcha, bsoup)
        if response:
            print('\033[0;34;40m', '1.账户已登录', '\033[0m')
        return response

    def captcha_login(self, captcha, bsoup):
        '''
        验证码登录
        :param captcha:
        :param bsoup:
        :return:
        '''
        from selenium import webdriver
        url_captcha = captcha.get('src')
        input_captcha_id = bsoup.find('input', attrs={'name': 'captcha-id'})
        captcha_id = input_captcha_id.get('value')
        print('\033[0;34;40m', "图片验证码地址: %s " % url_captcha, '\033[0m')
        browser = webdriver.Chrome()
        browser.set_window_size(400, 300)
        browser.get(url_captcha)
        captcha_text = input('\033[0;31;40m请输入上面图片中的验证码>>:\033[0m')
        self.captcha_solution = captcha_text
        self.captcha_id = captcha_id
        browser.quit()
        try:
            response = self.request.post(url=self.login_url, data=self.login_data, headers=self.headers,
                                         proxies=self.proxies)
            return response
        except:
            for i in range(settings.LOGIN_TRY):
                response = self.captcha_login(captcha, bsoup)
                if response:
                    return response
        return False

    def movies_rank(self):
        '''
        分类排行榜
        :return:
        '''
        response = self.request.get(url=self.movies_url)
        # 更新影片分类到本地文件
        if response:
            content = response.text
            types_dict = []
            tree = etree.HTML(content)
            try:
                movies_types = tree.xpath('//*[@id="content"]/div/div[2]/div[1]/div/span')
                for span in movies_types:
                    a_url = span.xpath('./a/@href')[0]
                    a_text = span.xpath('./a/text()')[0]
                    types_dict.append({'text': a_text.strip(), 'url': a_url.split('?')[1].strip(), })
            except:
                pass
            self.save_file('movies_types.json', json.dumps(types_dict).encode())

            print('\033[0;34;40m', '2.访问分类排行榜页面', '\033[0m')

        return response

    def get_cookies(self):
        data = []
        _cookie_dict = requests.utils.dict_from_cookiejar(self.request.cookies)
        if _cookie_dict:
            for item in _cookie_dict:
                data.append({'name': item, 'value': _cookie_dict[item]})
        return data

    def get_webdriver(self, url):
        '''
        使用chrome--headless模式，并同步cookie
        :param url:
        :return:
        '''
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=options)
        # 先更新下cookie信息
        browser.get(url)
        # 使用requests的cookie
        if self.get_cookies():
            cookies = self.get_cookies()
            for item in cookies:
                browser.add_cookie(item)
        browser.get(url)
        return browser

    @utils.calcu_time
    def movies_rank_type(self, save=False):
        '''
        指定分类排行榜
        :return:
        '''
        movies_types = json.load(open('./data/movies_types.json', 'r', encoding='utf-8'))
        if movies_types:
            for i, item in enumerate(movies_types):
                print("%d.%s" % (i, item.get('text')))
        type_index = int(input("\033[0;31;40m请输入指定的数字类型(默认为0)>>:\033[0m").strip())
        movies_type = movies_types[type_index]
        if not movies_types:
            movies_type = movies_types[0]
        type_name = movies_type.get('text')
        url = "%s?%s" % (self.type_url, movies_type.get('url'))
        print('\033[0;34;40m', "3.访问电影类型：%s -> %s ：" % (type_name, url), '\033[0m')

        browser = self.get_webdriver(url)
        browser.execute_script('window.scrollTo(0,2000)')
        # 本地保存下
        content = browser.page_source
        self.save_file("%s.html" % type_name, content.encode('utf-8'))
        movies_list = []
        # 解析html
        try:
            movie_items = browser.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div[6]/div')
            for i, movie in enumerate(movie_items, 1):
                title = movie.find_element_by_xpath('./div/div/div/span/a').text
                url = movie.find_element_by_xpath('./div/a').get_attribute('href')
                item = {'title': title, 'url': url, }
                movies_list.append(item)
                print("%d. %s %s" % (i, title, url))
        except:
            pass
        if save:
            self.save_movies(movies_list)
        return movies_list

    def save_movies(self, movies_list, filename=None):
        if not movies_list:
            return False
        movies = []
        for item in movies_list:
            if not item.get('url'):
                continue
            movie = self.movie_detail(item.get('url'))
            print(movie)
            movies.append(movie)
        if not filename:
            filename = 'movies-%s.json' % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return self.save_file(filename, json.dumps(movies).encode())

    @utils.calcu_time
    def movie_detail(self, url):
        browser = self.get_webdriver(url)
        browser.get(url)
        movie = {'title': '', 'year': '', 'cover': '', 'director': '', 'scriptwriter': '', 'actor': '',
            'releasedate': '', 'runtime': '', 'score': '', 'type': '', 'language': '', }
        try:
            # 电影名称
            title_ele = browser.find_element_by_xpath('//*[@id="content"]/h1/span[1]')
            if title_ele:
                movie['title'] = title_ele.text
            year_ele = browser.find_element_by_xpath('//*[@id="content"]/h1/span[2]')
            if year_ele:
                movie['year'] = year_ele.text

            # 电影封面
            cover_ele = browser.find_element_by_xpath('//*[@id="mainpic"]/a/img')
            if cover_ele:
                movie['cover'] = cover_ele.get_attribute('src')

            # 电影导演
            director_ele = browser.find_element_by_xpath('//*[@id="info"]/span[1]/span[2]/a')
            if director_ele:
                movie['director'] = director_ele.text
            # 电影编剧
            scriptwriter_ele = browser.find_element_by_xpath('//*[@id="info"]/span[2]/span[2]')
            if scriptwriter_ele:
                movie['scriptwriter'] = scriptwriter_ele.text
            # 电影演员
            actor_ele = browser.find_element_by_xpath('//*[@id="info"]/span[@class="actor"]/span[2]')
            if actor_ele:
                movie['actor'] = actor_ele.text
            # 电影上映日期
            release_ele = browser.find_element_by_xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]')
            if release_ele:
                movie['releasedate'] = release_ele.text
            # 电影片长
            runtime_ele = browser.find_element_by_xpath('//*[@id="info"]/span[@property="v:runtime"]')
            if runtime_ele:
                movie['runtime'] = runtime_ele.text
            # 电影评分
            score_ele = browser.find_element_by_css_selector('#interest_sectl strong')
            if score_ele:
                movie['score'] = score_ele.text
            # 电影类型
            movie_types = []
            genre_eles = browser.find_elements_by_xpath('//*[@id="info"]/span[@property="v:genre"]')
            for ele_type in genre_eles:
                movie_types.append(ele_type.text)
            movie['type'] = ' '.join(movie_types)
            # 电影语言
            language_ele = browser.find_element_by_xpath('//*[@id="info"]/span[@class="pl" and contains(text(),"语言:")]')
            if language_ele:
                movie['language'] = browser.execute_script('return arguments[0].nextSibling.textContent', language_ele)
        except:
            pass

        browser.quit()
        return movie

    def save_file(self, filename, content):
        filename = './data/%s' % filename
        with open(filename, 'wb') as f:
            f.write(content)
        return filename
