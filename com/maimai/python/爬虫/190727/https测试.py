import urllib.request
import urllib.parse
import ssl

context = ssl._create_unverified_context()

#CGI(Common Gateway Interface)是HTTP服务器运行的程序
#通过Internet把用户请求送到服务器
#服务器接收用户请求并交给CGI程序处理
#CGI程序把处理结果传送给服务器
#服务器把结果送回到用户

url = 'https://record.boohee.com/api/v2/eatings/hot'


data = {}

data['page'] = 1
data['token'] = 'B1oNpyd1ypDPjQ8vTN93jCAd8b4zXeyq'
data['user_key'] = '0342d302-62c6-4c98-82e9-72537d9d2d6c'
data['app_device'] = 'Android'
data['os_version'] = '5.1.1'
data['phone_model'] = 'hm+note+1lte'
data['channel'] = 'undefind'
data['app_key'] = 'one'

url_para = urllib.parse.urlencode(data)
full_url = url + '?' + url_para

context = ssl._create_unverified_context()

with urllib.request.urlopen(full_url, context=context) as response:
  html = response.read()
  print(response)#200是正常响应

req = urllib.request.Request(url, data=data)

with  urllib.request.urlopen(req, context=context) as response:
 html = response.read()
 print(html)