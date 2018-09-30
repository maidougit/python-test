# -*- coding: UTF-8 -*-
age =13
if age < 18 :
    print('your age is 张三' , age)
else:
    print ('you have adult')


if age < 10:
    print ('you are a young child')
elif 10 <= age < 18:
    print ('you are a young people')
else:
    print age

birth = input('birth')
if birth < 2000:
    print ('00前')
else:
    print ('00后')

day = input(int)
if day < 2017:
    print('今天是周四')
else:
    print ('我也不知道今天几号了')

height = float(input('输入身高(m):'))
weight = float(input('输入体重(kg):'))
bmi = weight / (height)
print('BMI为%.2f' % bmi)
if bmi < 18.5:
    print('过轻')
elif bmi < 25:
    print('正常')
elif bmi < 28:
    print('过重')
elif bmi < 32:
    print('肥胖')
else:
    print('严重肥胖')
print('身高%.2f(m),体重正常范围是%.2f(kg)—%.1f(kg)' % (height, 18.5 , 25, height * height))