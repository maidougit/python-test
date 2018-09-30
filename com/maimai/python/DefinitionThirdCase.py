# -*-coding=utf-8 -*-
# 多次方计算
def jisuan(x, n=2):
  m = 1
  while n > 0:
      n = n - 1
      m = m * x
  return  m

# 1. 规则 必选参数在前， 默认参数在后
#  多个参数时， 变化大的参数在前， 变化小的参数在后， 可以作为默认参数
print jisuan(5, 5)

print jisuan(6)

# 实验
def enroll(name, gener, age=6, city='Beijing'):
    print('name', name)
    print('gender', gener)
    print('age', age)
    print('city', city)

# 两个参数
enroll('张三', '男')

enroll("里斯", '女', 18, "上海")


def add_end(L=None):
    if L is None:
        L = []
    L.append('end')
    return L

print add_end()

# 多参实验1+2^2+3^3  调用的时候，需要先组装出一个list或tuple
def cal(numbers):
    sum = 0
    for n in numbers:
       sum = sum + n * n
    return sum

print cal([1, 2, 3])
print cal((1, 3, 5, 7))


def snm( _init ):
    def r( _seed, _n ):
        if _n >= _init:
            return _seed
        return r( _seed + _n * _n, _n + 1 )
    return r( 0, 0 )

print snm(997)

# 加星号为可变的参数 定义可变参数和定义一个list或tuple参数相比，仅仅在参数前面加了一个*号。在函数内部，参数numbers接收到的是一个tuple，
# 因此，函数代码完全不变。但是，调用该函数时，可以传入任意个参数，包括0个参数
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print calc(1, 3, 5)

nums = [1, 2, 3]
print calc(nums[1], nums[2])
# 将数组转换成可变参数
print calc(*nums)

#关键字参数 必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
def person(name, age, args, city, job):
    print(name, age, args, city, job)

person('Jack', 24, city='Beijing', job='Engineer')