import requests,json


baseurl = 'http://s.boohee.cn'

with open(r"F:\python-test\file\json\zaocan.json","r",encoding='utf8') as f:
    result = json.load(f)
    for each in result:
        imagepath = baseurl + each['thumb_image_name']
        itemimage = each['thumb_image_name'].split('.')[-1]
        #print(imagepath, itemimage,each['name'])
        print('now downloading : ', each['name'])
        pic = requests.get(imagepath)
        fp = open('F:\\python-test\\file\\薄荷健康\\' + each['name'] + '.' + itemimage, 'wb')
        fp.write(pic.content)
        fp.close()
