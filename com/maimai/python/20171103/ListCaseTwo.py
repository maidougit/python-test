#-*-coding=utf-8-*-
# 定义元祖
name =(1, 2, 3, 4, 5, 6)
# 元祖叠加输出
print name + name
print name * 3

names = list(name)
names[1]='我是谁'
name = tuple(names)


print name