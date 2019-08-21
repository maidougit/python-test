import requests
import json
import pprint


r = requests.get("https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid=24157236&sort=0&_=1553733228187")

data = json.loads(r.text)

use_map={}
for i in data['data']['replies']:
    use_map[i['member']['mid']]=i['member']['uname']
    # pprint.pprint([i['member']['mid'],i['member']['uname']])
    if i['replies'] != None:
        for j in i['replies']:
            pprint.pprint(j)

