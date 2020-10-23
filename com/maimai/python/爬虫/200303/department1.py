#-*- coding:utf8 -*-
import os,json
import urllib.parse
import ssl,csv
import urllib.request

path = 'D:\\study\\python-test\\file\department\\'

fileList = os.listdir(path)

url = 'https://xingren.com/page/ajax/clinic/search'

headers = ['province','city','district','hospitalName']

def filedel():
    for i in fileList:
        province = os.path.splitext(i)[0]
        filePathName = os.path.basename(path + i)
        pathName = path + i
        with open(r'%s' % (pathName), "r", encoding='gbk',errors='ignore') as f:
         result = json.load(f)
         for city in result['cities']:
             for area in result['cities'][city] :
                  print("查询信息", province, city, area)
                  request(province,city,area)


def request(province,city,district):
    data = params(province,city,district)
    data = urllib.parse.urlencode(data).encode()
    #print("连接信息", data)
    req = urllib.request.Request(url=url, headers=header())
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, data=data, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        result = json.loads(html)
        print(result['data'])
        resultList = result['data']
        for result in  resultList:
            each = {}
            each['province'] = province
            each['city'] = city
            each['district'] = district
            each['hospitalName'] = result['name']
            writeHospitalName(each)


def header() :
    header = {
        "Host": "xingren.com",
        "Content-Type": r"application/x-www-form-urlencoded;charset=UTF-8",
       # "Accept-Encoding":"gzip, deflate",
        "Accept":"*/*",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Proxy-Connection": "keep-alive",
        "Cookie": "PRIVDOC_SESSION=cb50787d0aafb6d621461200dc0dce69fd09270b-doctorId=204417552&appVersion=5.18.9; Hm_lvt_a1a382df8c3e81602f8d3b23c1c1257f=1583240657,1583245670; Hm_lpvt_a1a382df8c3e81602f8d3b23c1c1257f=1583245746",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 XRDoctor/5.18.9 NetType/WiFi Language/zh_CN",
        "X-Requested-With":"com.kanchufang.privatedoctor",
        "Origin":"https://xingren.com"
    }

    return header


def params(province,city,district):
    data = {}
    data['province'] = province
    data['city'] = city
    data['district'] = district

    return data

def writeHospitalName(each):
        print("write data", each)
        writer.writerow(each)


if __name__ == '__main__':
    f = open(r'D:\study\python-test\file\hospitalName.csv', 'a+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, headers)
    #writer.writeheader()
    print(filedel())

