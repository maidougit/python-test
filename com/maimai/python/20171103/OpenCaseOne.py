#-*-coding=utf-8-*-
x = open(r'‪E:/first-1102.edi', 'r')

try:
    y = x.read()
finally:
    x.close()

print y
