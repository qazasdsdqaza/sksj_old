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
from selenium.common.exceptions import TimeoutException

# 变量
status = True
login_status = True
page = 1
bb=0
index = 0
number = 0

# 创建一个worksheet
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('已刷新的订单')

try:
    workbook1 = xlrd.open_workbook('./登录信息.xlsx')  # 文件路径
    da = workbook1.sheet_by_name("Sheet0")
    内容 = da._cell_values
    for row in 内容:
        账户代号 = row[0]
        账户名 = row[1]
        登录密码 = row[2]
    print('账户代号:'+账户代号)
    print('账户名:' + 账户名)
except:
    print('请在文件中输入账号名和密码')

while login_status:
    try:
        if login_status == True:
            driver = webdriver.Chrome('./chromedriver.exe')
            # 用get打开目标网页
            print('')
            print('访问目标网页...')
            driver.set_page_load_timeout(60)
            try:
                driver.get("https://www.dianxiaomi.com/tracking/index.htm")
            except TimeoutException:
                print('！time out after 10 seconds when loading page！')
                driver.execute_script("window.stop()")
                # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作

            sleep(5)
            print('登录中...')
            driver.find_element_by_xpath('//*[@id="exampleInputName"]').send_keys(账户名)
            sleep(3)
            driver.find_element_by_xpath('//*[@id="exampleInputPassword"]').send_keys(登录密码)
            sleep(30)
            driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
            sleep(20)
            print('登录成功')
            login_status = False
    except Exception as e:
        print('登录不成功')
        driver.execute_script("window.stop()")
        login_status = True
        print(e)
driver.get("https://www.dianxiaomi.com/tracking/index.htm")
sleep(10)

print('开始刷新订单……')
worksheet.write(0, 0, label='订单号')
worksheet.write(0, 1, label='物流单号')
worksheet.write(0, 2, label='包裹号')
workbook.save('刷新了物流信息的订单.xlsx')

driver.find_element_by_xpath('//*[@id="pageList"]/div[1]/ul/li[4]/a/span[1]').click()
数量_未查到 = driver.find_element_by_xpath('//*[@id="pageList"]/div[1]/ul/li[4]/a/span[2]/span').text
数量_未查到 = int(数量_未查到)
print(数量_未查到)
sleep(10)
while status:
    if 数量_未查到 < index :
        status = False

    if status==True:
        try:
            for i in range(50):
                index = index + 1
                number = number + 1
                It = str(i*2+1)
                try:
                    driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[9]/div[1]/a').click()
                    sleep(4)
                    订单号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[2]/span').text
                    物流单号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[4]/span[3]').text
                    包裹号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[2]/a').text

                    print('刷新完成('+ str(index) +')：'+订单号[1:-1] +'—'+ 物流单号[1:-1])
                    worksheet.write(number, 0, label=订单号)
                    worksheet.write(number, 1, label=物流单号)
                    worksheet.write(number, 2, label=包裹号)
                    workbook.save('刷新了物流信息的订单.xlsx')
                except:
                    print('刷新失败')
        except Exception as e:
            print('刷新错误：'+e)
    try:
        print('正在翻页……')
        driver.find_element_by_xpath('//*[@id="downPageOrder"]/li[5]/a').click()
        sleep(15)
        当前页 = driver.find_element_by_xpath('//*[@id="downPageOrder"]/li[7]/a').text
        print('当页为：'+ 当前页)
    except :
        status = False
        print('翻页错误')

status = True
index = 0
driver.find_element_by_xpath('//*[@id="pageList"]/div[1]/ul/li[5]/a/span[1]').click()
数量_运输中 = driver.find_element_by_xpath('//*[@id="pageList"]/div[1]/ul/li[5]/a/span[2]/span').text
数量_运输中 = int(数量_运输中)
print(数量_运输中)
sleep(10)
while status:
    if 数量_运输中 < index :
        status = False

    if status==True:
        try:
            for i in range(50):
                index = index + 1
                number = number+1
                It = str(i*2+1)
                try:
                    driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[9]/div[1]/a').click()
                    sleep(4)
                    订单号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[2]/span').text
                    物流单号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[4]/span[3]').text
                    包裹号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[2]/a').text

                    print('刷新完成('+ str(index) +')：'+订单号[1:-1] +'—'+ 物流单号[1:-1])
                    worksheet.write(number, 0, label=订单号)
                    worksheet.write(number, 1, label=物流单号)
                    worksheet.write(number, 2, label=包裹号)
                    workbook.save('刷新了物流信息的订单.xlsx')
                except:
                    print('刷新失败')
        except Exception as e:
            print('刷新错误：'+e)
    try:
        print('正在翻页……')
        driver.find_element_by_xpath('//*[@id="downPageOrder"]/li[5]/a').click()
        sleep(15)
        当前页 = driver.find_element_by_xpath('//*[@id="downPageOrder"]/li[7]/a').text
        print('当页为：'+ 当前页)
    except :
        status = False
        print('翻页错误')

status = True
index = 0
driver.find_element_by_xpath('//*[@id="pageList"]/div[1]/ul/li[6]/a/span[1]').click()
数量_到达待取 = driver.find_element_by_xpath('//*[@id="pageList"]/div[1]/ul/li[6]/a/span[2]/span').text
数量_到达待取 = int(数量_到达待取)
print(数量_到达待取)
sleep(10)
while status:
    if 数量_到达待取 < index :
        status = False

    if status==True:
        try:
            for i in range(50):
                index = index + 1
                number = number+1
                It = str(i*2+1)
                try:
                    driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[9]/div[1]/a').click()
                    sleep(4)
                    订单号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[2]/span').text
                    物流单号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[4]/span[3]').text
                    包裹号 = driver.find_element_by_xpath('//*[@id="dhSysMsg"]/tr['+It+']/td[2]/a').text

                    print('刷新完成('+ str(index) +')：'+订单号[1:-1] +'—'+ 物流单号[1:-1])
                    worksheet.write(number, 0, label=订单号)
                    worksheet.write(number, 1, label=物流单号)
                    worksheet.write(number, 2, label=包裹号)
                    workbook.save('刷新了物流信息的订单.xlsx')
                except:
                    print('刷新失败')
        except Exception as e:
            print('刷新错误：'+e)
    try:
        print('正在翻页……')
        driver.find_element_by_xpath('//*[@id="downPageOrder"]/li[5]/a').click()
        sleep(15)
        当前页 = driver.find_element_by_xpath('//*[@id="downPageOrder"]/li[7]/a').text
        print('当页为：'+ 当前页)
    except :
        status = False
        print('翻页错误')

print('******  全部刷新完成--保存为：刷新了物流信息的订单.xlsx  ******')
input("输入回车键结束")


