import os
import scrapy
from ..items import Movie


class spider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["imdb.com"]

    def start_requests(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/movies.txt') as f:
            for title in list(f):
                url = f'https://imdb.com/find?q={title}'
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        href = response.xpath('//*[@id="main"]/div/div[2]/table/tr[1]/td[2]/a/@href').extract()[0]
        url = f'http://imdb.com{href}'

        il = scrapy.loader.ItemLoader(item=Movie(), response=response)
        il.add_xpath('title',               '//*[@id="main"]/div/div[2]/table/tr[1]/td[2]/a/text()')
        il.add_xpath('release_date',        '//*[@id="main"]/div/div[2]/table/tr[1]/td[2]/text()')

        yield scrapy.Request(
                                url=url,
                                callback=self.parse_description,
                                meta={'movie': il.load_item()}
                            )

    def parse_description(self, response):
        il = scrapy.loader.ItemLoader(item=response.meta['movie'], response=response)
        il.add_xpath('director',            '//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a/text()')
        il.add_xpath('cast_top3',           '//*[@id="title-overview-widget"]/div[2]/div[1]/div[4]/a/text()')
        il.add_xpath('runtime',             '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/time/text()')
        il.add_xpath('imdb_rating',         '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
        il.add_xpath('genres',              '//*[@id="titleStoryLine"]/div[4]/a/text()')
        il.add_xpath('budget',              '//*[@id="titleDetails"]/div[7]/text()')
        il.add_xpath('language',            '//*[@id="titleDetails"]/div[3]/a[1]/text()')
        yield il.load_item()