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
            driver.set_page_load_timeout(120)
            try:
                # driver.get("https://cn.tophatter.com/seller/orders?filter=shipped&sort=paid_at_asc")
                driver.get("https://cn.tophatter.com/seller/orders?filter=shipped&tracking_status=unknown")
            except TimeoutException:
                print('！time out after 10 seconds when loading page！')
                driver.execute_script("window.stop()")
                # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作

            sleep(5)
            print('登录中...')
            driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div[2]/div[1]/button').click()
            sleep(5)
            driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div/div[1]/input[1]').send_keys(账户名)
            sleep(5)
            driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div/div[1]/input[2]').send_keys(登录密码)
            sleep(5)
            driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div/div[1]/button[1]').click()
            sleep(60)
            print('登录成功')
            login_status = False
    except Exception as e:
        print('登录不成功')
        login_status = True
        print(e)

worksheet.write(0, 0, label='订单号')
worksheet.write(0, 1, label='物流单号')
workbook.save('刷新了物流信息的订单.xlsx')
while status:
    if status==True:
        try:
            for i in range(50):
                index = index + 1
                It = str(i+1)
                if bb==0:
                    try:
                        driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[3]/div/table/tbody/tr[3]/td[2]/a').click()
                        bb = 0
                        订单号 = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[1]/p/a').text
                        物流单号 = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[3]/div/table/tbody/tr[3]/td[2]/a').text
                        print('刷新完成('+ str(index) +')：'+订单号 +'—'+ 物流单号)
                        worksheet.write(index, 0, label=订单号)
                        worksheet.write(index, 1, label=物流单号)
                        workbook.save('刷新了物流信息的订单.xlsx')
                    except:
                        bb = 3
                if bb==3:
                    try:
                        driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[3]/div/table/tbody/tr[5]/td[2]/a').click()
                        订单号 = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[1]/p/a').text
                        物流单号 = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[3]/div/table/tbody/tr[5]/td[2]/a').text
                        bb = 0
                        print('刷新完成('+ str(index) +')：'+订单号 +'—'+ 物流单号)
                        worksheet.write(index, 0, label=订单号)
                        worksheet.write(index, 1, label=物流单号)
                        workbook.save('刷新了物流信息的订单.xlsx')
                    except:
                        bb = 5
                if bb==5:
                    try:
                        driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[3]/div/table/tbody/tr[7]/td[2]/a').click()
                        订单号 = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[1]/p/a').text
                        物流单号 = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr['+ It +']/td[3]/div/table/tbody/tr[7]/td[2]/a').text
                        bb = 0
                        print('刷新完成('+ str(index) +')：'+订单号 +'—'+ 物流单号)
                        worksheet.write(index, 0, label=订单号)
                        worksheet.write(index, 1, label=物流单号)
                        workbook.save('刷新了物流信息的订单.xlsx')
                    except:
                        bb = 0
                        print('无订单号')
                sleep(2)
        except Exception as e:
            print('刷新错误：'+e)

    page = page + 1
    try:
        # driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[4]/ul/li['+str(page)+']/a').click()
        driver.get("https://cn.tophatter.com/seller/orders?filter=shipped&page="+str(page)+"&tracking_status=unknown")
        print('')
        sleep(20)
        print('当页为：'+ str(page))
        status = True
        try:
            订单号 = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[3]/table/tbody/tr[1]/td[1]/p/a').text
        except:
            status = False
            print('翻页完成1')
    except :
        status = False
        print('翻页错误')

print('******  全部刷新完成--保存为：刷新了物流信息的订单.xlsx  ******')
input("输入回车键结束")


