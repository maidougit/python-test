import  requests


header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 YaBrowser/19.7.0.1635 Yowser/2.5 Safari/537.36'}
html = requests.get('http://jp.tingroom.com/yuedu/yd300p/')

print(html.text)