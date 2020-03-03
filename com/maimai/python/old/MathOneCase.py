#-*-coding=utf-8-*-
import math
i = int(raw_input('净利润:'))
arr = [1000000,600000,400000,200000,100000,0]
rat = [0.01,0.015,0.03,0.05,0.075,0.1]
r = 0
for idx in range(0,6):
    if i>arr[idx]:
        r+=(i-arr[idx])*rat[idx]
        print (i-arr[idx])*rat[idx]
        i=arr[idx]
print (r)

#一个整数，它加上100和加上268后都是一个完全平方数
for m in range(10000):
    x = int(math.sqrt(m+100))
    y = int(math.sqrt(m+268))
    if (x * x == m + 100) and (y * y == m+268):
      print m


