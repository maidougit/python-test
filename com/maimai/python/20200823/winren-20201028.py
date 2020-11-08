import urllib.parse
import ssl
from multiprocessing.dummy import Pool as ThreadPool,Manager
import  json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import urllib
import urllib.request,csv


def db():
    db = pm.connect(host='192.168.1.56', port=3306,
                         user='root', passwd='Yly,1O1', db='xr-doctor-test', charset='utf8',cursorclass=pm.cursors.DictCursor)
    return db

# SQL 插入语句
sql = "select * from t_xr_doctor_list where introduction is null or honor is null or  serial is null"

#更新sql
sql_update ="update t_xr_doctor_list set goodAt = '{goodAt}',introduction='{introduction}', honor ='{honor}' where serial = {serial}"

requesturl = 'https://gw.xingren.com/consult/common/api/doctor/homepage/{serial}/intro'


headers=[
    "serial",
    "goodAt",
    "introduction",
    "honor"
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
        "Cookie": "PRIVDOC_SESSION=0996d38e890571c8e691a6b555367d5d8e90ad43-loginId=12500013; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2212500013%22%2C%22first_id%22%3A%221755007d0711e0-016a11056c8ed2-627b2550-332800-1755007d0731b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221755007d0711e0-016a11056c8ed2-627b2550-332800-1755007d0731b%22%7D",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 XRDoctor/5.18.9 NetType/WiFi Language/zh_CN",
        "X-Requested-With":"com.kanchufang.privatedoctor",
        "Origin":"https://xingren.com"
    }

    return header


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

#更新数据
def updateData(each):
    sdb2 = db()
    cursor = sdb2.cursor()
    try:
        # 像sql语句传递参数
        #sql_update = "update t_xr_doctor_list set goodAt = '{goodAt}',introduction='{introduction}', honor ='{honor}' where serial = {serial}"
        sql_update1 = sql_update.format(goodAt=each['goodAt'], introduction=each['introduction'], honor=each['honor'],
                          serial=each['serial'])
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


def request(serial):
    url = requesturl.format(serial=serial)
    req = urllib.request.Request(url=url, headers=header())
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)
        success = data["success"]
        print(data)
        if success:
            result = data["data"]
            if result:
                properties = result["properties"]
                print(properties)
                obj = {"serial":serial}
                for each in properties:
                    if each['key'] == '个人简介':
                        obj['introduction'] = each['value']
                    elif each['key'] == '擅长主治':
                        obj['goodAt'] = each['value']
                    elif each['key'] == '获得荣誉':
                        obj['honor'] = each['value']
                writer.writerow(obj)


#主方法
if __name__ == '__main__':
    list = []
    # 请求参数
    with open(r'F:\python-test\file\json\serival.json', 'r', encoding='gbk')as fp:
        json_data = json.load(fp)
        list = json_data['serial']
    print(list)
    f = open(r'f:\python-test\file\csv\doctor-20201028-0001.csv', 'w+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    #查询处理
    # list = select()
    pool = ThreadPool(8)
    request(list[0])
    # dealresults = pool.map(request, list)
    # pool.close()
    # pool.join()



