# -*- coding: utf-8 -*-
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import requests
import re
import json
import random
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract
from pytesseract import image_to_string

browser = webdriver.Chrome()
browser.implicitly_wait(60 * 3)
browser.maximize_window()

start_time = time.time()


def login(ume, pwd):  # 登录函数

    # 登录页面
    login_url = "https://www.sxgbxx.gov.cn/login"
    browser.get(login_url)

    username = browser.find_element_by_id('userEmail')
    username.send_keys(ume)  # 此处填入账号
    password = browser.find_element_by_id('userPassword')
    password.send_keys(pwd)  # 此处填入密码
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


def peixun():
    """专题培训学习"""
    print('专题学习')
    with open('peixun_url.txt', 'r') as f:
        cou_url_list = f.read().splitlines()

        sum = len(cou_url_list)

    for x in range(1, 50):  # 每次随机学习，学习50次

        # 培训页面
        pei_url = (cou_url_list[random.randint(1, sum - 1)])
    # for pei_url in cou_url_list:
        browser.get(pei_url)
        print('--------------------------------------')
        print(pei_url)
        # print(browser.page_source)

        browser.find_element_by_xpath(
            '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li').click()  # 切换到培训内容详情页

        # print(browser.page_source)
        cou_obj = BeautifulSoup(browser.page_source, 'lxml')
        time.sleep(3)
        li_list = cou_obj.findAll('li')  # 找到所有培训课程
        # print('--------------------------------------')
        # print(li_list)

        for li in li_list:

            end_time = time.time()
            study_time = (end_time - start_time) / 60
            print('已学习%s分' % study_time)

            li_html = str(li)
            # print('--------------------------------------')
            # print(li_html)
            if 'kpoint_list' not in li_html:
                continue
            id = re.findall(r'kp_\d+', li_html)
            id = ''.join(id)
            print(id)

            if '视频播放' in li_html:
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                print('看视频')
                print("本视频长%s秒" % shichang)
                print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element_by_id(id).click()
                time.sleep(3)
                action = ActionChains(browser)
                title = browser.find_element_by_xpath(
                    '//*[@id="N-course-box"]/article/div/div[2]/section/h3/span')  # 鼠标移动到标题
                action.move_to_element(title).perform()
                action.move_by_offset(10, 50).send_keys(Keys.SPACE).perform()  # 移动到距离当前位置(10,50)的点单击空格
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '音频播放' in li_html:
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                print('听音频')
                print("本音频长%s秒" % shichang)
                print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element_by_id('yp_play').click()
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '随堂小测验' in li_html:
                continue

            else:
                print('读文字')
                browser.find_element_by_id(id).click()
                time.sleep(5)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()


def keicheng():
    """课程学习"""
    print('课程学习')
    with open('cou_url.txt', 'r') as f:
        cou_url_list = f.read().splitlines()

        sum = len(cou_url_list)
    for x in range(1, 50):

        # 课程页面
        cou_url = (cou_url_list[random.randint(1, sum - 1)])
        # for pei_url in cou_url_list:
        browser.get(cou_url)
        print("----------------------------")
        print(cou_url)

        browser.find_element_by_xpath(
            '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li').click()  # 切换到培训内容详情页
        print('--------------------------------------')
        # print(browser.page_source)
        cou_obj = BeautifulSoup(browser.page_source, 'lxml')
        time.sleep(3)
        li_list = cou_obj.findAll('li')  # 找到所有培训课程
        # print('--------------------------------------')
        # print(li_list)

        for li in li_list:

            end_time = time.time()
            study_time = (end_time - start_time) / 60
            print('已学习%s分' % study_time)

            li_html = str(li)
            # print('--------------------------------------')
            # print(li_html)
            if 'kpoint_list' not in li_html:
                continue
            id = re.findall(r'kp_\d+', li_html)
            id = ''.join(id)
            print(id)

            if '视频播放' in li_html:
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                print('看视频')
                print("本视频长%s秒" % shichang)
                print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element_by_id(id).click()
                time.sleep(3)
                action = ActionChains(browser)
                title = browser.find_element_by_xpath(
                    '//*[@id="N-course-box"]/article/div/div[2]/section/h3/span')  # 鼠标移动到标题
                action.move_to_element(title).perform()
                action.move_by_offset(10, 50).send_keys(Keys.SPACE).perform()  # 移动到距离当前位置(10,50)的点单击空格
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '音频播放' in li_html:
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                print('听音频')
                print("本音频长%s秒" % shichang)
                print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element_by_id('yp_play').click()
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '随堂小测验' in li_html:
                continue

            else:
                print('读文字')
                browser.find_element_by_id(id).click()
                time.sleep(5)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()


# 完成登录功能
ume = 'u0283323'
pwd = 'u0283323'
login(ume, pwd)

# 完成课程学习功能
# keicheng()

# 完成专题培训学习功能
peixun()
