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
from selenium.webdriver.common.keys import Keys

# 变量
login_status = True
index = 0
index1 = 0
index2 = 0
index3 = 0

# 创建一个worksheet
workbook3 = xlwt.Workbook(encoding = 'utf-8')
worksheet2 = workbook3.add_sheet('已截图成功的订单')
worksheet3 = workbook3.add_sheet('已截图失败的订单')
worksheet4 = workbook3.add_sheet('无订单信息的订单')

#获取登录信息
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

#登录账号
while login_status:
    try:
        if login_status == True:
            driver = webdriver.Chrome('./chromedriver.exe')
            # 用get打开目标网页
            print('')
            print('访问目标网页...')
            driver.set_page_load_timeout(120)
            try:
                driver.get("https://cn.tophatter.com/seller/orders?filter=all")
                driver.maximize_window()
                driver.implicitly_wait(6)
            except TimeoutException:
                print('！time out after 10 seconds when loading page！')
                driver.execute_script("window.stop()")
                # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
            sleep(5)
            print('登录中...')
            #driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div[2]/div[1]/button').click()
            driver.find_element_by_xpath('/html/body/div[9]/div/div[2]/div/div[3]/div/div[2]/div[1]/button').click()
            sleep(5)
            # driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div/div[1]/input[1]').send_keys(账户名)
            driver.find_element_by_xpath('/html/body/div[9]/div/div[2]/div/div[3]/div/div/div[1]/input[1]').send_keys(账户名)
            sleep(5)
            # driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div/div[1]/input[2]').send_keys(登录密码)
            driver.find_element_by_xpath('/html/body/div[9]/div/div[2]/div/div[3]/div/div/div[1]/input[2]').send_keys(登录密码)
            sleep(5)
            # driver.find_element_by_xpath('//*[@id="reg"]/div/div/div/div/div[3]/div/div/div[1]/button[1]').click()
            driver.find_element_by_xpath('/html/body/div[9]/div/div[2]/div/div[3]/div/div/div[1]/button[1]').click()
            sleep(30)
            print('登录成功')
            login_status = False
    except Exception as e:
        print('登录不成功')
        login_status = True
        print(e)
        driver.quit();

#获取截图
try:
    worksheet2.write(0, 0, label='订单号')
    worksheet2.write(0, 1, label='物流单号')
    worksheet2.write(0, 2, label='店铺名')
    worksheet2.write(0, 3, label='截图状态')

    worksheet3.write(0, 0, label='订单号')
    worksheet3.write(0, 1, label='物流单号')
    worksheet3.write(0, 2, label='店铺名')
    worksheet3.write(0, 3, label='截图状态')

    worksheet4.write(0, 0, label='订单号')
    worksheet4.write(0, 1, label='物流单号')
    worksheet4.write(0, 2, label='店铺名')
    worksheet4.write(0, 3, label='截图状态')

    workbook3.save('截图订单状态.xlsx')

    workbook2 = xlrd.open_workbook('./索赔订单.xlsx')  # 文件路径
    db = workbook2.sheet_by_name("Sheet1")
    内容2 = db._cell_values
    for row in 内容2:
        try:
            index = index + 1
            a = str(row[0])
            b = str(row[1])
            c = str(row[2])
            if row[0] != '订单号':
                try:
                    订单号 = a[0:9]
                    运单号 = b
                    账号名 = c
                    driver.find_element_by_xpath('//*[@id="q"]').clear()
                    sleep(1)
                    driver.find_element_by_xpath('//*[@id="q"]').send_keys(订单号)
                    sleep(1)
                    driver.find_element_by_xpath('//*[@id="q"]').send_keys(Keys.ENTER)
                    sleep(3)
                    aa = driver.find_element_by_xpath('//*[@id="bulk_actions"]/div/div[2]/span').text #判断是否有订单信息
                    if aa == 'NO ORDERS FOUND':
                        index3 = index3 + 1
                        worksheet4.write(index3, 0, label=订单号)
                        worksheet4.write(index3, 1, label=运单号)
                        worksheet4.write(index3, 2, label=账号名)
                        worksheet4.write(index3, 3, label='无订单信息-'+aa)
                        workbook3.save('截图订单状态.xlsx')
                    elif aa == 'DISPLAYING 1 ORDER':
                        index1 = index1 + 1
                        driver.get_screenshot_as_file('./截图文件夹/' + str(index1) + '-(' + 订单号 + ')-(' + 运单号 + ').png')
                        sleep(2)
                        print('成功-' + 订单号)
                        worksheet2.write(index1, 0, label=订单号)
                        worksheet2.write(index1, 1, label=运单号)
                        worksheet2.write(index1, 2, label=账号名)
                        worksheet2.write(index1, 3, label='截图成功')
                        workbook3.save('截图订单状态.xlsx')
                    else:
                        print('获取失败-' + 订单号)
                        index2 = index2 + 1
                        worksheet3.write(index2, 0, label=a)
                        worksheet3.write(index2, 1, label=b)
                        worksheet3.write(index2, 2, label=c)
                        worksheet3.write(index2, 3, label='截图失败')
                        workbook3.save('截图订单状态.xlsx')
                except:
                    print('获取失败-'+ 订单号 )
                    index2 = index2 + 1
                    worksheet3.write(index2, 0, label=a)
                    worksheet3.write(index2, 1, label=b)
                    worksheet3.write(index2, 2, label=c)
                    worksheet3.write(index2, 3, label='截图失败')
                    workbook3.save('截图订单状态.xlsx')
        except Exception as e:
            print(e)
            try:
                index2 = index2 + 1
                worksheet3.write(index2, 0, label=str(row[0]))
                worksheet3.write(index2, 1, label=str(row[1]))
                worksheet3.write(index2, 2, label=str(row[2]))
                worksheet3.write(index2, 3, label='截图失败')
                workbook3.save('截图订单状态.xlsx')
            except Exception as e:
                print(e)
except Exception as e:
    print(e)
    print('请确认索赔订单的文件正常')

print('******  全部获取完成  ******')
input("输入回车键结束")


