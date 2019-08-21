#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#此程序仅供学习交流使用。

import urllib.request
import json
import re
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

name = input("输入你想听的歌名or歌名+歌手:")
name = urllib.parse.quote(name)
url = "https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w="+name

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}

def network(url):
    request_url = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(request_url).read().decode('utf-8')
    return response

def download(songmid,music_name):
#json数据
    json_url = "https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback8796342823761736&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback8796342823761736&uin=0&" \
           "songmid="+songmid+"&filename=C400"+songmid+".m4a&guid=4626869183"
    html = network(json_url)
#找到json中music的信息
    music_json = json.loads(re.findall(r'^\w+\((.*)\)$',html)[0])
    filename = music_json['data']['items'][0]['filename']
    vkey = music_json['data']['items'][0]['vkey']
#歌曲的下载链接
    download_url = "http://dl.stream.qqmusic.qq.com/"+filename+"?vkey="+vkey+"&guid=4626869183&uin=0&fromtag=66"
    ret_url = urllib.request.Request(download_url,headers=headers)
    music_url = urllib.request.urlopen(ret_url).read()
    with open("./"+music_name+".m4a", "wb") as fb:
        fb.write(music_url)

def get():
#加载Chromedriver,百度chromedriver.exe，下载与自己chrome版本一致的。
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome('F:\python-test\venv\Scripts\chromedriver.exe',chrome_options=option)
#请自行修改加载的路径
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js_song")))
    music = driver.find_element_by_class_name('js_song')
    href = music.get_attribute('href')
    music_name = music.get_attribute('title')
#匹配到歌曲的id
    songmid = re.findall(r'https://y.qq.com/n/yqq/song/(\S+).html',href)[0]
    download(songmid,music_name)

if __name__ == '__main__':
    get()