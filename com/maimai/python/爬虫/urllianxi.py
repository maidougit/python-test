#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib.request


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


url = "http://tieba.baidu.com/p/4040087257/"
html = getHtml(url)

print(html)
