import requests,json
from lxml import html,re


# https://food.boohee.com/fb/v1/foods/dizhinailao.json
#先抓大在抓小
url = "http://www.boohee.com/food/group/1"
html = requests.get(url).text

selector=html.etree.HTML(html)

content=selector.xpath('//div[@class="food-list"]/li/text()')
#content = re.findall('<ul >(.*?)</ul>', html, re.S)
src = content[0].replace('\r\n\t', '')
image = re.findall('src="(.*?)"', src, re.S)
good_name = re.findall('class="goods-name">(.*?)</div>', src, re.S)