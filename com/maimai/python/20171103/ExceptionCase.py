#-*-coding=utf-8-*-
try:
    a = 10
    b = 0
    print a / b
except ZeroDivisionError:
    print "除零错误，已经捕获"