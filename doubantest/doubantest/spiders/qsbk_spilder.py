# -*- coding: utf-8 -*-
import scrapy


class QsbkSpilderSpider(scrapy.Spider):
    name = 'doubantest'
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        print(response.body)
