# -*- coding: utf-8 -*-
import scrapy
import logging
import sys,os,json
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from ..items import WeiyiItem
from urllib import parse
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError

logger = logging.getLogger(__name__)

class WeiyiSpider(scrapy.Spider):
    name = 'weiyi'
    allowed_domains = ['www.guahao.com/json/white/search/eteams']

    depart_ment = ['儿科', '皮肤科', '妇产科', '口腔科','新生儿科']
    start_urls = []

    with open(r"F:\python-test\first_scrapy\first_scrapy\spiders\start_url.json", 'r') as load_f:
        load_dict = json.load(load_f)
        for link in load_dict:
            start_urls.append(link)

    def parse(self, response):
        url = response.request.url
        data = json.loads(response.text.encode('utf8'))['data']
        if data['pageCount'] > 1:
            for i in range(1, data['pageCount'] + 1):
                # url = self.url_values_plus(url, 'page', i)
                u = parse.urlparse(url)
                qs = u.query
                pure_url = url.replace('?' + qs, '')
                qs_dict = dict(parse.parse_qsl(qs))
                for k in qs_dict.keys():
                    if k == 'page':
                        qs_dict[k] = i
                        tmp_qs = parse.unquote(parse.urlencode(qs_dict))
                        url = pure_url + "?" + tmp_qs
                        break
                logger.warning(url)
                yield scrapy.Request(url, callback=self.dealData, errback=self.errback_httpbin,dont_filter=True)
        else:
            yield scrapy.Request(url, callback=self.dealData, errback=self.errback_httpbin,dont_filter=True)


    # 处理数据
    def dealData(self, response):
        url = response.request.url
        u = parse.urlparse(url)
        qs = u.query
        qs_dict = dict(parse.parse_qsl(qs))
        departmantName = qs_dict['dept']
        logger.info(response.text)
        data_list = json.loads(response.text.encode('utf8'))['data']['list']
        if data_list:
            for data in data_list:
                item = WeiyiItem()
                item['id'] = data['id']
                item['departmantName'] = departmantName
                item['tlDoctorName'] = data['tlDoctorName']
                item['provinceName'] = data['provinceName']
                item['teamDoctorActivityList'] = data['teamDoctorActivityList']
                item['tlExpertPhoto'] = data['tlExpertPhoto']
                item['tlExpertUuid'] = data['tlExpertUuid']
                item['totalConsultCount'] = data['totalConsultCount']
                item['totalOrderCount'] = data['totalOrderCount']
                item['provinceId'] = data['provinceId']
                item['plusDemand'] = data['plusDemand']
                item['photo'] = data['photo']
                item['name'] = data['name']
                item['link'] = data['link']
                item['isPlus'] = data['isPlus']
                item['introduction'] = data['introduction']
                item['hospitalNameList'] = data['hospitalNameList']
                item['expertIdList'] = data['expertIdList']
                item['expertCount'] = data['expertCount']
                item['diseaseMap'] = data['diseaseMap']
                item['diseaseList'] = data['diseaseList']
                item['consultStarExpert'] = data['consultStarExpert']
                item['cityName'] = data['cityName']
                item['cityId'] = data['cityId']
                item['chatId'] = data['chatId']
                item['activityId'] = data['activityId']

                yield item

    def errback_httpbin(self, failure):
        # 日志记录所有的异常信息
        self.logger.error(repr(failure))

        # 假设我们需要对指定的异常类型做处理，
        # 我们需要判断异常的类型

        if failure.check(HttpError):
            # HttpError由HttpErrorMiddleware中间件抛出
            # 可以接收到非200 状态码的Response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # 此异常由请求Request抛出
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
                request = failure.request
                self.logger.error('TimeoutError on %s', request.url)
    # 替换某个参数信息
    def url_values_plus(url, k1, v1):
        ret = ''
        u = parse.urlparse(url)
        print('u:', u)
        qs = u.query
        print('qs:', qs)
        pure_url = url.replace('?' + qs, '')
        print('pure_url:', pure_url)
        qs_dict = dict(parse.parse_qsl(qs))
        print('qs_dict:', qs_dict)
        for k in qs_dict.keys():
            if k == k1:
                qs_dict[k] = v1
                tmp_qs = parse.unquote(parse.urlencode(qs_dict))
                ret = pure_url + "?" + tmp_qs
                break
        return ret
