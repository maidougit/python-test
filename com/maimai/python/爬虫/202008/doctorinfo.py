#-*- coding:utf8 -*-

import urllib.parse
import ssl
import urllib.request,json

url = 'https://gw.xingren.com/consult/doctor/api/doctor/find?department=%s&ref=%2Fwap%2Fqie%2Fdoctor%2Ffind&province=%s&subDepartment=%s&page=1&limit=20&city=%s'

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
       #data = json.loads(html)
       return html


def request(province,city,district):
    data = params(province,city,district)
    data = urllib.parse.urlencode(data).encode()
    print("连接信息", data)
    req = urllib.request.Request(url=url, headers=header())
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, data=data, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        result = json.loads(html)
        return result['data']



#第三方查询参数
def params(province,city,district):
    data = {}
    data['province'] = province
    data['city'] = city
    data['district'] = district

    return data


#主类
if __name__ == '__main__':
    #print(request('北京','北京市','西城区'));

    #url = 'https://gw.xingren.com/consult/doctor/api/doctor/find?department=%s&ref=%2Fwap%2Fqie%2Fdoctor%2Ffind&province=%s&subDepartment=%s&page=1&limit=20&city=%s'
    url = url % ("儿科", "全国", "儿科综合", "全省")
    print(url)

    # print(get_content(url))