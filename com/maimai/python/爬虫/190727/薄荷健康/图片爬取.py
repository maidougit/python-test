import os
from urllib.request import urlretrieve
import requests
from multiprocessing.dummy import Pool as ThreadPool
import pymysql as pm
import string


os.makedirs('./image/', exist_ok=True)
basepath = "F:\\python-test\\com\\maimai\\python\\爬虫\\190727\\薄荷健康\\image\\";
IMAGE_URL = "http://image.nationalgeographic.com.cn/2017/1122/20171122113404332.jpg"

# SQL 插入语句
sql = "select * from bohejiankang"


def urllib_download(image_path, iamge_name):
    itemimage = "." + image_path.split('.')[-1]
    urlretrieve(image_path, basepath + iamge_name + itemimage)


def request_download(image_path, iamge_name):
    r = requests.get(image_path)
    itemimage = "." + image_path.split('.')[-1]
    with open(basepath + iamge_name +itemimage, 'wb') as f:
        f.write(r.content)


def chunk_download(image_path, iamge_name):
    itemimage = "." + image_path.split('.')[-1]
    r = requests.get(image_path, stream=True)
    with open(basepath + iamge_name + itemimage, 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)

#批量下载图片
def downloadImg(each):
    itemimage = each.split('/')[-1]
    print('now downloading: ', each)
    pic = requests.get(each)
    fp = open('F:\\python-test\\file\\image\\' + itemimage, 'wb')
    fp.write(pic.content)
    fp.close()


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
def batchDownloadImage(row):
   itemimage = row['name'] + "." + row['thumb_image_name'].split('.')[-1]
   itemimage = deal_image(itemimage)
   print("start download iamge  ", itemimage)
   pic = requests.get(row['thumb_image_name'])
   fp = open('F:\\python-test\\file\\image\\bohe1\\'  + itemimage, 'wb')
   fp.write(pic.content)
   fp.close()


def deal_image(each):
    str = eval(repr(each).replace("/", ""))
    str = str.replace(" ", "")
    return str

#主类
if __name__ == '__main__':
    goodDb = select()
    print(goodDb)
    pool = ThreadPool(8)
    dealresults = pool.map(batchDownloadImage, goodDb)
    pool.close()
    pool.join()
