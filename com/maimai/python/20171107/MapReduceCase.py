#-*-coding=utf-8-*-
#map()传入的第一个参数是f，即函数对象本身。由于结果r是一个Iterator，
# Iterator是惰性序列，因此通过list()函数让它把整个序列都计算出来并返回一个list。
def f(x):
    return x * x

r = map(f, [1, 2, 3, 4, 5, 6])

print list(r)

def add(x, y):
    return x+y

# 求和
sum = reduce(add,[1, 3, 5, 7])

print sum

# 拼接字符
def fn(x, y):
    return x * 10 + y

sumStr = reduce(fn, [1, 7, 6, 3])

print sumStr

def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

print reduce(fn, map(char2num, '13572'))