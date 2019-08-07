import urllib.parse
import ssl,json
from multiprocessing.dummy import Pool as ThreadPool,Lock,Manager
import  requests, json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import threading

context = ssl._create_unverified_context()

#
jsonurl = 'https://food.boohee.com/fb/v1/foods/pingguo_junzhi.json'

url = 'https://record.boohee.com/api/v2/eatings/hot'
baseurl = 'http://s.boohee.cn'

db = pm.connect(host='localhost', port=3306,
                     user='root', passwd='root', db='blog', charset='utf8')

# SQL 插入语句
sql = "INSERT INTO blog.bohejiankang (food_id, calory, weight, code, name, thumb_image_name, health_light, is_liquid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

# 使用cursor()方法获取操作游标
cursor = db.cursor()
lock = threading.Lock()

list = []
def spider(page, lock='') :
    dealList = []
    print("deal data  ing ......" , page)
    data = {}
    data['page'] = page
    data['token'] = 'zkpD6bSgHZipXscYHVKZBKZfzyqTRDcf'
    data['user_key'] = '0342d302-62c6-4c98-82e9-72537d9d2d6c'
    data['app_device'] = 'Android'
    data['app_version'] = '7.1.8'
    data['os_version'] = '5.1.1'
    data['phone_model'] = 'hm note 1lte'
    data['channel'] = 'undefind'
    data['app_key'] = 'one'
    url_para = urllib.parse.urlencode(data)
    full_url = url + '?' + url_para
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(full_url, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)['foods']
        for each in data:
            array = []
            array.append(str(each['food_id']))
            array.append(str(each['calory']))
            array.append(str(each['weight']))
            array.append(str(each['code']))
            array.append(str(each['name']))
            array.append(str(baseurl + each['thumb_image_name']))
            array.append(str(each['health_light']))
            array.append(str(each['is_liquid']))
            dealList.append(array)
        #dealdata = tuple(tuple([y for y in x]) for x in list)
        #dealdata = tuple(list)
        list.append(dealList)
        #pymysql.err.ProgrammingError: (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'VALUES (1750,'241.0','100.0','dizhinailao','低脂奶酪',1,2,0),(872,'54.0','10' at line 1")
        # dealdata = tuple(tuple([y for y in x]) for x in dealList)
        # try:
        #     # 执行sql语句
        #     cursor.executemany(sql, dealdata)
        #     # 提交到数据库执行
        #     db.commit()
        # except pm.Warning as w:
        #     print(repr(w))
        #     # 如果发生错误则回滚
        #     db.rollback()
        # # 关闭游标
        # cursor.close()
        # # 关闭数据库连接
        # db.close()



def dealdata(data):
    print(len(data))

    dealdata = tuple(tuple([y for y in x]) for x in data)
    try:
        # 执行sql语句
        cursor.executemany(sql, dealdata)
        # 提交到数据库执行
        db.commit()
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        db.rollback()



if __name__ == '__main__':
    # pool = ThreadPool(4)
    # page = [x + 1 for x in range(18)]
    manager = Manager()
    lock = manager.Lock()
    # pool = ThreadPool(processes=8)
    for i in range(1, 20):
        # pool.apply_async(spider, (i, lock))
        spider(i)
    print(list)
    for i in list:
        if i == 21:
            continue
        else:
            dealdata(i)

    # results = pool.map(spider ,page)
    # pool.close()
    # pool.join()
    # 关闭游标
    cursor.close()
    # 关闭数据库连接
    db.close()