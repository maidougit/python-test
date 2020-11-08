#-*- coding:utf8 -*-

import urllib.parse
import ssl
import urllib.request,json

url = 'https://xingren.com/wap/qie/doctor/list?department=%E5%84%BF%E7%A7%91&ref=/wap/qie/doctor/find&province=%E4%B8%8A%E6%B5%B7&city=%E4%B8%8A%E6%B5%B7%E5%B8%82'

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

# 中文编码
def urlencode(chinese_str):
    # 先进行gb2312编码
    chinese_str = chinese_str.encode('gb2312')
    # 输出 b'\xd6\xd0\xce\xc4'
    # 再进行urlencode编码
    return urllib.parse.quote(chinese_str)


#主类
if __name__ == '__main__':
    # url = 'https://xingren.com/wap/qie/doctor/list?department=%E5%84%BF%E7%A7%91&ref=/wap/qie/doctor/find&province=%E4%B8%8A%E6%B5%B7&city=%E4%B8%8A%E6%B5%B7%E5%B8%82'
    url % ("儿科", )

    print(get_content(url))