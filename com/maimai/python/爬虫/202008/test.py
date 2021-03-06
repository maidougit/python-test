# -*- coding:utf8 -*-
import random
import functools
from functools import reduce
import urllib.parse,json,io
from urllib import parse


result =  list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

print(result)


def add(x, y):
  return x + y


reduceResult = reduce(add, [1, 3, 5, 7, 9])

print(reduceResult)


DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))



chinese_str = '中文'
# 先进行gb2312编码
chinese_str = chinese_str.encode('gb2312')
# 输出 b'\xd6\xd0\xce\xc4'
# 再进行urlencode编码
chinese_str_url = urllib.parse.quote(chinese_str)
# 输出 %D6%D0%CE%C4
print(chinese_str_url)


# with open("area.json",'r') as load_f:
#     area_id = []
#     load_dict = json.load(load_f)
#     for each in load_dict:
#         print(each)
#         if 'cities' in each:
#             for item in each['cities']:
#               area_id.append({"areaId":item['areaId']})
#         else:
#             area_id.append({"areaId":each['areaId']})
#
#     print(json.dumps(area_id))


depart_ment = ['儿科', '皮肤科', '妇产科', '口腔科','新生儿科']

base_url = "https://www.guahao.com/json/white/search/eteams?q=&dept={dept}&page=1&cid=&pid=&_=1604828782843"

base_url_list = []
for each  in depart_ment:
    base_url_list.append(base_url.format(dept=each))
print(json.dumps(base_url_list))

# with open("area_id.json", 'r') as load_f:
#     result_list = []
#     load_dict = json.load(load_f)
#     for each in load_dict:
#         for item in depart_ment:
#             result_list.append({"areaId":each['areaId'],"department":item})
#
# print(result_list)
# base_url_list = []
# for each in result_list:
#     base_url_list.append(base_url.format(dept=each['department'], cid=each['areaId']))
#
# print(json.dumps(base_url_list))
#
#
# with open("start_url.json", 'r') as load_f:
#     load_dict = json.load(load_f)
#     print(load_dict)
#
# list = io.open(r"start_url.json", "r", encoding="gbk")
# print(list[0])

# 儿科   https://www.guahao.com/expert/61412/%E5%84%BF%E7%A7%91            9962
# 妇产科 https://www.guahao.com/expert/61411/%E5%A6%87%E4%BA%A7%E7%A7%91   12135
# 口腔科 https://www.guahao.com/expert/61416/%E5%8F%A3%E8%85%94%E7%A7%91   4164
# 皮肤科 https://www.guahao.com/expert/61413/%E7%9A%AE%E8%82%A4%E7%A7%91   3353
base_url = ["https://www.guahao.com/expert/61412/%E5%84%BF%E7%A7%91/p{page}",
            "https://www.guahao.com/expert/61411/%E5%A6%87%E4%BA%A7%E7%A7%91/p{page}",
            "https://www.guahao.com/expert/61416/%E5%8F%A3%E8%85%94%E7%A7%91/p{page}",
            "https://www.guahao.com/expert/61413/%E7%9A%AE%E8%82%A4%E7%A7%91/p{page}"
            ]

start_url = []

for i in range(1,39):
    for item in base_url:
        start_url.append(item.format(page=i))

print(json.dumps(start_url))

