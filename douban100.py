'''
爬取豆瓣电影top 100排行，并存储到mongodb
'''
from collections import deque
from requests_html import HTMLSession

import pymongo


class Top100Spider:
    def __init__(self, url):
        self.start_url = url
        self.content = None
        self.pack = []
        self.page_url = []
        self.client = pymongo.MongoClient('localhost', port=27017)
        self.db = self.client['top100']
        self.collections = self.db['movie']

    def _start_craw(self):
        session = HTMLSession()
        self.content = session.get(self.start_url)
        self._get_pagenation_urls()
        self._get_movies_info()

    def _get_content(self, url=None):
        session = HTMLSession()
        self.content = session.get(url)

    def _get_pagenation_urls(self):
        pagenations = self.content.html.find('#content > div > div.article > div.paginator > a')
        for page in pagenations:
            self.page_url.append(page.attrs['href'])

    def _get_movies_info(self):
        # self._get_content()
        movie_table = self.content.html.find('#content > div > div.article > div:nth-child(3) > table > tr > td:nth-child(2) > div')
        #print(movie_table)

        for movie in movie_table:
            info = {}
            info['movie'] = movie.find('a', first=True).text
            info['link'] = movie.find('a', first=True).attrs['href']
            info['info'] = movie.find('p', first=True).text
            info['score'] = movie.find('div > span.rating_nums', first=True).text
            self.pack.append(info)
            self.collections.insert(info)
    
    def spider_top100(self):
        self._start_craw()
        for url in self.page_url:
            self._get_content(url)
            self._get_movies_info()

    def print_top100_movies(self):
        for info in self.pack:
            print(info)


if __name__ == "__main__":
    url = 'https://movie.douban.com/tag/Top100'
    spider = Top100Spider(url)
    #spider.get_movies_info()
    spider.spider_top100()
    #spider.print_top100_movies()
    

    

