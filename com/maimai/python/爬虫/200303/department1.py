#-*- coding:utf8 -*-

import urllib.request
import ssl

# 处理HTTPS请求 SSL证书验证 忽略认证 比如12306 网站
url = "https://xingren.com/page/practice/location/cities?p=%E8%BE%BD%E5%AE%81%E7%9C%81"
header =  {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36"}



def total_page1(url):
    request = urllib.request.Request(url, headers=header)
    context = ssl._create_unverified_context()
    res = urllib.request.urlopen(request,context=context)
    print(res.read().decode("utf8"))


#主类
if __name__ == '__main__':
    print(total_page1(url))