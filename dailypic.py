# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 10:33
# @Author  : Crazycosin
# @Site    : 
# @File    : dailypic.py
# @Software: PyCharm
import random
import urllib.request
import re
import ssl
import json
from urllib import error
import os
import win32gui
import win32con
from PIL import Image
_name= ''

ssl._create_default_https_context = ssl._create_unverified_context#针对https安全访问
ua_list = [
    "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS... "
]
user_agent = random.choice(ua_list)
url = u'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'


'''每天定时跟随系统启动抓取，抓取当日的壁纸，并存入文件夹中，然后设置为桌面'''
def scrapy_picture():
    request = urllib.request.Request(url)

    # 也可以通过调用Request.add_header() 添加/修改一个特定的header
    request.add_header("User-Agent", user_agent)
    # 第一个字母大写，后面的全部小写
    request.get_header("User-agent")

    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')
    dic_data = json.loads(data)
    image_url = u'https://cn.bing.com'+dic_data.get('images')[0].get('url')
    name = dic_data.get('images')[0].get('copyright').replace(' ', '').replace('/','&')
    date = dic_data.get('images')[0].get('startdate')
    image_name = date+','+name
    print(image_name)
    return image_url,image_name

def download():
    image_url,img_name = scrapy_picture()
    _name = img_name
    try:
        urllib.request.urlretrieve(image_url, (r'D:\dailypicture\{}.jpg'.format(img_name)).encode())
    except error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError")
            print(e.code)
        elif hasattr(e, 'reason'):
            print("URLError")
            print(e.reason)
    return img_name

varStorageBMPPath = u"D:\dailypicture\BMP"

def ConvertPicTypeToBMP(picPath):
    print("Convert the pic type to .BMP")
    picName = _name
    print(picName)
    im = Image.open(picPath)
    print("Format:%s,Size:%s,Mode:%s"%(im.format,im.size,im.mode))

    bmpPath = varStorageBMPPath + picName + ".BMP"#Set the full path of .BMP file to storage it
    print("BMP path:%s"%bmpPath)

    im.save(bmpPath)#Save the .BMP file to disk

    return bmpPath

def SetWindowsWallpaper(bmpFilePath):
    print("The pic path which will be set as wallpaper is:%s"%bmpFilePath)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmpFilePath, win32con.SPIF_SENDWININICHANGE);#Only .BMP file can be set as the wallpaper
    return None




if __name__ == "__main__":
    print("This is SetWindowsWallpaper.py")
    img_name = download()
    try:

        img_path = u'D:\dailypicture\{}.jpg'.format(img_name)
        print(img_path)
        bmpFullPath = ConvertPicTypeToBMP(img_path)
        SetWindowsWallpaper(bmpFullPath)#Set windows wallpaper by the given pic path
    except IOError:
        print("Set windows wallpaper failed!")