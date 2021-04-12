# -*- coding: utf-8 -*- 
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

with open('peng_url.txt', 'r') as f:
    cou_url_list = f.read().splitlines()

    sum = len(cou_url_list)
    # linestr = line.split(" ")
# print(cou_url_list)

start_time = time.time()

# exr_data = r'E:\360\360Chrome\Chrome\Application\360chrome.exe'
# chrome_options = Options()
# chrome_options.binary_location = exr_data
browser = webdriver.Chrome()

browser.implicitly_wait(60 * 3)

# 登录页面
login_url = "https://www.sxgbxx.gov.cn/login"
browser.get(login_url)

username = browser.find_element_by_id('userEmail')
username.send_keys('u0283323')  # 此处填入账号
password = browser.find_element_by_id('userPassword')
password.send_keys('u0283323')  # 此处填入密码
# 获取截图
browser.get_screenshot_as_file('tempimg/screenshot.png')

# 获取指定元素位置
element = browser.find_element_by_id('img')
left = int(element.location['x'])
top = int(element.location['y'])
right = int(element.location['x'] + element.size['width'])
bottom = int(element.location['y'] + element.size['height'])

# 通过Image处理图像
im = Image.open('tempimg/screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('tempimg/random.png')

img = Image.open('tempimg/random.png')
code = pytesseract.image_to_string(img)

randomcode = browser.find_element_by_id('randomCode')
randomcode.send_keys(code)
browser.find_element_by_class_name('bm-lr-btn').click()

time.sleep(10)

for x in range(1, 50):

    # 第一次学习
    # 课程页面
    cou_url = (cou_url_list[random.randint(1, sum - 1)])
    print(cou_url)
    browser.get(cou_url)
    browser.find_element_by_class_name('bm-lr-btn').click()
    print(browser.page_source)
    cou_obj = BeautifulSoup(browser.page_source, 'lxml')

    clslist = cou_obj.findAll('a', {"class": "c-p-title"})  # 找到课程标题
    print(clslist)
    play_icon = cou_obj.findAll('a', {"class": "c-p-title"})
    time.sleep(1000)
#     timelist = cou_obj.findAll('small', {"class": "vam fsize12 c-ccc f-fM"})  # 找到课程时长
#     # print(timelist)
    li_list = cou_obj.findAll('li')  # 找到课程
    # print('li_list::::%s' %li_list)
#     # print(len(li_list))
#     # print(len(clslist))
#
    for li in li_list:
        if "视频播放" in str(li):
            end_time = time.time()
            study_time = (end_time - start_time) / 60
            print('已学习%s分' % study_time)
            shichang = re.findall(r'\d+分\d+秒', li_html)
            shichang = re.findall(r'\d+', str(shichang))
            shichang = int(shichang[0]) * 60 + int(shichang[1])
            percent = re.findall(r'\d+\%', li_html)
            percent = re.findall(r'\d+', str(percent))
            percent = int(percent[0])
            print('看视频')
            print("本视频长%s秒" % shichang)
            print("已学习百分之%d" % percent)
            t = shichang * (100 - percent) * 0.01
            browser.find_element_by_id(id).click()
            time.sleep(15)
            browser.find_element_by_id('N-course-box').click()
            time.sleep(t + 20)
            print(li.get_text() + "学习完毕")
            print('\n')
            print('\n')
            browser.refresh()

#         li_html = str(li)
#         print(li_html)
#         id = re.findall(r'kp_\d+', li_html)
#         id = ''.join(id)
#         print(id)
#         time.sleep(10)
#
#
#         if "视频播放" in browser.page_source:
#
#
#
#
        else:
            print('读文字')
            browser.find_element_by_id(id).click()
            time.sleep(5)
            print(li.get_text() + "学习完毕")
            print('\n')
            print('\n')
            browser.refresh()
#
browser.quit()
exit()
#
