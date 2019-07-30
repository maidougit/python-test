from lxml import html
import requests, re

# 获取内容
content = requests.get('https://www.wochu.cn/Product/CategoryGoods/6').text
#etree 表达式
selector = html.etree.HTML(content)
#获取图片列表
image=selector.xpath('//div[contains(@class,"cgoods-item")]/ul/li/a/img/@src', stream=True) #这里使用id属性来定位哪个div和ul被匹配 使用text()获取文本内容
#下载图片
for each in image:
    itemimage = each.split('/')[-1]
    print('now downloading: ', each)
    pic = requests.get(each)
    fp = open('F:\\python-test\\file\\image\\' + itemimage, 'wb')
    fp.write(pic.content)
    fp.close()