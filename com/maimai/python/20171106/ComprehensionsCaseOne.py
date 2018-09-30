#-*-coding=utf-8-*-
# 生成1-10 数组
num = list(range(1, 11))

print num

#[1x1, 2x2, 3x3, ..., 10x10]

nums = [x * x for x in range(1, 11)]

print nums

#
nums = [x * x for x in range(1, 11) if x % 2 == 0]

print nums

# 双重循环
list= [m + n for m in 'ABC' for n in 'XYZ']

print list


