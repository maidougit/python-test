import requests
import json
import urllib
import ssl


url = 'https://record.boohee.com/api/v2/eatings/hot'

data = {
    'page':1,
    'token':'B1oNpyd1ypDPjQ8vTN93jCAd8b4zXeyq',
    'user_key':'0342d302-62c6-4c98-82e9-72537d9d2d6c',
    'app_version':'7.1.8',
    'app_device':'Android',
    'os_version':'5.1.1',
    'phone_model':'hm+note+1lte',
    'channel':'undefind',
    'app_key':'one'
}

headers ={
    "content-type":"application/json"
}


req = requests.get(url = url,
                headers = headers,
                data = json.dumps(data).encode("utf-8"))

print(req.text)


context = ssl._create_unverified_context()
req = urllib.request.Request(url=url,headers=headers)

