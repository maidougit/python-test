#-*-coding=utf-8-*-
import os
#列出当前目录列表
print  [d for d in os.listdir('.')]

d = {'x': 'A', 'y': 'B', 'z': 'C' }

for k in d:
    print k

for value in d.items():
    print value

