# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv,os
from .spiders.weiyi import logger



class FirstScrapyPipeline:
    def process_item(self, item, spider):
        return item


class WeiyiScrapyPipeline:
    def __init__(self):
        if os.path.exists('detail.csv') is False:
            # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
            self.f = open("detail.csv", "a", newline="", encoding='utf-8')
            # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
            self.fieldnames = ["id",
                               "tlDoctorName",
                               "provinceName",
                               "departmantName",
                               "teamDoctorActivityList",
                               "tlExpertPhoto",
                               "tlExpertUuid",
                               "totalConsultCount",
                               "totalOrderCount",
                               "provinceId",
                               "plusDemand",
                               "photo",
                               "name",
                               "link",
                               "isPlus",
                               "introduction",
                               "hospitalNameList",
                               "expertIdList",
                               "expertCount",
                               "diseaseMap",
                               "diseaseList",
                               "consultStarExpert",
                               "cityName",
                               "cityId",
                               "chatId",
                               "activityId"
                               ]
            # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
            self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
            # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
            self.writer.writeheader()
        else:
            os.remove("detail.csv")
            # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
            self.f = open("detail.csv", "a", newline="", encoding='utf-8')
            # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
            self.fieldnames = ["id",
                               "tlDoctorName",
                               "provinceName",
                               "departmantName",
                               "teamDoctorActivityList",
                               "tlExpertPhoto",
                               "tlExpertUuid",
                               "totalConsultCount",
                               "totalOrderCount",
                               "provinceId",
                               "plusDemand",
                               "photo",
                               "name",
                               "link",
                               "isPlus",
                               "introduction",
                               "hospitalNameList",
                               "expertIdList",
                               "expertCount",
                               "diseaseMap",
                               "diseaseList",
                               "consultStarExpert",
                               "cityName",
                               "cityId",
                               "chatId",
                               "activityId"
                               ]
            # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
            self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
            # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
            self.writer.writeheader()




    def process_item(self, item, spider):
        logger.warning('准备写数据:',item)
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.f.close()
