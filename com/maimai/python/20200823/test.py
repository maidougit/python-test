# -*- coding: utf-8 -*-

import  copy, urllib
from urllib import parse

url_change = parse.urlparse('https://i.cnblogs.com/EditPosts.aspx?opt=1')
print (url_change.query)


def url_values_plus(url, k1,v1):
    ret = ''
    u = parse.urlparse(url)
    print('u:', u)
    qs = u.query
    print('qs:', qs)
    pure_url = url.replace('?'+qs, '')
    print('pure_url:', pure_url)
    qs_dict = dict(parse.parse_qsl(qs))
    print('qs_dict:', qs_dict)
    for k in qs_dict.keys():
        if k == k1:
         qs_dict[k] = v1
         tmp_qs = parse.unquote(parse.urlencode(qs_dict))
         ret = pure_url + "?" + tmp_qs
         break
    return ret

url = "http://www.waitalone.cn/index.php?id=123&abc=456&xxx=ooo"
payloads = ('../boot.ini','../etc/passwd','../windows/win.ini','../../boot.ini','../../etc/passwd')
urls = url_values_plus(url, 'xxx', '123')
print (urls)

