import urllib.parse
import ssl,json
from multiprocessing.dummy import Pool as ThreadPool,Lock,Manager
import  requests, json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import threading
import urllib


db = pm.connect(host='192.168.1.56', port=3306,
                     user='root', passwd='Yly,1O1', db='t_yly_reptile', charset='utf8')


#更新sql
sql_update ="update bohejiankang set food_detail = '{0}',ingredient_only='{1}' where id = {2}"

# 使用cursor()方法获取操作游标
cursor = db.cursor()

try:
    # 像sql语句传递参数
    cursor.execute(sql_update.format("2", '3', 342))
    # 提交
    db.commit()
except Exception as e:
    print(e)
    # 错误回滚
    db.rollback()
finally:
    db.close()