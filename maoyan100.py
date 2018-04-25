'''
爬取猫眼电影top100，存储到mongodb
'''
from requests_html import HTMLSession
import pymongo

class Top100:
    def __init__(self):
        self.urls = ['http://maoyan.com/board/4?offset={0}'.format(i*10) for i in range(10)]
        self.client = pymongo.MongoClient('localhost', port=27017)
        self.db = self.client['top100']
        self.collections = self.db['maoyan']

    def get_page_content(self, url):
        try:
            #print('#####url is @', url)
            session = HTMLSession()
            self.response = session.get(url)
            self.parse_url_content()
        except Exception as e:
            print(e)
            pass


    def parse_url_content(self):
        info = {}
        movie_infos = self.response.html.find('#app > div > div > div.main > dl > dd')
        for movie in movie_infos:
            info['_id'] = movie.find('i', first=True).text
            info['movie'] = movie.find('div > div > div.movie-item-info > p > a', first=True).text
            info['url'] = 'http://maoyan.com{0}'.format(movie.find('div > div > div.movie-item-info > p > a', first=True).attrs['href'])
            info['actor'] = movie.find('div > div > div.movie-item-info > p.star', first=True).text
            info['releasetime'] = movie.find('div > div > div.movie-item-info > p.releasetime', first=True).text
            info['score'] = movie.find('div > div > div.movie-item-number.score-num > p > i.integer', first=True).text+movie.find('div > div > div.movie-item-number.score-num > p > i.fraction', first=True).text
            #self.collections.insert(info)
            self.write_to_database(info)
            #print(info)

    def write_to_database(self, info):
        try:
            self.collections.insert(info)
        except Exception as e:
            print(e)

    def spider(self):
        for url in self.urls:
            self.get_page_content(url)


if __name__ == '__main__':
    spider = Top100()
    spider.spider()
