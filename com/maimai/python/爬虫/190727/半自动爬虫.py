import re,requests


f = open(r"F:\python-test\file\source.txt",'r', encoding="utf8",errors='ignore')
html = f.read()
f.close()

i = 0
pic_url = re.findall('img src="(.*?)" class="lessonimg"', html, re.S)
#删除第一行数字
del pic_url[0]
#print(pic_url)
for each in pic_url:
    print('now downloading: ', each)
    pic = requests.get(each)
    fp = open('F:\\python-test\\file\\' + str(i) + '.png', 'wb')
    fp.write(pic.content)
    fp.close()
    i += 1


#print(html)