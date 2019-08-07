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
                     user='root', passwd='Yly,1O1', db='t_yly_reptile', charset='utf8')

# SQL 插入语句
insertsql = "INSERT INTO  bohejiankang (calory, weight, code, name, thumb_image_name, health_light, is_liquid) VALUES (%s,%s,%s,%s,%s,%s,%s)"

# 使用cursor()方法获取操作游标
cursor = db.cursor()


#批量插入数据
def dealdata(tupledata):
    try:
        # 执行sql语句
        cursor.executemany(insertsql, tupledata)
        # 提交到数据库执行
        db.commit()
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        db.rollback()




#主类
if __name__ == '__main__':

    data = (('125', '100', 'zamifan', '杂米饭', 'http://s.boohee.cnhttps://s.boohee.cn/house/upload_food/2016/9/5/mid_photo_url_2967203f131e40ee92a70435a212c686.jpg', '1', 'False'), ('94', '100', 'yumifan', '玉米饭', 'http://s.boohee.cnhttps://s.boohee.cn/house/upload_food/2008/9/17/96427_1221613705mid.jpg', '1', 'False'), ('173', '100', 'tianyuanboluochaomifan', '田园菠萝炒米饭', 'http://s.boohee.cnhttps://s.boohee.cn/house/upload_food/2009/2/8/156362_1234107492mid.jpg', '2', 'False'), ('188', '100', 'shijinchaofan', '炒饭', 'http://s.boohee.cnhttps://s.boohee.cn/house/new_food/mid/956d967b624f43d39140d3bedd720f10.jpg', '2', 'False'))
    dealdata(data)
    db.close()