# -*- coding: UTF-8 -*-
classmates = ['张三', '里斯']

print(classmates[0])

#输出长度
print len(classmates)

#插入数据
classmates.insert(2, '王五')

# 添加数据后长度
print len(classmates)

#删除数据
classmates.pop(1)

print classmates[1]
print len(classmates)

#替换元素
classmates[1] = '黎明'

print classmates[1]

#循环输出数据
for  classmate in classmates:
    print classmate

# 循环方法二
for index,app_id in enumerate(classmates):
    print index, app_id