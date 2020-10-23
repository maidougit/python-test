# -*- coding:utf8 -*-
import random
import functools
from functools import reduce
import urllib.parse
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

dict1 = "find/url"
dict1 = parse.urlencode(dict1)
print(dict1)