import re,requests


html = requests.get('https://www.wochu.cn/Product/CategoryGoods/6').text

content = re.findall('<ul>(.*?)</ul>', html, re.S)


src = content[0].replace('\r\n\t', '')

image = re.findall('src="(.*?)"', src, re.S)
print(image)

i = 0
for each in image:
    print('now downloading: ', each)
    pic = requests.get(each)
    fp = open('F:\\python-test\\file\\image\\' + str(i) + '.png', 'wb')
    fp.write(pic.content)
    fp.close()
    i += 1



