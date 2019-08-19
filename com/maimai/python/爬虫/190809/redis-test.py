import redis

# re = redis.Redis(host='127.0.0.1', port=6379,db=0, password=123456)
#
# re.set('test:{0}'.format("student"),'value_tom')
# print(re.get('test:student'))


# redis 链接
def redis_connect():
    pool = redis.ConnectionPool(host='192.168.1.119', password=123456,  port=6379, db=0)
    red = redis.Redis(connection_pool=pool)

    return red


if __name__ == '__main__':
    red = redis_connect()
    red.set("test:key1", "value2")

    if red.exists('test:key1'):
        print("存在")
    else:
        print("不存在")