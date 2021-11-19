import re
import datetime
import requests
import time
from bs4 import BeautifulSoup, Tag
import xlrd
from xlutils.copy import copy
import xlwt
import json

print('准备替换5M，正在请求、请稍后……')

now = datetime.datetime.now() - datetime.timedelta(hours=16)
now = now.strftime('%Y-%m-%d %H:%M:%S')

user = xlrd.open_workbook('./user_mssge.xlsx')
de = xlrd.open_workbook('./input.xlsx')

# 创建一个worksheet
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('失败单号')

user = user.sheet_by_name("Sheet1")
for row in user._cell_values:
    账号名 = row[0]
    账号API = row[1]

print('账号名：'+账号名 +'      账号API：'+账号API)

sheet1 = de.sheet_by_name("Sheet1")
worksheet.write(0, 0, label='商品ID')
worksheet.write(0, 1, label='视频地址')
worksheet.write(0, 2, label='失败类型')
workbook.save('替换失败商品.xls')
i=0
sheet1 = de.sheet_by_name("Sheet1")
for row in sheet1._cell_values:
    if row[0] !='商品ID':
        ID = str(int(row[0]))
        main_image_url = row[1]
        image_set = []
        ll = len(row)
        try:
            for j in range(2,len(row)-1):
                if row[j] != '':
                    image = {'image_url':row[j]}
                    image_set.append(image)
        except:
            print(ID+'无详图')
        headers = { 'X-Api-Key': 账号API}
        data = {
            'goods_id': ID,
            'main_image_url': main_image_url,
            'image_set':image_set,
        }
        try:
            data = json.dumps(data)
            subm = requests.post('https://hibiscus.5miles.com/api/v1/products/update.json', data=data, headers=headers, timeout=40)
            if subm.status_code == 200:
                print('替换成功：'+ID)
            else:
                print('失败：' + ID)
                i = i + 1
                worksheet.write(i, 0, label=ID)
                worksheet.write(i, 1, label=main_image_url)
                worksheet.write(i, 2, label='替换失败')
                workbook.save('替换失败商品.xls')
        except:
            print('失败：' + ID)
            i = i + 1
            worksheet.write(i, 0, label=ID)
            worksheet.write(i, 1, label=main_image_url)
            worksheet.write(i, 2, label='替换失败')
            workbook.save('替换失败商品.xls')

input("输入回车键结束")
print('******替换完成******')
input("输入回车键结束")