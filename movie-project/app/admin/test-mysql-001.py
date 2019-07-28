#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
conn=pymysql.connect(host='rm-uf6og7m625tv8b174vo.mysql.rds.aliyuncs.com',port=3306,user='dbtest',password='Dbtest123',db='we888', charset='utf8')
# 创建游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

#有参数存储过程
cursor.execute("call create_calendar_day_new('ojl6X1NDYR4QX5RkDCGGp5sphBvo','2018-12-09','2018-12-22')")
conn.commit()
cursor.close()

print ('调用存储过程完毕................')
