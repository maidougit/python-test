#-*-coding=utf-8-*-
f = open('E:\ideawork\pom.xml')
while True:
    text = f.readline()    #读取文件指针指向的哪一行内容，然后指针下移
    if text:
        print(text)
    else:  #当文读到最后一行，三个空字符串
        print(len(text))
        break
f.close()  #关闭文件，运行一下

##
f = open("hello.txt")
line_list = f.readlines()  #一次性读取，以列表的形式表现出来
print(type(line_list))
for line in line_list:
    print(line)
f.close()
