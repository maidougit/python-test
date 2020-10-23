# -*- coding=utf8 -*-
from hdfs3 import HDFileSystem

hdfs = HDFileSystem(host='139.196.126.222', port=9000)

list = hdfs.ls('/dest')

for a in list:
    print(a)