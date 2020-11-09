# -*- coding: utf-8 -*-
import scrapy, json
import math
from lxml import etree
from ..items import DataFangItem, DataDynamicJson, DataCommentJson,  DataHouseapartment, ImageItem
import re, io
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep


class FangtianxiaSpider(scrapy.Spider):
    name = "fangtianxia"
    allowed_domains = ["fang.com"]
   # city_link_list = io.open(r"/home/kevin/work/data_fang/data_fang/spiders/城市url", "r", encoding="gbk")
    city_link_list = ['http://bj.fang.com/']
    # city_link_list = city_link_list.readline()


    for link in city_link_list:
        start_urls = link.replace("\n", "")
        start_urls = [start_urls]

    def __init__(self):
        super(FangtianxiaSpider, self).__init__()

        self.dynamic_urls = []
        self.dynamicJson = []
        self.house_list = []

    def parse(self, response):
        # 解析每个城市
        new_house = response.xpath(
            "//div[@class='newnav20141104nr']//div/a[contains(text(),'新房')]/@href").extract()[0]  # 获取新房url
        new_house = re.sub(r"\?\w+\=\w+", "", new_house)  # 去掉？后面的字符
        print('新房信息：', self.parse_all_house)
        yield scrapy.Request(new_house, callback=self.parse_all_house)

    def parse_all_house(self, response):
        # 解析所有房源
        url = response.url

        all_house = response.xpath("//*[@class='clearfix']/div/a/@href ").extract()  # 获取当前页面所有的房源url
        for one_house in all_house:
            house = u"https:" + one_house
            house = re.sub(r"\?\w+=\w+_\w+", "", house)  # 去掉？后面的字符
            self.house_list.append(house)

        # The_next_page = response.xpath(
        #     '//li[@class="floatr rankWrap"]/div/a[contains(text(),">")]/@href').extract_first()  # 获取下一页
        # if The_next_page != None:
        #     The_next_page = url + The_next_page
        #     yield scrapy.Request(The_next_page, callback=self.parse_all_house)

        the_next_page = response.xpath(
            '//li[@class="floatr rankWrap"]/div/a[contains(text(),">")]/@href').extract_first()  # 获取下一页
        if the_next_page is None:
            url = self.house_list.pop()
            yield scrapy.Request(url, callback=self.home_page)

        else:
            the_next_page_url = url + the_next_page
            yield scrapy.Request(the_next_page_url, callback=self.parse_all_house)

    def home_page(self, response):
        # 解析首页获取详情页
        item = DataFangItem()
        item['_id'] = response.url
        item['subarea'] = response.xpath('//div[@class="br_left"]//ul[@class="tf f12"]//li[3]/a/text()').extract()
        item['subarea'] = "".join(item['subarea'])  # 字符串切片，去掉后面2个字
        item['subarea'] = item['subarea'][:-2]
        item['area'] = response.xpath('//div[@class="s2"]/div/a/text()').extract()  # 当前城市




        positioning = response.xpath("//div[@class='mapbox_dt']/iframe/@src").extract_first()  # 获取楼盘定位地址
        positioning = u"https:" + positioning

        particulars = response.xpath("//*[@class='navleft tf']//a[contains(text(),'详情')]/@href|"
                                     "//*[@class='navleft tf']//a[contains(text(),'详细')]/@href").extract()  # 楼盘详情
        particulars = "".join(particulars)
        particulars = u"https:" + particulars

        # yield scrapy.Request(positioning, meta={"item": item, "xiangqing": particulars}, callback=self.positioning)    # 爬取详情打开注释

        try:
            dynamic = response.xpath("//*[@class='navleft tf']//a[contains(text(),'动态')]/@href").extract()  # 楼盘动态
            dynamic = "".join(dynamic)
            dynamic = u"https:" + dynamic
            yield scrapy.Request(dynamic, callback=self.parse_dynamic)
        except Exception as e:
            pass
        url = self.house_list.pop()
        yield scrapy.Request(url, callback=self.home_page)

        """爬取点评打开注释"""
        # try:
        #     comments = response.xpath(
        #         "//*[@class='navleft tf']//a[contains(text(),'点评')]/@href").extract_first()  # 楼盘点评
        #     comments = "".join(comments)
        #     comments = u"https:" + comments
        #     yield scrapy.Request(comments, callback=self.parse_comments)
        # except Exception as e:
        #     pass

        """爬取户型打开注释"""
        # try:
        #     houseapartment = response.xpath(
        #         "//*[@class='navleft tf']//a[contains(text(),'户型')]/@href").extract_first()  # 楼盘户型
        #     # houseapartment = "".join(houseapartment)
        #     houseapartment = u"https:" + houseapartment
        #     yield scrapy.Request(houseapartment, callback=self.parse_houseapartment)
        # except Exception as e:
        #     pass

        """爬取相册打开注释"""
        # try:
        #     houseImage = response.xpath(
        #         "//*[@class='navleft tf']//a[contains(text(),'相册')]/@href").extract_first()  # 楼盘相册
        #     if not houseImage:
        #         yield {"_id": item['_id'], "houseImage": json.dumps([])}
        #     houseImage = u"https:" + houseImage
        #     yield scrapy.Request(houseImage, meta={"_id": response.url}, callback=self.parse_image_base)
        # except Exception as e:
        #     pass

    def parse_image_base(self, response):
        """
        使用正则的方法匹配url,并且直接使用ajax请求
        :return:
        """
        html = response.text
        _id = response.meta["_id"]
        building_name = re.search(r"//(\w+)\.", response.url).group(1)
        building_number = re.search(r"(\d+)\.htm", response.url).group(1)
        module_dict = {}
        image_list = []
        re_effect_image = re.compile(r"\<a\W.*?\<span\>效果图\<\/span\>.*?\<\/a\>")
        re_realsight_image = re.compile(r"\<a\W.*?\<span\>实景图\<\/span\>.*?\<\/a\>")
        re_traffic_image = re.compile(r"\<a\W.*?\<span\>交通图\<\/span\>.*?\<\/a\>")
        re_prototype_room = re.compile(r"\<a\W.*?\<span\>样板间\<\/span\>.*?\<\/a\>")

        effect_image = re_effect_image.findall(html)
        realsight_image = re_realsight_image.findall(html)
        traffic_image = re_traffic_image.findall(html)
        prototype_room = re_prototype_room.findall(html)

        pattern_url = re.compile(r"//.*?htm")
        pattern_num = re.compile(r"<em>(\d+)<\/em>")

        # use interface to get data directly
        effect_number, realsight_number, traffic_number, prototype_number = (0, 0, 0, 0)
        if effect_image:
            try:
                effect_image_url = "http:" + pattern_url.findall(effect_image[0])[0]
                effect_number = int(pattern_num.search(effect_image[0]).group(1))
                module_dict.update({"xiaoguotu": [effect_number, effect_image_url, 904]})
            except Exception as e:
                print(str(e))
                effect_number = 0
        if realsight_image:
            try:
                realsight_image_url = "http:" + pattern_url.findall(realsight_image[0])[0]
                realsight_number = int(pattern_num.search(realsight_image[0]).group(1))
                module_dict.update({"shijingtu": [realsight_number, realsight_image_url, 903]})
            except Exception as e:
                print(str(e))
                realsight_number = 0
        if traffic_image:
            try:
                traffic_image_url = "http:" + pattern_url.findall(traffic_image[0])[0]
                traffic_number = int(pattern_num.search(traffic_image[0]).group(1))
                module_dict.update({"jiaotongtu": [traffic_number, traffic_image_url, 901]})
            except Exception as e:
                print(str(e))
                traffic_number = 0
        if prototype_room:
            try:
                prototype_room_url = "http:" + pattern_url.findall(prototype_room[0])[0]
                prototype_number = int(pattern_num.search(prototype_room[0]).group(1))
                module_dict.update({"yangbanjian": [prototype_number, prototype_room_url, 905]})
            except Exception as e:
                print(str(e))
                prototype_number = 0

        # 判断如果各种图全部没有，则直接返回
        if effect_number + realsight_number + traffic_number + prototype_number == 0:
            print("一张图片都没有")
            yield {"_id": _id, "picJson": json.dumps("", ensure_ascii=False)}
        else:
            full_image_interface_list = []
            for key, value in module_dict.items():
                base_url = "http://" + building_name + ".fang.com/house/ajaxrequest/photolist_get.php?newcode=" + building_number + "&type=" + str(
                    value[2]) + "&room=&nextpage="
                page_number = value[0] // 6 + 2 if value[0] % 6 else value[0] // 6 + 1
                [full_image_interface_list.append([base_url + str(i), key]) for i in range(1, page_number)]
            first_url = full_image_interface_list.pop()
            meta = {"_id": _id, "request_list": full_image_interface_list, "type": first_url[1], "json_data": []},
            yield scrapy.Request(first_url[0], meta={"item": meta}, callback=self.parse_images)

    def parse_images(self, response):
        """
        :param total_number: total number of images of effect
        :param style_number: total number of images of effect
        :return:
        """
        item = dict(response.meta["item"][0])
        TuUrl = ImageItem()
        data_list = item["json_data"]
        image_type = item["type"]
        _id = item["_id"]
        full_image_interface_list = item["request_list"]

        if full_image_interface_list:
            data = json.loads(response.body)
            # print("相册借口", data)
            [data_list.append({"picUrl": "http:" + re.sub(r"\d+x\d+\.", "880x600.", i["url_s"]), "type": image_type})
             for i in data]

            first_url = full_image_interface_list.pop()
            meta = {"_id": _id, "request_list": full_image_interface_list, "type": first_url[1],
                    "json_data": data_list},
            yield scrapy.Request(first_url[0], meta={"item": meta}, callback=self.parse_images)
        else:
            yield {"_id": _id, "picJson": json.dumps(data_list)}

        data = json.loads(response.text)
        for images in data:
            TuUrl["image_urls"] = ["http:" + re.sub(r"\d+x\d+\.", "880x600.", images["url_s"])]
            yield TuUrl

    def parse_houseapartment(self, response):
        # 解析户型页面 通过拼接 接口获取数据
        data_url = response.url
        building_name = re.sub(r"\w+\/\w+_\d+_\d+.htm", "", data_url)
        building_number = re.search(r"(\d+)\.htm", data_url).group(1)

        jiekou_url = building_name + "house/ajaxrequest/householdlist_get.php?newcode=" + building_number + "&room=all"
        yield scrapy.Request(jiekou_url, meta={"house_url": building_name}, callback=self.house_interface)

    def house_interface(self, response):
        # 户型接口
        item = DataHouseapartment()
        house_url = response.meta["house_url"]
        all_comment_dict = {"_id": house_url}
        houseapartment = []
        datas = json.loads(response.text)
        for data in datas:
            # item["houseUrl"]
            images = []
            imag = "http:" + re.sub("220x150", "748x600", data["houseimageurl"])
            images.append({"picUrl": imag})
            item["imgs"] = images  # 户型名称
            # item["_id"] = house_url  # 户型url
            item["name"] = data["housetitle"]  # 户型名称
            item["houseUrl"] = house_url + "photo/d_house_" + data["picID"] + ".htm"
            item["salesStatus"] = data["status"]  # 在售状态
            item["roomNum"] = data["room"]  # 户型(房)
            item["hallNum"] = data["hall"]  # 户型(厅)
            item["toiletNum"] = data["toilet"]  # 户型(卫)
            item["constructSpace"] = data["buildingarea"]
            # item["price"] = data["toilet"]
            # item["propertyType"] = data["toilet"]
            # item["remark"] = data["toilet"]

            try:
                if "-" in data["reference_price"]:
                    lower_price, high_price = data["reference_price"].split("-")
                    data["reference_price"] = str((float(lower_price) + float(high_price)) / 2)
            except Exception as e:
                print(str(e))
            try:
                item["price"] = int(float(data["reference_price"]) / float(data["buildingarea"]) * 10000) if \
                    data["reference_price"] != "待定" and data["buildingarea"] != "待定" \
                    and data["reference_price"] and data["buildingarea"] \
                    and float(data["reference_price"]) and \
                    float(data["buildingarea"]) else None  # 参考均价
            except Exception as e:
                print(str(e))
            if not data["reference_price"]:
                item["totalPrices"] = ""
            elif data["reference_price"] == "待定":
                item["totalPrices"] = data["reference_price"]
            else:
                item["totalPrices"] = data["reference_price"] + "万元/套"
            houseapartment.append(dict(item))

        houseapartment = json.dumps(houseapartment, ensure_ascii=False)
        all_comment_dict.update({"houseapartment": houseapartment})
        yield all_comment_dict

    def parse_comments(self, response):
        # 解析评论
        url = response.url
        house = re.sub(r"dianping/", "", url)

        particulars = response.xpath("//*[@class='navleft tf']//a[contains(text(),'详情')]/@href|"
                                     "//*[@class='navleft tf']//a[contains(text(),'详细')]/@href").extract_first()
        particulars = u"https:" + particulars
        parameter = re.search(r"/(\d+)/", particulars).group(1)

        comments_data = response.xpath("//*[@id='dpCount']/text()").extract_first()
        comments_data = re.search(r"(\d+)", comments_data).group(1)
        comments_data = int(comments_data)
        port_url = house + "house/ajaxrequest/dianpingList_201501.php"  # pc端接口
        port = {
            "dianpingNewcode": str(parameter),
            "ifjiajing": "0",
            # "page": "1",
            "tid": "null",
            "pagesize": str(comments_data),
            "starnum": "6",
            "shtag": "-1",

        }
        yield scrapy.FormRequest(url=port_url, method="POST", formdata=port, callback=self.comment_port)  # 发送post请求

    def comment_port(self, response):
        item = DataCommentJson()
        url = response.url
        url = re.sub(r"house\/\w+\/\w+_\d+.php", "", url)
        all_comment_dict = {"_id": url}
        commentJson = []
        # datas = json.loads(response.body)["list"]
        datas = json.loads(response.text)["list"]
        # datas = json.loads(response.body.decode("gb18030"))
        for data in datas:
            item["source"] = "房天下"
            item["userNick"] = data["nickname"]
            if item["userNick"] == "":
                item["userNick"] = data["username"]
            item["content"] = data["content"]
            item["sourceUrl"] = url + "dianping/"
            item["createDate"] = data["create_time"]
            commentJson.append(dict(item))
        # commentJson = json.dumps(commentJson, ensure_ascii=False)
        all_comment_dict.update({"commentJson": commentJson})
        yield all_comment_dict

    def parse_dynamic(self, response):
        # 解析动态
        # dynamic_urls = []

        dynamic = response.xpath("//*[@class='navleft tf']//a[contains(text(),'首页')]/@href").extract()  # 楼盘首页
        dynamic = "".join(dynamic)
        _id = u"https:" + dynamic

        try:
            dynamic_url = response.xpath(
                '//div[@id="gushi_all"]//a[contains(text(),"详情")]/@href').extract()  # 获取动态里详情链接
            # dynamic_url = "".join(dynamic_url)
            if dynamic_url != None:
                for one_dynameic_url in dynamic_url:
                    one_dynameic_url = u"https:" + one_dynameic_url
                    # yield scrapy.Request(one_dynameic_url, callback=self.dynamic_particulars)
                    self.dynamic_urls.append(one_dynameic_url)

                the_next_page = response.xpath(
                    '//div[@id="gushi_all"]//li[@class="clearfix dbib"]//a[contains(text(),"下一页")]/@href').extract_first()  # 下一页

                if the_next_page is None:
                    url = self.dynamic_urls.pop()
                    yield scrapy.Request(url, callback=self.dynamic_particulars)
                else:
                    the_next_page = _id + the_next_page
                    yield scrapy.Request(the_next_page, callback=self.parse_dynamic)
        except Exception as e:
            pass

        # the_next_page = response.xpath('//div[@id="gushi_all"]//li[@class="clearfix dbib"]//a[contains(text(),"下一页")]/@href').extract_first()   # 下一页
        # print("0033",the_next_page)
        # if the_next_page != None:
        #     the_next_page = _id + the_next_page
        #     yield scrapy.Request(the_next_page,callback=self.parse_dynamic)

    def dynamic_particulars(self, response):
        item = DataDynamicJson()
        dynamic = response.xpath("//*[@class='navleft tf']//a[contains(text(),'首页')]/@href").extract()  # 楼盘首页
        dynamic = "".join(dynamic)
        _id = u"https:" + dynamic
        all_comment_dict = {"_id": _id}
        # dynamicJson = []
        url = response.url
        url = re.sub(r"\d+_\d+\.htm", "", url)
        dynamic_content = response.xpath("//div[@class='atc-wrapper']")
        for i in dynamic_content:
            item["soutse"] = "房天下"
            item["title"] = i.xpath("./h1/text()").extract_first()
            item["publishDate"] = i.xpath("./h2/text()[3]").extract_first()
            item['publishDate'] = re.search(r"\d+.*", item["publishDate"], re.S).group()  # 时间
            # item["publishDate"] = item["publishDate"].replace(" ", "")
            item["publishDate"] = item["publishDate"].replace("\n", "")
            item["publishDate"] = item["publishDate"].replace("\t", "")
            item["publishDate"] = item["publishDate"].replace("\r", "")
            # time = "".join(time)
            # data["publishDate"] =re.search(r"/d+.*",time,re.S).group()
            item["content"] = i.xpath(
                ".//p[@style='text-indent:2em;']//text()|//div[@class='leftboxcom']//text()").extract()
            item["content"] = "".join(item["content"])
            item["content"] = item["content"].replace(" ", "")
            item["content"] = item["content"].replace("\n", "")
            item["content"] = item["content"].replace("\t", "")
            item["content"] = item["content"].replace("\r", "")
            self.dynamicJson.append(dict(item))

        the_next_page1 = response.xpath('//div[@class="fy-wrapper"]/a[@class="xyp"]/@href').extract_first()
        the_next_page = url + the_next_page1

        if self.dynamic_urls == []:
            # if the_next_page1 == "javascript:void(0);":
            all_comment_dict.update({"dynamicJson": self.dynamicJson})
            yield all_comment_dict
            self.dynamicJson.clear()
        else:
            url = self.dynamic_urls.pop()
            yield scrapy.Request(url, callback=self.dynamic_particulars)

    def positioning(self, response):
        item = response.meta["item"]
        particulars = response.meta["xiangqing"]
        ditu = response.body.decode("utf8")
        # re_search = re.search(r'"mapx":"(.*?)","mapy":"(.*?)"', ditu, re.DOTALL)
        re_search = re.search(r'"mapx":"(\d+\.\d+)","mapy":"(\d+\.\d+)"', ditu, re.DOTALL)
        housecoord = re_search.group(2) + "," + re_search.group(1)
        item["housecoord"] = housecoord
        yield scrapy.Request(particulars, meta={"item": item}, callback=self.parse_particulars)

    def parse_particulars(self, response):
        # 解析详情页
        url = re.sub(r"house/\d+/\w+.htm", "", response.url)
        pattern = re.compile(r'\W+', re.S)
        html = response.body.decode("gb18030")
        soup = BeautifulSoup(html, "html.parser")
        html = etree.HTML(html)
        item = response.meta['item']
        item['housename'] = response.xpath('//*[@id="daohang"]//h1/a/text()').extract()  # 楼盘名称
        item['housename'] = "".join(item['housename'])
        try:
            housename2 = response.xpath('//*[@id="daohang"]//div/span/text()').extract()  # 楼盘别名
            housename2 = "".join(housename2)
            item['housename2'] = housename2[3:]  # 字符串切片去掉前面三个字符
            if not item['housename2']:
                item['housename2'] = ""
        except Exception as e:
            item['housename2'] = None
        houseproperty = response.xpath('//div[@class="lpicon tf"]//text()').extract()  # 楼盘标签
        houseproperty = [pattern.sub('', i) for i in houseproperty]
        re_houseproperty = []
        [re_houseproperty.append(i)
         for i in houseproperty if i]
        houseproperty = ",".join(re_houseproperty)  # 空格替换逗号
        houseproperty = "".join(houseproperty)
        item["houseproperty"] = houseproperty
        #  ---------------------------预售证------------------------
        try:
            basic_information = response.xpath(
                "//div//h3[contains(text(),'销售信息')]/..//div[@class='table-all']//tr[position()>1]")
            if basic_information == []:
                basic_information = response.xpath(
                    "//div//h3[contains(text(),'销售信息')]/..//div[@class='table-part']//tr[position()>1]")
        except Exception as e:
            basic_information = None
            pass
        all_comment_dict = {"_id": url}
        presale = []
        for i in basic_information:
            # 基本信息
            # data_lists = []
            data = {}
            # data = DataPresale()
            budgetLicence = i.xpath(".//td[1]/text()").extract()
            data['budgetLicence'] = "".join(budgetLicence)
            licenceDate = i.xpath(".//td[2]/text()").extract()
            data["licenceDate"] = "".join(licenceDate)  # 获取时间
            pattern = re.compile(r'(\d{4}).*?(\d{1,2}).*?(\d{1,2})')
            pattern_without_day = re.compile(r'(\d{4}).*?(\d{1,2})')
            if data["licenceDate"]:
                re_serch = pattern.search(data["licenceDate"])
                if re_serch:
                    start_year, start_month, start_day = re_serch.group(1), re_serch.group(2), re_serch.group(3)
                    start_month, start_day = start_month.rjust(2, '0'), start_day.rjust(2, '0')
                    data["licenceDate"] = start_year + "-" + start_month + "-" + start_day + " 00:00:00"
                else:
                    try:
                        re_serch = pattern_without_day.search(data["licenceDate"])
                        start_year, start_month = re_serch.group(1), re_serch.group(2)
                        start_month = start_month.rjust(2, '0')
                        data["licenceDate"] = start_year + "-" + start_month + "-01 00:00:00"
                    except:
                        pass
            # data['bindingHouse'] = i.find_element_by_xpath(".//td[3]").text
            bindingHouse = i.xpath(".//td[3]/text()").extract()
            data['bindingHouse'] = "".join(bindingHouse)
            # if not data['bindingHouse'] and not data["licenceDate"] and not data['budgetLicence']:
            #     continue
            # data_lists.append(data)
            presale.append(data)
        # presale = json.dumps(presale, ensure_ascii=False)
        all_comment_dict.update({"presale": presale})
        yield all_comment_dict
        #  ---------------预售证----------------------

        basic_information = response.xpath("//div[@class='main-left']")
        for i in basic_information:
            # 基本信息
            # item['_id'] = url  # 楼盘url
            item['source'] = "房天下"  # 来源
            item['allstatus'] = "1"  # 采集状态
            price = i.xpath('./div[1]//em/text()').extract()  # 均价
            price = ''.join(price)
            try:
                price = price.replace("\n", "")
                price = price.replace("\t", "")
                price = price.replace(" ", "")
            except Exception as e:
                pass
            try:
                item['houseprice'] = re.search(r"\d+.*", price, re.S).group()  # 取出数字及后面的字
            except Exception as e:
                item['houseprice'] = "待定"
            book_list = soup.find(attrs={"class": "main-left"})
            book_list_name = book_list.find_all("li")
            data_dict = {}
            for i in book_list_name:
                key = i.find(attrs={"class": "list-left"})
                try:
                    key = key.text
                except Exception as e:
                    pass
                value = i.find(attrs={"class": ["list-right", "list-right-text", "list-right-floor"]})  # 获取两个class名
                try:
                    value = value.text
                except Exception as e:
                    pass
                try:
                    key = key.replace(" ", "")
                    key = key.replace("\n", "")
                    key = key.replace("\t", "")
                except Exception as e:
                    pass
                try:
                    value = value.replace("\n", "")
                    # value = value.replace(" ", ",")
                    value = value.replace("\t", "")
                except Exception as e:
                    pass
                data_dict.update({key: value})
            # 基本信息
            if "物业类别：" in data_dict.keys():
                item['houseatr'] = data_dict["物业类别："]
                item['houseatr'] = item['houseatr'].replace(",", "")
                item['houseatr'] = item['houseatr'].replace(" ", "")
            if "建筑类别：" in data_dict.keys():
                item['housetype'] = data_dict["建筑类别："]
                item['housetype'] = item['housetype'].replace(" ", ",")
            elif "写字楼级别：" in data_dict.keys():
                item['housetype'] = data_dict["写字楼级别："]
                # item['housetype'] = item['housetype'].replace(" ", ",")
            if "产权年限：" in data_dict.keys():
                item['years'] = data_dict["产权年限："]
                item['years'] = item['years'].replace(",", "")
            if "装修状况：" in data_dict.keys():
                item['decoration'] = data_dict["装修状况："]
            if "开发商：" in data_dict.keys():
                item['developer'] = data_dict["开发商："]
            if "楼盘地址：" in data_dict.keys():
                item['houseaddress'] = data_dict["楼盘地址："]
            # 销售信息
            if "销售状态：" in data_dict.keys():
                item['salestatus'] = data_dict["销售状态："]
                item['salestatus'] = item['salestatus'].replace(" ", "")
            if "开盘时间：" in data_dict.keys():
                item['startSaleString'] = data_dict["开盘时间："]
            if "交房时间：" in data_dict.keys():
                item['endSaleString'] = data_dict["交房时间："]
            if "售楼地址：" in data_dict.keys():
                item['saleaddress'] = data_dict["售楼地址："]
            # 小区规划
            if "占地面积：" in data_dict.keys():
                landarea = data_dict["占地面积："]
                data_re = re.findall(r"\d+", landarea, re.S)  # 取出数字
                item['landarea'] = ("".join(data_re))  # 列表转字符串
            if "建筑面积：" in data_dict.keys():
                housearea = data_dict["建筑面积："]
                data_re = re.findall(r"[\d\.]+", housearea, re.S)  # 取出数字
                item['housearea'] = ("".join(data_re))  # 列表转字符串
            if "容积率：" in data_dict.keys():
                item['plotratio'] = data_dict["容积率："]
                item['plotratio'] = ''.join(item['plotratio'].split())
            if "绿化率：" in data_dict.keys():
                item['greenrate'] = re.sub(r'\%', '', data_dict["绿化率："])  # 去掉%
                if item['greenrate'] == "暂无资料":
                    item['greenrate'] = None
            if "停车位：" in data_dict.keys():
                item['carsite'] = data_dict["停车位："]
                try:
                    item['carsite'] = item['carsite'].replace("\r", "")
                    item['carsite'] = item['carsite'].replace("\n", "")
                    item['carsite'] = item['carsite'].replace("\t", "")
                    item['carsite'] = item['carsite'].replace(" ", "")
                except Exception as e:
                    pass
            elif "停车位配置：" in data_dict.keys():
                item['carsite'] = data_dict["停车位配置："]
                try:
                    item['carsite'] = item['carsite'].replace("\r", "")
                    item['carsite'] = item['carsite'].replace("\n", "")
                    item['carsite'] = item['carsite'].replace("\t", "")
                    item['carsite'] = item['carsite'].replace(" ", "")
                except Exception as e:
                    pass
            if "楼栋总数：" in data_dict.keys():
                housecount = data_dict["楼栋总数："]
                data_re = re.findall(r"\d+", housecount, re.S)  # 取出数字
                item['housecount'] = ("".join(data_re))  # 列表转字符串
                item['housecount'] = item['housecount'].replace(" ", "")
            elif "楼栋情况：" in data_dict.keys():
                item['housecount'] = data_dict["楼栋情况："]
                item['housecount'] = item['housecount'].replace(" ", "")
            if "总户数：" in data_dict.keys():
                allcount = data_dict["总户数："]
                data_re = re.findall(r"\d+", allcount, re.S)  # 取出数字
                item['allcount'] = ("".join(data_re))  # 列表转字符串
            if "物业公司：" in data_dict.keys():
                item['managecompany'] = data_dict["物业公司："]
            if "物业费：" in data_dict.keys():
                item['managefee'] = data_dict["物业费："]
                item['managefee'] = "".join(item['managefee'].split())  # 去掉\xa0字符
            if "楼层状况：" in data_dict.keys():
                item['floorCondition'] = data_dict["楼层状况："]

            item['fetch_time'] = str(datetime.now())  # 获取当前时间
            pattern = re.compile(r'(\d{4}).*?(\d{1,2}).*?(\d{1,2})')
            pattern_without_day = re.compile(r'(\d{4}).*?(\d{1,2})')

            if item['startSaleString']:
                re_serch = pattern.search(item["startSaleString"])
                if re_serch:
                    start_year, start_month, start_day = re_serch.group(1), re_serch.group(2), re_serch.group(3)
                    start_month, start_day = start_month.rjust(2, '0'), start_day.rjust(2, '0')
                    item["startsaletime"] = start_year + "-" + start_month + "-" + start_day + " 00:00:00"
                else:
                    try:
                        re_serch = pattern_without_day.search(item["startSaleString"])
                        start_year, start_month = re_serch.group(1), re_serch.group(2)
                        start_month = start_month.rjust(2, '0')
                        item["startsaletime"] = start_year + "-" + start_month + "-01 00:00:00"
                    except:
                        pass
            if item["endSaleString"]:
                re_serch = pattern.search(item["endSaleString"])
                if re_serch:
                    start_year, start_month, start_day = re_serch.group(1), re_serch.group(2), re_serch.group(3)
                    start_month, start_day = start_month.rjust(2, '0'), start_day.rjust(2, '0')
                    item["endsaletime"] = start_year + "-" + start_month + "-" + start_day + " 00:00:00"
                else:
                    try:
                        re_serch = pattern_without_day.search(item["endSaleString"])
                        start_year, start_month = re_serch.group(1), re_serch.group(2)
                        start_month = start_month.rjust(2, '0')
                        item["endsaletime"] = start_year + "-" + start_month + "-" + "-01 00:00:00"
                    except:
                        pass

            for key, value in item.items():
                if value and value.endswith(","):
                    item[key] = value[:-1]
                if value and type(value) == str and '[' in value:  # 去掉[]内的内容
                    item[key] = re.sub(r'[^\w]?\[.*?\]', '', value)
            yield item
