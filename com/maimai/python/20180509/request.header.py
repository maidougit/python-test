#-*-codinh=utf8-*-
import requests

hd = {'User-agent':'123'}
r = requests.get('http://www.baidu.com', headers=hd)
print(r.request.headers)
'''
OUT:
{'User-agent': '123', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive
'}
'''