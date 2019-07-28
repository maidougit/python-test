import re


secret_code = "djakjdjaxxIxxjdajdjajxxlovexxjijahhhahxxyouxxjxjjjjsh"

# 正则表达式手册
# http://tool.oschina.net/uploads/apidocs/jquery/regexp.html

# . : 匹配任意字符，换行符\n 除外
# * : 匹配前一个字符0次或无限次
# ? : 匹配前一个字符0此或一次
# .*: 贪心算法
# .?: 非贪心算法


# .的使用
a = 'xyzx123'
b = re.findall('x.', a)
print('点号使用的结果：' , b)

# *号的使用
a = 'xy1234x1'
b = re.findall('x*', a);
print('星号使用的结果: ' , b)


a = 'xy1234x1'
b = re.findall('x?', a);
print('问号使用的结果: ' , b)

# .* 的使用举例
a = re.findall('xx.*xx', secret_code);
print(a)
b = re.findall('xx.*?xx', secret_code)
print(b)

# 使用括号与不适用括号的区别
a = re.findall('xx(.*?)xx', secret_code)
print(a)

for each in a :
    print(each)


# 换行符  re.S  换行符的区别
s = '''xx123334
xx123xx1dkaxx
'''
a = re.findall('xx(.*?)xx',s)
a = re.findall('xx(.*?)xx',s, re.S)
print(a)


secret_code = 'xxkskaxxskakkakxxkdkkkkxxkakkkaxx'
a = re.search("xx(.*?)xx", secret_code)

secret_code = 'xx123445xx'
a = re.sub('xx(.*?)', 'xx%dxx'%789, secret_code)
print(a)
