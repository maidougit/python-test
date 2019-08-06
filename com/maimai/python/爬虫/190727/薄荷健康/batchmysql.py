import pymysql as pm
from warnings import filterwarnings
filterwarnings('error', category=pm.Warning)


db = pm.connect(host='localhost', port=3306,
                     user='root', passwd='root', db='blog', charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO blog.bohejiankang (food_id, calory, weight, code, name, thumb_image_name, health_light, is_liquid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
# 一个tuple或者list
T = (('1750', '241.0', '100.0', 'dizhinailao', '低脂奶酪', "http://s.boohee.cn/house/new_food/mid/d81ffff988a844e59c2a7f6058ecb0ae.jpg", '2', 'False'), ('872', '54.0', '100.0', 'niuru_junzhi', '全脂牛奶', "http://s.boohee.cn/house/new_food/mid/e4ba04daf3814d06a7d0a25890adde36.jpg", '1', 'True'))

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
