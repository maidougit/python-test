import urllib.parse
import ssl,json
from multiprocessing.dummy import Pool as ThreadPool,Lock,Manager
import  requests, json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import threading
import urllib,csv


#食物详情
fooddeatiljson = 'https://food.boohee.com/fb/v1/foods/{0}.json'
#微量元素
ingredientjson = 'https://food.boohee.com/fb/v1/foods/{0}/ingredient_only.json '


db = pm.connect(host='192.168.1.56', port=3306,
                     user='root', passwd='Yly,1O1', db='t_yly_reptile', charset='utf8')

# SQL 插入语句
sql = "select * from bohejiankang"

#更新sql
sql_update ="update bohejiankang set food_detail = '{0}',ingredient_only='{1}' where id = {2}"

# 使用cursor()方法获取操作游标

dealresult = []

headers = ['id','food_detail','ingredient_only']

#查询
def select():
    cursor = db.cursor()
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
        # print("id", "code", "name")
        # print(results)
        # # # 遍历结果
        # for row in results:
        #     id = row[0]
        #     code = row[4]
        #     name = row[5]
        #     print(id, code, name)
    except Exception as e:
        raise e
    finally:
        db.close()

#更新数据
def updateData(dealdata):
    cursor = db.cursor()
    try:
        for each in dealdata:
            print("start update data:{0},{1},{2}".format( each[0], each[1], each[1]))
            # 像sql语句传递参数
            print(sql_update.format(each[1], each[2], each[0]))
            cursor.execute(sql_update.format(each[1], each[2], each[0]))
            # 提交
            db.commit()
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def dealHttps(dealdata):
    for row in dealdata:
        print("deal data id: {0}, name:{1}, code:{2}".format(row[0],row[5],row[4]) )
        each = []
        id = row[0]
        code = row[4]
        name = row[5]
        each.append(id)
        ingredient = urllib.request.urlopen(ingredientjson.format(code))
        each.append(ingredient.read().decode('utf-8'))
        fooddeatil = urllib.request.urlopen(fooddeatiljson.format(code))
        each.append(fooddeatil.read().decode('utf-8'))
        dealresult.append(each)

def downloadImage(list):
    headers = ['id', 'food_detail', 'ingredient_only']
    with open(r'D:\pyproject\pystudy\file\bohe\bohe.csv', 'w', newline='',encoding='utf-8-sig') as f:
        print('now writing data 112345')
        # writer = csv.writer(f, headers)
        # writer.writeheader()
        writer = csv.writer(f, delimiter=' ')
        for each in list:
            writer.writerow(each)


#主方法
if __name__ == '__main__':
    #查询处理
    result = select()

    #请求数据处理
    dealHttps(result)

    #转换元组合
    #dealdata = tuple(tuple([y for y in x]) for x in dealresult)

    #print(dealresult)
    #更新数据
    downloadImage(dealresult)

    # print(result)



