# -*- coding:utf8 -*-
import requests, json,csv

url = "http://47.112.136.39:94/v1/wxKeFu/createQRCode"  # 接口地址

headers = ['qrCodeStr','qrcodePath','url']

# 消息头数据


payload = {
    "qrCodeStr": "xibao_02",
    "appId": "wxd2fde4173472e6d3",
    "bucket": "ylyoss-app"
}


# verify = False 忽略SSH 验证
def delPost():
    headers1 = {
        'Connection': 'keep-alive',
        'Authorization': 'Ylytk MTAwMTo5bDdrNzJ6N2Ry'
    }
    for i in range(111):
        if i > 12:
            payload['qrCodeStr'] = 'xibao_' + str(i);
            print(payload)
            r = requests.post(url, json=payload, headers=headers1, verify=False).json()
            data = {}
            data['qrCodeStr'] = payload['qrCodeStr']
            data['qrcodePath'] = r['data']['qrcodePath']
            data['url'] = r['data']['url']
            writeHospitalName(data)

def writeHospitalName(each):
    print("write data", each)
    writer.writerow(each)

if __name__ == '__main__':
    f = open(r'D:\study\python-test\file\csv\qrCodeStr1.csv', 'a+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, headers)
    delPost()
