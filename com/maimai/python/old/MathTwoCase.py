#-*-coding=utf-8 -*-
#整数顺序排列问题简述：任意三个整数类型，x、y、z
#提问：要求把这三个数，按照由小到大的顺序输出
# 声明变量
l = []
y = int(input('数组长度'))
#三个数组循环
for i in range(y):
    x = int(input('integer:\n'))
    l.append(x)
# 排序
l.sort()
print (l)


#斐波那契 测试
def feibonaqie(n):
    if n ==1 or n == 2:
        return 1;
    return feibonaqie(n-1) + feibonaqie(n-2)

print (feibonaqie(10))

