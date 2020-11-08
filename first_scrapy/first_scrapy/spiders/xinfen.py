import scrapy


class XinfenSpider(scrapy.Spider):
    name = 'xinfen'
    allowed_domains = ['xinfen.com.cn']
    start_urls = ['http://xinfen.com.cn/']

    def parse(self, response):
        pass
