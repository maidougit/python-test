import requests,re


url = 'https://www.crowdfunder.com/course/deals&template'

data = {
    'enteities_only':'true',
    'page':'1'
}

html_post = requests.post(url, data=data)
title = re.findall('"card-title">(.*?)</div>', html_post.text, re.S)
for each in title:
    print(each)