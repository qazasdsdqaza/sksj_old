import re
import datetime
import requests
import time
from bs4 import BeautifulSoup, Tag
import xlrd,json
import xlwt
from xlutils.copy import copy

from selenium import webdriver
from time import sleep
aa = True

try:
    driver = webdriver.Chrome('./chromedriver.exe')
    # 用get打开速卖通主
    driver.get("https://www.aliexpress.com/")
    # 找到输入框，并输入“关键词”
    aa = 'прнтер'
    driver.find_element_by_id('search-key').send_keys('rrrfrf')
    sleep(1)
    # # 处理弹出的警告页面
    try:
        driver.find_element_by_class_name('close-layer').click()
        sleep(1)
        print('关闭弹窗')
    except:
        print('无弹窗')
    # 点击搜索按钮
    driver.find_element_by_class_name('search-button').click()
    sleep(1)
    aa = driver.page_source
    bb =  re.findall(r'enKeyword":"(.+?)","i18n_language', aa)
    print('开始翻译')
except:
    print('错误0')


try:
    workbook1 = xlrd.open_workbook('./热搜词-原始.xlsx')  # 文件路径
    da = workbook1.sheet_by_name("Sheet0")
    xlsc = copy(workbook1)  # 将xlrd对象拷贝转化为xlwt对象
    shtc = xlsc.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    热搜词 = da._cell_values
    i=0
    for row in 热搜词:
        while aa == True:
            try:
                目标词 = row[1]
                sleep(2)
                try:
                    driver.find_element_by_class_name('next-dialog-close').click()
                    sleep(1)
                    print('关闭弹窗')
                except:
                    print('')
                driver.find_element_by_id('search-key').clear()
                sleep(1)
                driver.find_element_by_id('search-key').send_keys(目标词)
                sleep(1)
                # 点击搜索按钮
                driver.find_element_by_class_name('search-button').click()
                sleep(1)

                aa = driver.page_source
                bb =  re.findall(r'enKeyword":"(.+?)","i18n_language', aa)
                shtc.write(row[0], 2, bb[0])
                print(row[1]+'翻译为：'+ bb[0])
                xlsc.save('热搜词-EN.xlsx')  # 保存文件名
                aa = True
            except:
                print('错误2')
                aa = False
                sleep(600)
except:
    print('错误1')

print('******翻译完成******')
input("输入回车键结束")


