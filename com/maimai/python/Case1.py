#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 循环输出无重复数字
for i in range(1,5):
    for j in range(1, 5):
        for k in range(1, 5):
            if(i != j) and (i != k) and (j !=k):
                print i, j, k

# 将无重复的三位数添加至数组， 并且计算多少位
d = []
for a in range(1, 5):
    for b in range(1, 5):
        for c in range(1, 5):
            if (a != b) and (a != c) and (c != b):
                d.append([a, b, c])
print "总数量：", len(d)
print d


list_num = [1,2,3,4]

list  = [i*100 + j*10 + k for i in list_num for j in list_num for k in list_num if (j != i and k != j and k != i)]

print (list)



num=[1,2,3,4]
i=0
for a in num:
    for b in num:
        for c in num:
            if (a!=b) and (b!=c) and (c!=a):
                i+=1
                print(a,b,c)
print('总数是：'.decode('UTF-8'),i)