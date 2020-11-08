# -*- coding: utf-8 -*-
import scrapy


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    def parse(self, response):
        # with open("qiubai.html", 'w', encoding="utf-8") as f:
        #     f.write(response.text)
        div_list = response.xpath('//div[starts-with(@id, "qiushi_tag_")]')
        print(type(div_list))
        # 遍历列表，获取列表内容
        item_list = []
        for div in div_list:
            '''
            先通过xpath获取内容，返回的是一个列表
            然后通过extract()转换成unicode字符串，再获取第0个, 也就是指定的内容
            将解析到的内容保存到字典中
            '''
            image_url = div.xpath('./div[@class="author clearfix"]//img/@src').extract_first()
            name = div.xpath('./div[@class="author clearfix"]//h2/text()').extract_first()
            age = div.xpath('./div[@class="author clearfix"]/div/text()').extract_first()
            content = div.xpath('./a/div[@class="content"]/span/text()').extract()
            content = ' '.join(content)
            haha_count = div.xpath('./div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract()[0]
            item = dict(
                image_url=image_url,
                name=name,
                age=age,
                content=content,
                haha_count=haha_count
            )
            yield item
