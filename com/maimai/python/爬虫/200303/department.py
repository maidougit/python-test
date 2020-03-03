#-*- coding:utf8 -*-

import urllib.parse
import ssl
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import urllib.request,json
import urllib.request
from urllib.request import urlopen

url = 'https://xingren.com/page/practice/location/cities'


def header() :
    header = {
        "Host": "xingren.com",
        "Content-Type": r"application/x-www-form-urlencoded;charset=UTF-8",
        "Connection": "keep-alive",
        "Proxy-Connection": "keep-alive",
        "Cookie": "PRIVDOC_SESSION=cb50787d0aafb6d621461200dc0dce69fd09270b-doctorId=204417552&appVersion=5.18.9; Hm_lvt_a1a382df8c3e81602f8d3b23c1c1257f=1583240657,1583245670; Hm_lpvt_a1a382df8c3e81602f8d3b23c1c1257f=1583245746",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 XRDoctor/5.18.9 NetType/WiFi Language/zh_CN",
        "X-Requested-With":"com.kanchufang.privatedoctor"
    }

    return header

def get_content(url):
    #Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=header())
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req,context=context) as response:
       html = response.read()
       html = html.decode("utf-8")
       return html


def total_page1(search):
    data = params()
    url_para = urllib.parse.urlencode(data)
    full_url = url + '?' + url_para
    print("连接信息", full_url)
    return get_content(full_url)



#第三方查询参数
def params():
    data = {}
    data['p'] = "北京"
    data['c'] = "北京市"
    data['d'] = "石景山区"

    return data


#主类
if __name__ == '__main__':
    print(total_page1('辽宁省'))