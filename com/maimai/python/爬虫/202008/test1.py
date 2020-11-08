# -*- coding: utf-8 -*-
# @Time    : 2020/11/216:09
# @Author  : Terry Fu
# @File    : spider_bugumama
# @Desc    :
import requests
import csv
import json
import simplejson
import logging
from requests import exceptions
import traceback


def headers(yly_auth):
    headers = {
        'Host': 't-ylygw.doctopia.com.cn',
        'appid': 'D1C0haMwbmI0mbhl',
        'Accept': '*/*',
        'yly_auth': yly_auth,
        'Authorization': 'Ylytk 8888',
        'clientid': '1015',
        'Accept-Language': 'zh-cn',
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NvdW50SWQiOjEyNDU2ODQxNTYwNjYzOTQxMTMsInBob25lIjoiMTc2MjEzOTM5MzkiLCJpZGVudGl0eSI6ImNvbnN1bWVyIiwibmFtZSI6ImhvbWxlZSIsImV4cCI6MTYxMjU4Mjc3MSwiZnJvbUlkIjoxMDAxLCJpYXQiOjE2MDM5NDI3NzF9.Lil9v5ZMtgZj0kEkqaF9qbKrWs5ZslJ1FkgHK6C-2wFXUSJ5YlUVVSyfI0oVda7QieZgVPO0JRPkRXm4mgSGKA',
        'Content-Type': 'application/json',
        'Origin': 'https://officetmpapp.doctopia.com.cn',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 /sa-sdk-ios/sensors-verify/yilingyi.datasink.sensorsdata.cn?default',
        'Referer': 'https://officetmpapp.doctopia.com.cn/user-home-main/?one-sandbox=ios&v=1604470581'
    }
    return headers
def recommend_doctor_list():
    doctor_list = []
    url = "https://t-ylygw.doctopia.com.cn/yly-front/v1/doctor/recommendList"
    payload = {"current": 1, "isLogin": True, "size": 100}
    yly_auth = ['eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NvdW50SWQiOjEyNDU2ODQxNTYwNjYzOTQxMTMsInBob25lIjoiMTc2MjEzOTM5MzkiLCJpZGVudGl0eSI6ImNvbnN1bWVyIiwibmFtZSI6ImhvbWxlZSIsImV4cCI6MTYxMjU4Mjc3MSwiZnJvbUlkIjoxMDAxLCJpYXQiOjE2MDM5NDI3NzF9.Lil9v5ZMtgZj0kEkqaF9qbKrWs5ZslJ1FkgHK6C-2wFXUSJ5YlUVVSyfI0oVda7QieZgVPO0JRPkRXm4mgSGKA',
                'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NvdW50SWQiOjEzMjIwNTM4MTQ4OTc1Njk3OTQsInBob25lIjoiMTU4MjE1OTA4MzkiLCJpZGVudGl0eSI6ImNvbnN1bWVyIiwibmFtZSI6IuWtleWmiDA4MzkiLCJleHAiOjE2MTMxMzM1NzYsImZyb21JZCI6MTAxNSwiaWF0IjoxNjA0NDkzNTc2fQ.KhDZzlBXCHtbrtXZ_9aDVLYisjHGtwQhEt8hGpxLH-vPDjze6sB9kZ0X6czo8X1Ixe-35Kn1AMJCtTQvl1OMxQ']
    b = 0
    for auth in yly_auth:
      response = requests.post(url, headers=headers(auth), json=payload, timeout=10)
      try:
        if response.status_code != 200:
          return response.status_code, response.text
        else:
          content = response.content.decode('utf-8')
          con = json.loads(content)['data']['records']
      except exceptions.Timeout:
          return traceback.format_exc()
      except exceptions.HTTPError:
          return traceback.format_exc()
      except json.decoder.JSONDecodeError:
          return response.status_code, ''
      except simplejson.errors.JSONDecodeError:
          return response.status_code, ''
      except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise
      a = b
      for i in con:
        a += 1
        doctorId = i["accountId"]
        name = i["realName"]
        hospitalName = i["hospitalName"]
        departmentName = i['departmentName']
        body = str(a).strip() + '、 ' + doctorId + ' ' + name + ' ' + hospitalName + ' ' + departmentName
        doctor_list.append({
            "accountId": doctorId,
            "name": name,
            "hospitalName": hospitalName,
            "departmentName": departmentName
          })
        print(body)
      b = a + len(con)
    return doctor_list

def save_data():
    headers = ['accountId', 'name','hospitalName','departmentName']
    try:
      with open('test_dict.csv', 'w+', newline='', encoding='utf-8-sig') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(recommend_doctor_list())
    except:
      print(traceback.format_exc())
    finally:
      f.close()

if __name__ == '__main__':
    save_data()
