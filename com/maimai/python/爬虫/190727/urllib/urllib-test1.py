from urllib import request

resp = request.urlopen("https://www.baidu.com",)

print(resp.read())

