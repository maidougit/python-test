#-*-coding=utf-8-*-
import time

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# 暂停一秒
time.sleep(1)

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

a1 = 1
b2 = 1
for i in range(1,21):
    print '%12ld %12ld' % (a1,b2),
    if (i % 3) == 0:
        print ''
    a1 = a1 + b2
    b2 = a1 + b2