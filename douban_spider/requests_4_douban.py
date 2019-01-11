#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2019/1/8
import json
import random
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs
import settings


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
            print('1.账户已登录')
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
        print("图片验证码地址: ", url_captcha)
        browser = webdriver.Chrome()
        browser.set_window_size(400, 300)
        browser.get(url_captcha)
        captcha_text = input('请输入上面图片中的验证码>>:')
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
        if response:
            content = response.text

            types_dict = []
            tree = etree.HTML(content)
            movies_types = tree.xpath('//*[@id="content"]/div/div[2]/div[1]/div/span')
            for span in movies_types:
                a_url = span.xpath('./a/@href')[0]
                a_text = span.xpath('./a/text()')[0]
                types_dict.append({'text': a_text.strip(), 'url': a_url.split('?')[1].strip(), })
            self.save_file('movies_types.json', json.dumps(types_dict).encode())
        if response:
            print('2.访问分类排行榜页面')

        return response

    def get_cookies(self):
        data = []
        _cookie_dict = requests.utils.dict_from_cookiejar(self.request.cookies)
        if _cookie_dict:
            for item in _cookie_dict:
                data.append({'name': item, 'value': _cookie_dict[item]})
        return data

    def movies_rank_type(self, save=False):
        '''
        指定分类排行榜
        :return:
        '''

        movies_types = json.load(open('./data/movies_types.json', 'r', encoding='utf-8'))
        if movies_types:
            for i, item in enumerate(movies_types):
                print("%d.%s" % (i, item.get('text')))
        type_index = int(input("请输入指定的数字类型(默认为0)>>:").strip())
        movies_type = movies_types[type_index]
        if not movies_types:
            movies_type = movies_types[0]
        type_name = movies_type.get('text')
        url = "%s?%s" % (self.type_url, movies_type.get('url'))
        print("3.访问电影类型：%s -> %s" % (type_name, url))

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
        browser.execute_script('window.scrollTo(0,2000)')
        content = browser.page_source
        self.save_file("%s.html" % type_name, content.encode('utf-8'))
        movie_items = browser.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div[6]/div')
        movies_list =[]
        for movie in movie_items:
            title = movie.find_element_by_xpath('./div/div/div/span/a').text
            url = movie.find_element_by_xpath('./div/a').get_attribute('href')
            movies_list.append({
                'title': title,
                'url': url,
            })
        print(movies_list)
        if save:
            self.save_movies(movies_list)
        return movies_list

    def save_movies(self, movies_list):
        if not movies_list:
            return False
        movies = []
        for item in movies_list:
            if not item.get('url'):
                continue
            movie = self.movie_detail(item.get('url'))
            print(movie)
            movies.append(movie)
        return self.save_file('movies.json', json.dumps(movies).encode())

    def movie_detail(self, url):
        print("访问电影详情页面>> ", url)
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        # 使用requests的cookie
        if self.get_cookies():
            cookies = self.get_cookies()
            for item in cookies:
                browser.add_cookie(item)
        browser.get(url)
        movie = {
            # 'title': browser.find_element_by_xpath('//*[@id="content"]/h1/span[1]').text,
            # 'year': browser.find_element_by_xpath('//*[@id="content"]/h1/span[2]').text,
            # 'cover': browser.find_element_by_xpath('//*[@id="mainpic"]/a/img').get_attribute('src'),
            # 'director': browser.find_element_by_xpath('//*[@id="info"]/span[1]/span[2]/a').text,
            # 'scriptwriter': browser.find_element_by_xpath('//*[@id="info"]/span[2]/span[2]').text,
            # 'actor': browser.find_element_by_xpath('//*[@id="info"]/span[@class="actor"]/span[2]').text,
            # 'releasedate': browser.find_element_by_xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]').text,
            # 'runtime': browser.find_element_by_xpath('//*[@id="info"]/span[@property="v:genre"]').text,
            # 'score': browser.find_element_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong').text,
        }
        movie_types = []
        genre_eles = browser.find_elements_by_xpath('//*[@id="info"]/span[@property="v:genre"]')
        for ele_type in genre_eles:
            movie_types.append(ele_type.text)
        movie['type'] = ' '.join(movie_types)
        xpath_selector = ''
        pl_eles = browser.find_elements_by_css_selector('#info span[class=pl]')
        for i, ele in enumerate(pl_eles, 1):
            ele_text = ele.text
            print(ele_text, ele_text.find("语言:"), i)
            if ele_text.find("语言:") != -1:
                print('parent:%s | location:%s' % (ele.parent, ele.location))
                xpath_selector = '//*[@id="info"]/span[@class="pl"][%d]/following-sibling::*/text()' % i
                print(xpath_selector)

                break
        language = browser.find_element_by_xpath(xpath_selector)[0]
        print(language)
        browser.quit()
        return movie

    def save_file(self, filename, content):
        filename = './data/%s' % filename
        with open(filename, 'wb') as f:
            f.write(content)
        return filename

    def test(self):
        pass
