
import re

url = 'https://www.jikexueyuan.com/course/android?pageNum=2'
total_page = 20

f = open('F:\\python-test\\file\\test.html', 'r',encoding='utf8',errors='ignore')
html = f.read()
f.close()

#print(html)

title = re.search('<title>(.*?)</title>', html, re.S).group(1)

print(title)


links = re.findall('href="(.*?)"', html, re.S)
for each in links:
    print(each)


# 先抓大在抓小
text_field = re.findall('<ul>(.*?)</ul>',html,re.S)[0]
print(text_field)
the_text = re.findall('href="(.*?)"', text_field, re.S)
the_text1 = re.findall('">(.*?)</a>', text_field, re.S)
for exch in the_text1:
    print(exch)

#print(the_text1)

for i in range(2, total_page+1):
    new_link = re.sub('pageNum=\d+','pageNum=%d'%i, url, re.S)
    print(new_link)