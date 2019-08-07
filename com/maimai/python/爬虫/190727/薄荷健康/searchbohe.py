import urllib.parse
import ssl,json
from multiprocessing.dummy import Pool as ThreadPool,Lock,Manager
import  requests, json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import threading
import urllib,csv
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool
import  requests, json, sys,importlib


#基础数据库
db = pm.connect(host='192.168.1.56', port=3306,
                     user='root', passwd='Yly,1O1', db='t_yly_reptile', charset='utf8',cursorclass=pm.cursors.DictCursor)

# SQL 插入语句
sql = "select * from bohejiankang where food_id is not null and name != '猪肉馅' and name != '米饭' and name != '低脂奶酪'"

#查询基础数据
url = 'https://food.boohee.com/fb/v1/foods/fast_search'

# SQL 插入语句
insertsql = "INSERT INTO  bohejiankang (calory, weight, code, name, thumb_image_name, health_light, is_liquid) VALUES (%s,%s,%s,%s,%s,%s,%s)"

#图片基础路径
baseurl = 'http://s.boohee.cn'

# 使用cursor()方法获取操作游标
cursor = db.cursor()


finalList = []

#查询
def select():
    cursor = db.cursor()
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    # finally:
    #     db.close()


def spider(search) :
    print("start deal: ", search)
    dealList = []
    data = {}
    data['q'] = search
    data['token'] = 'DvXBAxh782XPWcWWaMeV8JizFwpWdVxj'
    data['user_key'] = '0342d302-62c6-4c98-82e9-72537d9d2d6c'
    data['app_device'] = 'Android'
    data['app_version'] = '7.1.8'
    data['os_version'] = '5.1.1'
    data['phone_model'] = 'redmi note 2'
    data['channel'] = 'undefind'
    url_para = urllib.parse.urlencode(data)
    full_url = url + '?' + url_para
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(full_url, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)['foods']
        for each in data:
            array = []
            #print(each)
            if(each['name'] != search):
                array.append(str(each['calory']))
                array.append(str(each['weight']))
                array.append(str(each['code']))
                array.append(str(each['name']))
                if(each['thumb_image_url']) is None:
                    array.append("1")
                else:
                   array.append(str(baseurl + each['thumb_image_url']))
                array.append(str(each['health_light']))
                array.append(str(each['is_liquid']))
                dealList.append(array)
        #批量保存数据
        finalList.append(dealList)
        # print(dealList)
        # dealdata(tuple(tuple([y for y in x]) for x in dealList))



#批量插入数据
def dealdata(data):
    print("start deal data")
    try:
        # 执行sql语句
        cursor.executemany(insertsql, data)
        # 提交到数据库执行
        db.commit()
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        db.rollback()

#名称
def nameList(dbdata):
    nameList = []
    for each in dbdata:
        nameList.append(each['name'])
    return nameList


#主类
if __name__ == '__main__':
    pool = ThreadPool(8)
    dbdata = select()
    #print(dbdata)
    dealNameList = nameList(dbdata)
    #print(dealNameList)
    dealresults = pool.map(spider, dealNameList)

    for data in finalList:
      dealdata(dealdata(tuple(tuple([y for y in x]) for x in data)))
      print(data)
    #查询处理
    #dealresults = pool.map(spider, ["米饭"])
    #result = spider("米饭")
    #print(result)
    pool.close()
    pool.join()
    db.close()