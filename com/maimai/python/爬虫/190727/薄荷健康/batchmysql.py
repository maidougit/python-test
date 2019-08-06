import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)


db = pm.connect(host='localhost', port=3306,
                     user='root', passwd='root', db='blog', charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO `blog`.`user` (`name`, `email`,`password`, `username`) VALUES (%s,%s,%s,%s)"
# 一个tuple或者list
T = (('xiaoming', 1, "31", 'boy'), ('hong',2, "32", 'girl'), ('wang', 3, "33", 'man'))

try:
    # 执行sql语句
    cursor.executemany(sql, T)
    # 提交到数据库执行
    db.commit()
except pm.Warning as w:
    print(repr(w))
    # 如果发生错误则回滚
    db.rollback()
# 关闭游标
cursor.close()
# 关闭数据库连接
db.close()
