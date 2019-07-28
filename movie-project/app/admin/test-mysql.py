#!/usr/bin/env python3
# coding:utf8
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://dbtest:Dbtest123@rm-uf6og7m625tv8b174vo.mysql.rds.aliyuncs.com:3306/yoytest", max_overflow=5)

result = engine.execute('select * from t_wx_doctor_info limit 1')
print(result.fetchall())