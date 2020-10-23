#-*- coding:utf8 -*-

import urllib.parse
import ssl
import urllib.request
from urllib import parse
import json, csv
from multiprocessing.dummy import Pool as ThreadPool

#url = 'https://gw.xingren.com/consult/doctor/api/doctor/find?department=%s&ref=%s&province=%s&subDepartment=%s&page=1&limit=20&city=%s'

url = 'https://gw.xingren.com/consult/doctor/api/doctor/find?'

headers = [
    'doctorName',
    'avatar',
    'title',
    'department',
    'hospital',
    'metricskey1',
    'metricsval1',
    'metricskey2',
    'metricsval2',
    'consultPrice',
    'illnessKeywords',
    'tags'
]

def param(department,ref,province,page,limit,city):
    param = {
        "department":department,
        "ref":ref,
        "province":province,
        "page":page,
        "limit":limit,
        "city":city
    }

    return parse.urlencode(param)

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


doctor = {"儿科":["儿科综合","儿内科","小儿呼吸科","儿外科","小儿妇科","小儿皮肤科","小儿精神科","儿童保健科","儿童五官科"],"妇产科":[],"内科":["内科综合","呼吸内科","消化内科","神经内科","心血管内科","血液科","肾内科","内分泌科","风湿免疫科","其他内科"],"外科":["普外综合","肝胆外科","肛肠外科","甲状腺乳腺外科","血管外科","胸外科","心血管外科","神经外科","其他外科"],"精神科":[],"口腔科":[],"皮肤性病科":[],"泌尿外科/男科":[],"肿瘤科":[],"中医科":["中医综合科","中医内科","中医外科","中医妇科","中医生殖中心科","中医儿科","中医皮肤性病科","中医男科","中医骨科","中医康复理疗科","中医五官科","中医其他科","中西医结合科"],"骨科":[],"耳鼻喉头颈科":[],"整形美容科":[],"感染科/传染科":[],"眼科":[],"烧伤科":[],"结核病科":[],"营养科":[],"全科":[],"康复理疗科":[],"预防保健科":[],"其他":[]}


def get_content(url):
    req = urllib.request.Request(url=url, headers=header())
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req,context=context) as response:
       html = response.read()
       html = html.decode("utf-8")
       data = json.loads(html)
       total = data['data']['total']
       return total

# 计算页码
def calculationPage(total, limit=200):
    page = total / limit
    if isinstance(page, int):
        page
    else:
        page = int(page) + 1
    return page


def dealList(row):
    request(row["department"],row["ref"],row["province"],row["page"],row["limit"],row["city"],row["subDepartment"])

# 请求
def request(department,ref,province,page,limit,city,subDepartment):
    data = params(department,ref,province,page,limit,city,subDepartment)
    data = urllib.parse.urlencode(data)
    print("连接信息", data)
    req = urllib.request.Request(url=url+data, headers=header())
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)
        total = data['data']['total']
        pages = calculationPage(total)
        for i in range(1, pages):
          requestData(department,ref,province,i,limit,city, subDepartment)


# 处理数据
def requestData(department, ref, province, page, limit, city, subDepartment):
    data = params(department, ref, province, page, limit, city, subDepartment)
    data = urllib.parse.urlencode(data)
    req = urllib.request.Request(url=url + data, headers=header())
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)
        data = data['data']['doctors']
        dealData(data)

def dealData(data):
    for each in data:
     print(each)
     row = {}
     row['doctorName'] = each['doctorName']
     row['avatar'] = each['avatar']
     row['title'] = each['title']
     row['department'] = each['department']
     row['hospital'] = each['hospital']
     if each['metrics']:
         row['metricskey1'] = each['metrics'][0]['key']
         row['metricsval1'] = each['metrics'][0]['value']
         if len(each['metrics']) == 2:
             row['metricskey2'] = each['metrics'][1]['key']
             row['metricsval2'] = each['metrics'][1]['value']
         else:
             row['metricskey2'] = ''
             row['metricsval2'] = ''
     else:
         row['metricskey1'] = ''
         row['metricsval1'] = ''
         row['metricskey2'] = ''
         row['metricsval2'] = ''
     row['consultPrice'] = each['consultPrice']
     row['illnessKeywords'] = each['illnessKeywords']
     if len(each['tags']):
        tag = each['tags'][0]['value']
        tag = tag.replace(",","，")
        row['tags'] = tag
     else:
       row['tags'] = ''
     downloadDoctor(row)

# #将中文标点符号转换为英文标点符号
def C_trans_to_E(string):
    E_pun = u',.!?[]()<>"\''
    C_pun = u'，。！？【】（）《》“‘'
    #ord返回ASCII码对应的int
    #zip将合并为列表，元素为元祖，元祖为对应位置所有元素依次的集合，如这种形式[(',','，')...]
    #s生成对应字典
    table= {ord(f):ord(t) for f,t in zip(C_pun,E_pun)}
    #将字符传对应转换
    return string.translate(table)


def downloadDoctor(each):
    writer.writerow(each)

#第三方查询参数
def params(department,ref,province,page,limit,city,subDepartment):
    data = {
        "department": department,
        "ref": ref,
        "province": province,
        "page": page,
        "limit": limit,
        "city": city,
    }
    if subDepartment != 1:
        data['subDepartment'] = subDepartment
    return data

    #url = 'https://gw.xingren.com/consult/doctor/api/doctor/find?department=%s&ref=%2Fwap%2Fqie%2Fdoctor%2Ffind&province=%s&subDepartment=%s&page=1&limit=20&city=%s'

#主类
if __name__ == '__main__':
    f = open(r'F:\python-test\file\csv\doctor-20201023.csv', 'w+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    #param = request('儿科','/wap/qie/doctor/find','全国',1,10,'全省','儿科综合')
    list = []
    for k,v in doctor.items():
        if v:
           for item in v:
               data = {
                   "department": k,
                   "ref": '/wap/qie/doctor/find',
                   "province": '全国',
                   "page": 1,
                   "limit": 200,
                   "city": '全省',
                   "subDepartment": item
               }
               list.append(data)
        else:
            data = {
                "department": k,
                "ref": '/wap/qie/doctor/find',
                "province": '全国',
                "page": 1,
                "limit": 200,
                "city": '全省',
                "subDepartment": 1
            }
            list.append(data)
    print(list)
    pool = ThreadPool(3)
    dealresults = pool.map(dealList, list)
    pool.close()
    pool.join()
    f.close()