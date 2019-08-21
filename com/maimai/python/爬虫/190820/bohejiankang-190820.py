import urllib.parse
import ssl,json
from multiprocessing.dummy import Pool as ThreadPool,Lock,Manager
import  requests, json
import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)
import threading
import urllib,csv,re
import uuid
from xpinyin import Pinyin
import logging
import redis
import random



#日志文件
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename=r'F:\python-test\file\image\log\record-190810-004.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )


# SQL 插入语句
sql = "select * from bohejiankang limit 1"

#查询在表里的存在数据
delrepeatSql = "select * from bohejiankang where code in %s"

#查询基础数据
url = 'https://food.boohee.com/fb/v1/foods/search'

# SQL 插入语句
insertsql = "INSERT INTO  bohejiankang (calory, weight, code, name, thumb_image_name, health_light, is_liquid) VALUES (%s,%s,%s,%s,%s,%s,%s)"

updateSql = "update bohejiankang set food_detail='{1}', ingredient_only='{2}' where id={0}"

#图片基础路径
baseurl = 'http://s.boohee.cn'

#食物详情
fooddeatiljson = 'https://food.boohee.com/fb/v1/foods/{0}.json'
#微量元素
ingredientjson = 'https://food.boohee.com/fb/v1/foods/{0}/ingredient_only.json '

#合计文字而为数组
chinese_array = []


#查询
def select():
    sdb = db()
    cursor = sdb.cursor()
    sql = 'select id, name,code from bohejiankang'
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        sdb.close()


#提取中文
def chinese(word):
    p = re.compile(r'[\u4e00-\u9fa5]')
    res = re.findall(p, word)
    result = ''.join(res)
    return  result


#中文文字拆分
def split_chinese(chinese):
    # text = unicode(chinese, 'utf-8')
    chinese = u'{0}'.format(chinese)
    chinesearrar = []
    for i in chinese:
        chinesearrar.append(i)
    return chinesearrar

# 数据库连接db
# def db():
#     db = pm.connect(host='192.168.1.56', port=3306,
#                     user='root', passwd='Yly,1O1', db='t_yly_reptile', charset='utf8',cursorclass=pm.cursors.DictCursor)
#     return db

# def db():
#     db = pm.connect(host='localhost', port=3306,
#                     user='root', passwd='root', db='t_yly_reptie', charset='utf8',cursorclass=pm.cursors.DictCursor)
#     return db

def db():
    db = pm.connect(host='localhost', port=3306,
                     user='root', passwd='root', db='t_reptile', charset='utf8',cursorclass=pm.cursors.DictCursor)

    return db


def deal_db_chinese(list):
    for each in list:
        result =  split_chinese(chinese(each['name']))
        chinese_array.append(result)

#第三方查询参数
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

    return data

#获取当前总页数
def total_page(search):
    data = params(search)
    url_para = urllib.parse.urlencode(data)
    full_url = url + '?' + url_para
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(full_url, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)
        return  data['total_pages']

# 批处理
def spider(search) :
    p = Pinyin()
    red = redis_connect()
    name = p.get_pinyin(u'{0}'.format(search))
    if red.exists('name:{0}'.format(name)):
        logging.info("已搜索: " + 'name:{0}'.format(name))
    else:
        print("start deal: ", search)
        totalpage = total_page(search)
        p = Pinyin()
        red = redis_connect()
        name = p.get_pinyin(u'{0}'.format(search))
        red.set('page:{0}'.format(name), totalpage)
        if totalpage == 1:
            batch_page(1, search, totalpage)
        else:
            for page in range(1, totalpage+1):
                batch_page(page, search, totalpage)
        #         batch_deal_data(dealList)
        # #更新搜索结果
        update_search(search)



def spiderdata(search) :
    if select_search(search) is not None:
        print("this is search having done")
        return
    else:
        print("start deal: ", search)
        totalpage = total_page(search)
        pages = array_page(totalpage, search)

        dealpool = ThreadPool(4)

        dealresults = dealpool.map(batch_page_list, pages)

        dealpool.close()
        dealpool.join()

        # for page in (1, totalpage):
        #     dealList = []
        #     data = params(search)
        #     data["page"] = page
        #     url_para = urllib.parse.urlencode(data)
        #     full_url = url + '?' + url_para
        #     context = ssl._create_unverified_context()
        #     with urllib.request.urlopen(full_url, context=context) as response:
        #         html = response.read()
        #         html = html.decode("utf-8")
        #         data = json.loads(html)['foods']
        #         for each in data:
        #             array = []
        #             #print(each)
        #             if(each['name'] != search):
        #                 array.append(str(uuid.uuid1()))
        #                 array.append(str(each['calory']))
        #                 array.append(str(each['weight']))
        #                 array.append(str(each['code']))
        #                 array.append(str(each['name']))
        #                 if(each['thumb_image_url']) is None:
        #                     array.append("1")
        #                 else:
        #                    array.append(str(each['thumb_image_url']))
        #                 array.append(str(each['health_light']))
        #                 array.append(str(each['is_liquid']))
        #                 dealList.append(array)
        #         #批量保存数据
        #         print("start save data 搜索条件 ：{0}, 共：{1}页, 第{2}页".format(search ,totalpage, page))
        # #         batch_deal_data(dealList)
        # # #更新搜索结果
        # # update_search(search)

def spider_data_by_chinese_item(search) :
    logging.info("start deal: "+ search['chinese_item'])
    totalpage = total_page(search['chinese_item'])
    pages = array_page(totalpage, search['chinese_item'])

    # dealpool = ThreadPool(4)
    if len(pages) >= 1:
       batch_page_list(pages[0])
    # dealresults = dealpool.map(batch_page_list, pages)
    #
    # dealpool.close()
    # dealpool.join()

# 按页处理
def batch_page(page, search, totalpage):
    red = redis_connect()
    dealList = []
    data = params(search)
    data["page"] = page
    url_para = urllib.parse.urlencode(data)
    full_url = url + '?' + url_para
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(full_url, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)['foods']
        # 去重
        for each in data:
            array = []
            # print(each)
            code = str(each['code'])
            if red.exists("code:{0}".format(code)):
                logging.info("code:{0}".format(code) + "已存在")
                continue
            else:
                red.set("code:{0}".format(code), each)
                array.append(str(uuid.uuid1()))
                array.append(str(each['calory']))
                array.append(str(each['weight']))
                array.append(str(each['code']))
                array.append(str(each['name']))
                if (each['thumb_image_url']) is None:
                    array.append("1")
                else:
                    array.append(str(each['thumb_image_url']))
                if each['health_light'] is None:
                    array.append("3")
                else:
                  array.append(str(each['health_light']))
                array.append(str(each['is_liquid']))
                array.append(search)
                print("入库数据", array)
                logging.info("入库数据"+ "".join(array))
                dealList.append(array)
            # 批量保存数据
        logging.info("start save data 搜索条件 ：" + search + "共：" + str(totalpage) + "页, 第" + str(page) + " 页, 共:" + str(len(dealList)) + "条数据")
        print("start save data 搜索条件 ：{0}, 共：{1}页, 第{2}页, 共:{3} 条数据".format(search, totalpage, page, len(dealList)))
        if dealList :
          batch_deal_data(dealList)


# 按页处理
def batch_page_list(page):
    print(page)
    dealList = []
    data = params(page['search'])
    data["page"] = page['page']
    url_para = urllib.parse.urlencode(data)
    full_url = url + '?' + url_para
    context = ssl._create_unverified_context()
    red = redis_connect()
    with urllib.request.urlopen(full_url, context=context) as response:
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)['foods']
        # 去重
        # data = heavy_discharge_list(data)
        # 去重干掉
        for each in data:
            code = str(each['code'])
            if each['name'] == page['search']:
                print('存在信息', each['name'])
                array = []
                array.append(str(uuid.uuid1()))
                array.append(str(each['calory']))
                array.append(str(each['weight']))
                array.append(str(code))
                array.append(str(each['name']))
                if (each['thumb_image_url']) is None:
                    array.append("1")
                else:
                    array.append(str(each['thumb_image_url']))
                if each['health_light'] is None:
                    array.append("3")
                else:
                  array.append(str(each['health_light']))
                array.append(str(each['is_liquid']))
                array.append(page['search'])
                print("入库数据", array)
                dealList.append(array)
                break
        if dealList:
           # 批量保存数据
           logging.info("start save data 搜索条件 ：" + page['search'] + "共：" + str(page["totalPage"]) + "页, 第" + str(
                page) + "页, 共:" + str(len(dealList)) + "条数据")
           print("start save data 搜索条件 ：{0}, 共：{1}页, 第{2}页, 共:{3} 条数据".format(page['search'], page['totalPage'], page,
                                                                               len(dealList)))
           batch_deal_data(dealList)
           # update_search(each['name'])


#筛选数据并且入库
def heavy_discharge_list(data):
    data_arrar = []
    final_data_arrar = []
    for each in data:
        data_arrar.append(each['code'])
    database_jk = select_in_code(data_arrar)
    if database_jk:
        for each_data in data:
            for jk_data in database_jk:
                if each_data['code'] != jk_data['code']:
                    final_data_arrar.append(each_data)

        return  final_data_arrar
    else:
       return data



#去重信息
def select_in_code(searchlist):
    select_search_sql = "select * from bohejiankang where code in (%s)"
    sdb5 = db()
    cursor = sdb5.cursor()
    try:
        in_code = ', '.join((map(lambda x: '%s', searchlist)))
        print("去重查询：", select_search_sql % in_code)
        # 执行sql语句
        cursor.execute(select_search_sql % in_code, searchlist)
        # 提交到数据库执行
        result = cursor.fetchmany()  # 获取查询的所有记录
        sdb5.commit()
        return result
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        sdb5.rollback()

#批量插入数据
def batch_deal_data(data):
    insertsql = "INSERT INTO  bohejiankang (id, calory, weight, code, name, thumb_image_name, health_light, is_liquid,remark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
    sdb2 = db()
    cursor = sdb2.cursor()
    dealdata = tuple(tuple([y for y in x]) for x in data)
    try:
        # 执行sql语句
        result = cursor.executemany(insertsql, dealdata)
        # 提交到数据库执行
        sdb2.commit()
        return  result
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        sdb2.rollback()

#更新搜索条件为1
def update_search(search):
    print("start deal data")
    updatesql = "update t_chinese  set status = 1 where chinese_item = '{0}'"
    sdb3 = db()
    cursor = sdb3.cursor()
    try:
        # 执行sql语句
        result = cursor.execute(updatesql.format(search))
        # 提交到数据库执行
        sdb3.commit()
        return  result
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        sdb3.rollback()


#查询搜索条件为1
def select_search(search):
    select_search_sql = "select * from t_chinese where chinese_item = '{0}' and is_query = 1"
    print("查询：", select_search_sql.format(search))
    sdb4 = db()
    cursor = sdb4.cursor()
    try:
        # 执行sql语句
        cursor.execute(select_search_sql.format(search))
        # 提交到数据库执行
        result = cursor.fetchone()  # 获取查询的所有记录
        sdb4.commit()
        return result
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        sdb4.rollback()


#返回总页数
def array_page(totalpage,search):
    arraypage = range(1, totalpage+1)
    pages = []
    for each in arraypage:
        page_obj = {}
        page_obj['page'] = each
        page_obj['search'] = search
        page_obj['totalPage'] = totalpage
        pages.append(page_obj)
    return pages


#查询搜索条件为1
def select_search_not_deal():
    select_search_sql = "select chinese_item from chinese_item where status is null"
    sdb8 = db()
    cursor = sdb8.cursor()
    try:
        # 执行sql语句
        cursor.execute(select_search_sql)
        # 提交到数据库执行
        result = cursor.fetchall()  # 获取查询的所有记录
        sdb8.commit()
        return result
    except pm.Warning as w:
        print(repr(w))
        # 如果发生错误则回滚
        sdb8.rollback()

# redis 链接
def redis_connect():
    pool = redis.ConnectionPool(host='192.168.1.119', password=123456,  port=6379, db=0)
    red = redis.Redis(connection_pool=pool)

    return red


def random_num():

    return random.randint(12, 100);



def deal_kuohao(list):
    inresult = []
    notresult = []
    for each in list:
      if '[' not in each['chinese_item'] or ']' not in  each['chinese_item']:
          inresult.append(each)
      else:
          notresult.append(each)
    return inresult, notresult

#主类
if __name__ == '__main__':
    # spider("再")
    pool = ThreadPool(8)

    data = select_search_not_deal()
    print('总计数据：',  len(data))
    inresult, notresult = deal_kuohao(data)

    print('不含括号的数据：', len(inresult), '含括号的数据：', len(notresult))
    dealresults = pool.map(spider_data_by_chinese_item, inresult)
    #
    # pool.close()
    # pool.join()