# -*- coding:utf8 -*-
import json, csv
from urllib.request import Request, urlopen
from multiprocessing.dummy import Pool as ThreadPool
import pymysql as pm
import logging



#日志文件
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename=r'D:\study\python-test\file\log\20201103-001.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )


url = "https://ichoice.myweimai.com/dprs/doctor/list?channelAlias=&channelSource=&channelPlatform=101"

detail_url = "https://ichoice.myweimai.com/dprs/doctor/search"


doctor_detail_url = "https://ichoice.myweimai.com/dprs/doctor/detail?channelPlatform=101&doctorId={doctorId}"


# 城市请求
city_url = "https://ichoice.myweimai.com/dprs/doctor/paramlist?channelAlias=&channelSource=&channelPlatform=101"

doctor_list_url = ""

headers = {
    'Host': 'ichoice.myweimai.com',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=utf-8',
    'x-weimai-token': '847ef151-fc0a-42ba-9568-ef5ee26ce63c',
    'origin': 'https://m.myweimai.com',
    'accept-language': 'zh-cn',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 WeiMai/  WMAPP/6.3.1 (iOS 13.6.1; iPhone 8; Client Resident; Bridge 1.0.0; PayToken ; logid (null);)',
    'referer': 'https://m.myweimai.com/new/dpr/doctorlist.html?filterParams=areaId0departmentId20&sortParams=areaId910500000001960199&from=3'
}

depatemant_id_list = [20, 26, 22, 45, 21]

# csv 头信息
csvheaders = [
    "adviceCount",
    "currencyFrom",
    "departId",
    "departName",
    "doctorAvatar",
    "doctorId",
    "doctorLabels",
    "doctorName",
    "doctorUserId",
    "employeeId",
    "favorableRate",
    "hospitalId",
    "hospitalName",
    "ifCrown",
    "itemId",
    "packageId",
    "price",
    "professionTitleCode",
    "replyRate",
    "skill",
    "skuId",
    "stdDepartCode",
    "titleName",
    "cityName"
]


# 参数
def paramData(page):
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
                "value": page
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


# 城市请求参数
def city_request():
    return {"filterParams": [{"type": "areaId", "value": "0"}],
            "sortParams": [{"type": "areaId", "value": "910500000001960199"}]}


# 查询参数列表
def doctor_list(areaId, departmentId):
    param = {
        "filterParams": [
            {"type": "areaId", "value": areaId},
            {"type": "departmentId", "value": departmentId}
        ],
        "sortParams":
            [
                {"type": "areaId", "value": "910500000001960199"}
            ]
    }

    return param


# 明细请求
def detailParam(page, keyWord):
    param = {
        "channelAlias": '',
        "channelSource": '',
        "channelPlatform": 101,
        "areaId": 910500000001960199,
        "pageIndex": page,
        "pageSize": 10,
        "keyWord": keyWord
    }

    return param

# 请求参数列表
def doctor_param_list():
    request_city_list_param = requestCityList()["city"]
    department_id_list_param = depatemant_id_list
    param_list = []
    for city in request_city_list_param:
        for department_id in department_id_list_param:
            param = {
                "areaId": city['id'],
                "departmentId":department_id,
                "cityName":city['name']
            }

            param_list.append(param)
    return param_list

# 处理请求
def request(page):
    req = Request(url=url, data=json.dumps(paramData(page)).encode('utf-8'), headers=headers, method='POST')
    file_content = urlopen(req).read().decode('utf-8')
    data = json.loads(file_content)
    dealData(data['data'])

# 医生列表信息
def request_doctor_list(row):
    req = Request(url=url, data=json.dumps(doctor_list(row['areaId'], row['departmentId'])).encode('utf-8'), headers=headers, method='POST')
    file_content = urlopen(req).read().decode('utf-8')
    data = json.loads(file_content)
    # print(json.dumps(data))
    deal_doctor_list(data['data'], row['cityName'])
    # dealData(data['data'])

# 明细请求 dumps 将结果转换成json
def requestDetail(page, keyWord):
    req = Request(url=url, data=json.dumps(detailParam(page, keyWord)).encode('utf-8'), headers=headers, method='POST')
    file_content = urlopen(req).read().decode('utf-8')
    data = json.loads(file_content)
    print(json.dumps(data))

# 处理请求
def request_doctor_detail(item):
    doctorId = item['doctorId']
    req = Request(url=doctor_detail_url.format(doctorId=doctorId), headers=headers, method='GET')
    file_content = urlopen(req).read().decode('utf-8')
    data = json.loads(file_content)
    # 记录日志
    logging.info(json.dumps(data))
    data = data['data']
    row = {}
    if data:
        row['doctorId'] = doctorId
        row['fansCount'] = data['fansCount']
        row['favorableRate'] = data['favorableRate']
        row['professionCode'] = data['professionCode']
        row['professionName'] = data['professionName']
        row['adviceNum'] = data['adviceNum']
        row['registionCount'] = data['registionCount']
        row['is_deal'] = 1
        #更新
        updateData(row)


# 城市 列表信息
def requestCityList():
    city_row = {}
    req = Request(url=city_url, data=json.dumps(city_request()).encode('utf-8'), headers=headers, method='POST')
    file_content = urlopen(req).read().decode('utf-8')
    data = json.loads(file_content)['data']
    city_row['type'] = data['type']
    city_row['value'] = data['value']
    list_parent = data['paramResList']
    city_list = []
    for each_parent in list_parent:
        list_item = each_parent['child']
        for item in list_item:
            row = {}
            if item['name'] == '全国':
                continue
            else:
                row['name'] = item['name']
                row['id'] = item['id']
                city_list.append(row)
    city_row['city'] = city_list
    return city_row


def deal_doctor_list(data, cityName):
    for each in data:
        row = {}
        row["adviceCount"] = each["adviceCount"]
        row["currencyFrom"] = each["currencyFrom"]
        row["departId"] = each["departId"]
        row["departName"] = each["departName"]
        row["doctorAvatar"] = each["doctorAvatar"]
        row["doctorId"] = each["doctorId"]
        if each["doctorLabels"]:
            row["doctorLabels"] = each["doctorLabels"]
        else:
            row["doctorLabels"] = ''
        row["doctorName"] = each["doctorName"]
        row["doctorUserId"] = each["doctorUserId"]
        row["employeeId"] = each["employeeId"]
        row["favorableRate"] = each["favorableRate"]
        row["hospitalId"] = each["hospitalId"]
        row["hospitalName"] = each["hospitalName"]
        row["ifCrown"] = each["ifCrown"]
        row["itemId"] = each["itemId"]
        row["packageId"] = each["packageId"]
        row["price"] = each["price"]
        if each["professionTitleCode"]:
            row["professionTitleCode"] = each["professionTitleCode"]
        else:
            row["professionTitleCode"] = ''
        row["replyRate"] = each["replyRate"]
        if each["skill"]:
            row["skill"] = each["skill"]
        else:
            row["skill"] = ''
        row["skuId"] = each["skuId"]
        if each["stdDepartCode"]:
            row["stdDepartCode"] = each["stdDepartCode"]
        else:
            row["stdDepartCode"] = ''
        if each["titleName"]:
            row["titleName"] = each["titleName"].strip().replace("\r\n", "").replace(" ", "")
        row['cityName'] = cityName
        downloadWeimai(row)

# 处理数据
def dealData(data):
    for each in data:
        row = {}
        row["adviceCount"] = each["adviceCount"]
        row["currencyFrom"] = each["currencyFrom"]
        row["departId"] = each["departId"]
        row["departName"] = each["departName"]
        row["doctorAvatar"] = each["doctorAvatar"]
        row["doctorId"] = each["doctorId"]
        if each["doctorLabels"]:
            row["doctorLabels"] = each["doctorLabels"]
        else:
            row["doctorLabels"] = ''
        row["doctorName"] = each["doctorName"]
        row["doctorUserId"] = each["doctorUserId"]
        row["employeeId"] = each["employeeId"]
        row["favorableRate"] = each["favorableRate"]
        row["hospitalId"] = each["hospitalId"]
        row["hospitalName"] = each["hospitalName"]
        row["ifCrown"] = each["ifCrown"]
        row["itemId"] = each["itemId"]
        row["packageId"] = each["packageId"]
        row["price"] = each["price"]
        if each["professionTitleCode"]:
            row["professionTitleCode"] = each["professionTitleCode"]
        else:
            row["professionTitleCode"] = ''
        row["replyRate"] = each["replyRate"]
        if each["skill"]:
            row["skill"] = each["skill"]
        else:
            row["skill"] = ''
        row["skuId"] = each["skuId"]
        if each["stdDepartCode"]:
            row["stdDepartCode"] = each["stdDepartCode"]
        else:
            row["stdDepartCode"] = ''
        if each["titleName"]:
            row["titleName"] = each["titleName"].strip().replace("\r\n", "").replace(" ", "")
        downloadWeimai(row)


def C_trans_to_E(string):
    E_pun = u',.!?[]()<>"\''
    C_pun = u'，。！？【】（）《》“‘'
    # ord返回ASCII码对应的int
    # zip将合并为列表，元素为元祖，元祖为对应位置所有元素依次的集合，如这种形式[(',','，')...]
    # s生成对应字典
    table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    # 将字符传对应转换
    return string.translate(table)


def downloadWeimai(each):
    print(each)
    # writer.writerow(each)


def db():
    db = pm.connect(host='192.168.1.56', port=3306,
                         user='root', passwd='Yly,1O1', db='xr-doctor-test', charset='utf8',cursorclass=pm.cursors.DictCursor)
    return db

#查询
def select():
    sdb1 = db()
    cursor = sdb1.cursor()
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        sdb1.commit()
        return results
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        sdb1.rollback()
    finally:
        sdb1.close()

# SQL 插入语句
sql = "select * from t_wm_doctor_list_1030 where is_deal = 0"

#更新sql
sql_update ="update t_wm_doctor_list_1030 set favorableRate = '{favorableRate}',registionCount='{registionCount}', adviceNum ='{adviceNum}', fansCount = '{fansCount}' where doctorId = {doctorId}"


#更新数据
def updateData(each):
    sdb2 = db()
    cursor = sdb2.cursor()
    try:
        # 像sql语句传递参数
        sql_update = "update t_wm_doctor_list_1030 set favorableRate = '{favorableRate}',registionCount='{registionCount}', adviceNum ='{adviceNum}', fansCount = '{fansCount}', professionName='{professionName}', is_deal = 1 where doctorId = {doctorId}"
        sql_update1 = sql_update.format(favorableRate=each['favorableRate'], registionCount=each['registionCount'],
                                        adviceNum=each['adviceNum'],fansCount=each['fansCount'],professionName=each['professionName'],doctorId=each['doctorId'])
        print(sql_update1)
        cursor.execute(sql_update1)
        # 提交
        sdb2.commit()
    except Exception as e:
        # 错误回滚
        print(e)
        sdb2.rollback()
    finally:
        sdb2.close()

if __name__ == '__main__':
    # f = open(r'D:\study\python-test\file\csv\weiwei-20201030-003.csv', 'w+', newline='', encoding='utf-8')
    # writer = csv.DictWriter(f, csvheaders)
    # writer.writeheader()
    # # list = range(1,2)
    list_doctor = select()
    pool = ThreadPool(8)
    pool.map(request_doctor_detail, list_doctor)
    pool.map(request_doctor_list, doctor_param_list())
    pool.close()
    pool.join()
    # f.close()
    # requestDetail(1, "四川")
    #print(len(doctor_param_list()))
    #request_doctor_list(doctor_param_list()[1])
    # request_doctor_detail(1523223086558720002)

    # list_doctor = select()
    # request_doctor_detail(list_doctor[0])
