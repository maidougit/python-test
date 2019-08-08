import pymysql as pm
from multiprocessing.dummy import Pool as ThreadPool
import json, csv

# SQL 插入语句
sql = "select * from bohejiankang"

headers = [
    'id', 'food_id', 'food_id',
    'calory',
    'weight',
    'code',
    'name',
    'thumb_image_name',
    'health_light',
    'is_liquid',
    'calory',
    'protein',
    'fat',
    'saturated_fat',
    'fatty_acid',
    'mufa',
    'pufa',
    'cholesterol',
    'carbohydrate',
    'sugar',
    'fiber_dietary',
    'natrium',
    'alcohol',
    'vitamin_a',
    'carotene',
    'vitamin_d',
    'vitamin_e ',
    'vitamin_k',
    'thiamine',
    'lactoflavin',
    'vitamin_b6',
    'vitamin_b12',
    'vitamin_c',
    'niacin',
    'folacin',
    'pantothenic',
    'biotin',
    'choline',
    'phosphor',
    'kalium',
    'magnesium',
    'calcium',
    'iron',
    'zinc',
    'iodine',
    'selenium',
    'copper',
    'fluorine',
    'manganese'
]


# 查询
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


# 数据库连接db
def db():
    db = pm.connect(host='localhost', port=3306,
                    user='root', passwd='root', db='t_reptile', charset='utf8', cursorclass=pm.cursors.DictCursor)
    return db


# dealHttpsByObj
def batchDealHttpsByObj(row):
    ingredient_only = json.loads(row['ingredient_only'])
    row['calory'] = ingredient_only['ingredient']['main_ingredient']['calory']
    row['protein'] = ingredient_only['ingredient']['main_ingredient']['protein']
    row['fat'] = ingredient_only['ingredient']['main_ingredient']['fat']
    row['saturated_fat'] = ingredient_only['ingredient']['main_ingredient']['saturated_fat']
    row['fatty_acid'] = ingredient_only['ingredient']['main_ingredient']['fatty_acid']
    row['mufa'] = ingredient_only['ingredient']['main_ingredient']['mufa']
    row['pufa'] = ingredient_only['ingredient']['main_ingredient']['pufa']
    row['cholesterol'] = ingredient_only['ingredient']['main_ingredient']['cholesterol']
    row['carbohydrate'] = ingredient_only['ingredient']['main_ingredient']['carbohydrate']
    row['sugar'] = ingredient_only['ingredient']['main_ingredient']['sugar']
    row['fiber_dietary'] = ingredient_only['ingredient']['main_ingredient']['fiber_dietary']
    row['natrium'] = ingredient_only['ingredient']['main_ingredient']['natrium']
    row['alcohol'] = ingredient_only['ingredient']['main_ingredient']['alcohol']

    row['vitamin_a'] = ingredient_only['ingredient']['vitamin_ingredient']['vitamin_a']
    row['carotene'] = ingredient_only['ingredient']['vitamin_ingredient']['carotene']
    row['vitamin_d'] = ingredient_only['ingredient']['vitamin_ingredient']['vitamin_d']
    row['vitamin_e '] = ingredient_only['ingredient']['vitamin_ingredient']['vitamin_e']
    row['vitamin_k'] = ingredient_only['ingredient']['vitamin_ingredient']['vitamin_k']
    row['thiamine'] = ingredient_only['ingredient']['vitamin_ingredient']['thiamine']
    row['lactoflavin'] = ingredient_only['ingredient']['vitamin_ingredient']['lactoflavin']
    row['vitamin_b6'] = ingredient_only['ingredient']['vitamin_ingredient']['vitamin_b6']
    row['vitamin_b12'] = ingredient_only['ingredient']['vitamin_ingredient']['vitamin_b12']
    row['vitamin_c'] = ingredient_only['ingredient']['vitamin_ingredient']['vitamin_c']
    row['niacin'] = ingredient_only['ingredient']['vitamin_ingredient']['niacin']
    row['folacin'] = ingredient_only['ingredient']['vitamin_ingredient']['folacin']
    row['pantothenic'] = ingredient_only['ingredient']['vitamin_ingredient']['pantothenic']
    row['biotin'] = ingredient_only['ingredient']['vitamin_ingredient']['biotin']
    row['choline'] = ingredient_only['ingredient']['vitamin_ingredient']['choline']

    row['phosphor'] = ingredient_only['ingredient']['minerals_ingredient']['phosphor']
    row['kalium'] = ingredient_only['ingredient']['minerals_ingredient']['kalium']
    row['magnesium'] = ingredient_only['ingredient']['minerals_ingredient']['magnesium']
    row['calcium'] = ingredient_only['ingredient']['minerals_ingredient']['calcium']
    row['iron'] = ingredient_only['ingredient']['minerals_ingredient']['iron']
    row['zinc'] = ingredient_only['ingredient']['minerals_ingredient']['zinc']
    row['iodine'] = ingredient_only['ingredient']['minerals_ingredient']['iodine']
    row['selenium'] = ingredient_only['ingredient']['minerals_ingredient']['selenium']
    row['copper'] = ingredient_only['ingredient']['minerals_ingredient']['copper']
    row['fluorine'] = ingredient_only['ingredient']['minerals_ingredient']['fluorine']
    row['manganese'] = ingredient_only['ingredient']['minerals_ingredient']['manganese']

    # 移除多余key
    del row['ingredient_only']
    del row['remark']
    del row['food_detail']
    downloadImage(row)


def dealHttps(row):
    print(row)
    each = {}
    id = row[0]
    code = row[4]
    name = row[5]
    downloadImage(each)


def downloadImage(each):
    print("start write data")
    writer.writeheader()
    writer.writerow(each)


# 主类
if __name__ == '__main__':
    goodDb = select()
    # print(batchDealHttpsByObj(goodDb[0]))
    #
    # pool = ThreadPool(8)
    #
    # dealresults = pool.map(batchDealHttpsByObj, goodDb)
    # pool.close()
    # pool.join()
    pool = ThreadPool(10)
    f = open(r'F:\python-test\file\record\bohejiankang-0808.csv', 'w+', newline='', encoding='utf-8-sig')
    writer = csv.DictWriter(f, headers)

    dealresults = pool.map(batchDealHttpsByObj, goodDb)
    pool.close()
    pool.join()
    f.close()
