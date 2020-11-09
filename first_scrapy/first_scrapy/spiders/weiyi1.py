import scrapy,json


class Weiyi1Spider(scrapy.Spider):
    name = 'weiyi1'
    allowed_domains = ['www.guahao.com']
    start_urls = []

    with open(r"first_scrapy\spiders\start_url1.json", 'r') as load_f:
        load_dict = json.load(load_f)
        for link in load_dict:
            start_urls.append(link)

    def parse(self, response):
        pass
