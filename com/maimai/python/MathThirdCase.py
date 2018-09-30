#-*-coding=utf-8-*-

#斐波那契 输出对应的结果
def fib(n):
    if n == 1:
        return [1]
    elif n == 2:
        return [1,1]
    fibs = [1,1]
    for i in (2, n):
        fibs.append(fibs[i-1]+fibs[i-2])
    return fibs

print fib(3)
