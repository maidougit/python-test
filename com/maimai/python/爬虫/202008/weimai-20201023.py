#-*- coding:utf8 -*-

import urllib.parse
import ssl
import urllib.request
from urllib import parse
import json, csv
from urllib.request import Request, urlopen

#url = 'https://gw.xingren.com/consult/doctor/api/doctor/find?department=%s&ref=%s&province=%s&subDepartment=%s&page=1&limit=20&city=%s'

url = 'https://ichoice.myweimai.com/dprs/doctor/list?channelAlias=&channelSource=&channelPlatform=101'

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


headers = {
      'Host': 'ichoice.myweimai.com',
      'accept': 'application/json, text/plain, */*',
      'content-type': 'application/json;charset=utf-8',
      'x-weimai-token': '847ef151-fc0a-42ba-9568-ef5ee26ce63c',
      'origin': 'https://m.myweimai.com',
      'accept-language': 'zh-cn',
      'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 WeiMai/  WMAPP/6.3.1 (iOS 13.6.1; iPhone 8; Client Resident; Bridge 1.0.0; PayToken ; logid (null);)'
}


def paramData(pageIndex):
    data = {
        "filterParams": [
            {
                "type": "areaId",
                "value": "0"
            },
            {
                "type": "departmentId",
                "value": "0"
            },
            {
                "type": "pageIndex",
                "value": pageIndex
            }
        ],
        "sortParams": [
            {
                "type": "areaId",
                "value": "910500000001960199"
            }
        ]
    }

    return data

def paramData(pageIndex):
    data = {
        "filterParams": [
            {
                "type": "areaId",
                "value": "0"
            },
            {
                "type": "departmentId",
                "value": "0"
            },
            {
                "type": "pageIndex",
                "value": pageIndex
            }
        ],
        "sortParams": [
            {
                "type": "areaId",
                "value": "910500000001960199"
            }
        ]
    }

# 请求
def request():
    req = Request(url=url, data=json.dumps(paramData(1)).encode('utf-8'), headers=headers, method='POST')
    file_content = urlopen(req).read().decode('utf-8')
    return file_content


#主类
if __name__ == '__main__':
    print(request())
    # f = open(r'F:\python-test\file\csv\doctor-20201023.csv', 'w+', newline='', encoding='utf-8-sig')
    # writer = csv.DictWriter(f, headers)
    # writer.writeheader()
    # #param = request('儿科','/wap/qie/doctor/find','全国',1,10,'全省','儿科综合')
    # pool = ThreadPool(3)
    # dealresults = pool.map(dealList, list)
    # pool.close()
    # pool.join()
    # f.close()