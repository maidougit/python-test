# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class QsbkPipeline(object):
    def __init__(self):
       # 可选实现
       self

    def process_item(self, item, spider):
        return item
