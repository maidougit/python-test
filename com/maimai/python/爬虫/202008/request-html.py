# -*- coding=utf8 -*-
import requests,json
from lxml import html




html1 = requests.get("https://www.guahao.com/expert/61410/%E5%A4%96%E7%A7%91/p2").text

selector=html.etree.HTML(html1)

result = selector.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li')

list_obj = []
for i in result:
    print(i)
