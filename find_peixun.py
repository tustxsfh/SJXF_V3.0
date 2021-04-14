# -*- coding: utf-8 -*- 
# 找到专题培训课程URL，写入文件
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import requests
import re
import json
import random
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from PIL import Image
import pytesseract
from pytesseract import image_to_string



browser = webdriver.Chrome()
browser.implicitly_wait(60*3)

#登录页面
login_url = "https://www.sxgbxx.gov.cn/login"
browser.get(login_url)

username = browser.find_element_by_id('userEmail')
username.send_keys('*********')                       #此处填入账号
password = browser.find_element_by_id('userPassword')
password.send_keys('*********')                       #此处填入密码
#获取截图
browser.get_screenshot_as_file('tempimg/screenshot.png')

#获取指定元素位置
element = browser.find_element_by_id('img')
left = int(element.location['x'])
top = int(element.location['y'])
right = int(element.location['x'] + element.size['width'])
bottom = int(element.location['y'] + element.size['height'])

#通过Image处理图像
im = Image.open('tempimg/screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('tempimg/random.png')


img = Image.open('tempimg/random.png')
code = pytesseract.image_to_string(img)

randomcode = browser.find_element_by_id('randomCode')
randomcode.send_keys(code)
browser.find_element_by_class_name('bm-lr-btn').click()

time.sleep(5)

# https://www.sxgbxx.gov.cn/uc/plan  我的培训
pei_url = 'https://www.sxgbxx.gov.cn/uc/plan'
# "https://www.sxgbxx.gov.cn/uc/plan/info?id=764af75f77ec964f" 培训一

browser.get(pei_url)
r = browser.page_source
pei_obj = BeautifulSoup(r, "lxml")
pei_list = pei_obj.findAll("div",{"class":"e-m-more"})  # 获取我的专题培训内容

f1 = open('peng_url.txt','w')  # 培训课程的url

for pid in pei_list:
    pid = str(pid)
    print(pid)
    pid = re.findall(r'id=(.+?)"',pid)
    print(pid)
    peixun_url = 'https://www.sxgbxx.gov.cn/uc/plan/info?id=' + pid[0]   # 生成培训课题的url
    browser.get(peixun_url)

    # print(browser.page_source)
    time.sleep(10)
    r = browser.page_source
    pei_obj = BeautifulSoup(r, "lxml")
    peixun_list = pei_obj.findAll("a", {"class": "lh-reply-btn"})

    for i in peixun_list:
        # print(i)
        # print(i.get_text())
        # print(i['href'])
        i = 'https://www.sxgbxx.gov.cn' + str(i['href'])
        print(i)
        f1.write(i)
        f1.write('\n')





f1.close()
