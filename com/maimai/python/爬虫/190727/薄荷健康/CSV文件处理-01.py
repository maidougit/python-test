import pymysql as pm
from multiprocessing.dummy import Pool as ThreadPool


# SQL 插入语句
sql = "select * from bohejiankang limit 10"

#查询
def select():
    selectDb = db();
    cursor = selectDb.cursor()
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        selectDb.close()


#数据库连接db
def db():
    db = pm.connect(host='localhost', port=3306,
                    user='root', passwd='root', db='t_reptile', charset='utf8', cursorclass=pm.cursors.DictCursor)
    return db


# dealHttpsByObj
def batchDealHttpsByObj(row):
   print(row['id'], row['name'], row['thumb_image_name'])


#主类
if __name__ == '__main__':
    goodDb = select()
    print(goodDb)

    pool = ThreadPool(8)

    dealresults = pool.map(batchDealHttpsByObj, goodDb)
    pool.close()
    pool.join()