import urllib.parse
import ssl,json
from multiprocessing.dummy import Pool as ThreadPool,Lock,Manager
import  requests, json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import threading
import urllib,csv


#基础数据库
db = pm.connect(host='localhost', port=3306,
                     user='root', passwd='root', db='t_reptile', charset='utf8',cursorclass=pm.cursors.DictCursor)

# SQL 插入语句
sql = "select * from bohejiankang where food_detail is NULL"

#查询在表里的存在数据
delrepeatSql = "select * from bohejiankang where code in %s"

#查询基础数据
url = 'https://food.boohee.com/fb/v1/foods/fast_search'

# SQL 插入语句
insertsql = "INSERT INTO  bohejiankang (calory, weight, code, name, thumb_image_name, health_light, is_liquid) VALUES (%s,%s,%s,%s,%s,%s,%s)"

updateSql = "update bohejiankang set food_detail='{1}', ingredient_only='{2}' where id={0}"

#图片基础路径
baseurl = 'http://s.boohee.cn'

#食物详情
fooddeatiljson = 'https://food.boohee.com/fb/v1/foods/{0}.json'
#微量元素
ingredientjson = 'https://food.boohee.com/fb/v1/foods/{0}/ingredient_only.json '

dealresult = []


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
    finally:
        db.close()


def spider(search) :
    print("start deal: ", search)
    dealList = []
    data = params(search)
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

#查询参数
def params(search):
    data = {}
    data['q'] = search
    data['token'] = 'zkpD6bSgHZipXscYHVKZBKZfzyqTRDcf'
    data['user_key'] = '0342d302-62c6-4c98-82e9-72537d9d2d6c'
    data['app_device'] = 'Android'
    data['app_version'] = '7.1.8'
    data['os_version'] = '5.1.1'
    data['phone_model'] = 'hm note 1lte'
    data['channel'] = 'undefind'
    data['app_key'] = 'one'

    return data


#批量插入数据
def dealdata(data):
    print("start deal data")
    cursor = db.cursor()
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


def repeatCodes(codes):
    cursor = db.cursor()
    try:
        cursor.execute(delrepeatSql,codes)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        db.close()

def dealHttps(dealdata):
    for row in dealdata:
        print("deal data id: {0}, name:{1}, code:{2}".format(row[0], row[5], row[4]))
        each = {}
        id = row[0]
        code = row[4]
        name = row[5]
        each['id'] = id
        fooddeatil = urllib.request.urlopen(fooddeatiljson.format(code))
        each['food_detail'] = fooddeatil.read().decode('utf-8')
        ingredient = urllib.request.urlopen(ingredientjson.format(code))
        each['ingredient_only'] = ingredient.read().decode('utf-8')

        dealresult.append(each)

# dealHttpsByObj
def dealHttpsByObj(dealdata):
    for row in dealdata:
        each = {}
        id = row['id']
        code = row['code']
        name = row['name']
        each['id'] = id
        # each.append(code)
        # each.append(name)
        fooddeatil = urllib.request.urlopen(fooddeatiljson.format(code))
        each['food_detail'] = fooddeatil.read().decode('utf-8')
        ingredient = urllib.request.urlopen(ingredientjson.format(code))
        each['ingredient_only'] = ingredient.read().decode('utf-8')
        updateOneData(each)

# dealHttpsByObj
def batchDealHttpsByObj(row):
    each = {}
    id = row['id']
    code = row['code']
    name = row['name']
    each['id'] = id
    # each.append(code)
    # each.append(name)
    fooddeatil = urllib.request.urlopen(fooddeatiljson.format(code))
    each['food_detail'] = fooddeatil.read().decode('utf-8')
    ingredient = urllib.request.urlopen(ingredientjson.format(code))
    each['ingredient_only'] = ingredient.read().decode('utf-8')
    updateOneData(each)

# 例子
# UPDATE bohejiankang
#     SET ingredient_only = CASE id
#         WHEN 685 THEN 1.57
#         WHEN 686 THEN 1.58
#         WHEN 687 THEN 1.59
#     END
# WHERE id IN (685,686,687);
def batchUpdate():
    f = open(r"F:\python-test\file\json\batchUpdate.txt", 'r', encoding='utf8')
    res = f.readlines()
    datalen = len(res)
    # cursor = db.cursor()
    for i in range(0,42):
        sql1 = "UPDATE nine_tuple SET ingredient_only = CASE id "
        sql2 = "1"
        sql3 = ""
        for j in range(i*10000, (i+1)*10000):
            if j < datalen-1:
                r = res[j].split('\n')[0].split(';')
                ntid = int(r[0])
                f_senti_sala = float(r[1])
                sql3 += ' WHEN %d THEN %.1f' % (ntid, f_senti_sala)
                sql2 += ',' + str(ntid)
        sql = sql1 + sql3 +  ' END' + " WHERE id IN (%s)" % (sql2)
        print(sql)
    #     cursor.execute(sql)
    #     db.commit()
    # db.close()
    print('OK')

#批量更新数据
def updateBatchData(data):
    updateDb = pm.connect(host='localhost', port=3306,
                    user='root', passwd='root', db='t_reptile', charset='utf8', cursorclass=pm.cursors.DictCursor)
    # dealdata = tuple(tuple([y for y in x]) for x in data)
    print(data)
    cursor = updateDb.cursor()
    try:
        # 像sql语句传递参数
        for each in data:
            print(updateSql.format(each['id'], each['food_detail'], each['ingredient_only']))
            cursor.execute(updateSql.format(each['id'], each['food_detail'], each['ingredient_only']))
            # 提交
            updateDb.commit()
    except Exception as e:
        print(e)
        # 错误回滚
        updateDb.rollback()
    finally:
        updateDb.close()


# 批量更新数据
def updateOneData(each):
    updateOneDb = pm.connect(host='localhost', port=3306,
                          user='root', passwd='root', db='t_reptile', charset='utf8',
                          cursorclass=pm.cursors.DictCursor)
    # dealdata = tuple(tuple([y for y in x]) for x in data)
    cursor = updateOneDb.cursor()
    try:
        # 像sql语句传递参数
        print(updateSql.format(each['id'], each['food_detail'], each['ingredient_only']))
        cursor.execute(updateSql.format(each['id'], each['food_detail'], each['ingredient_only']))
        # 提交
        updateOneDb.commit()
    except Exception as e:
        print(e)
        # 错误回滚
        updateOneDb.rollback()
    finally:
        updateOneDb.close()

#主类
if __name__ == '__main__':
    pool = ThreadPool(8)
    #查询结果
    dbdata = select()
    print(len(dbdata))

    #更新数据
    dealresults = pool.map(batchDealHttpsByObj, dbdata)
