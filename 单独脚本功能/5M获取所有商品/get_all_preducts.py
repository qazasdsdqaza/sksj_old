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
user = user.sheet_by_name("Sheet1")
for row in user._cell_values:
    账号名 = row[0]
    账号API = row[1]
print('账号名：'+账号名 +'      账号API：'+账号API)

# 创建一个worksheet
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('所有商品')

worksheet.write(0, 0, label='商品ID')
worksheet.write(0, 1, label='SKU')
workbook.save(账号名+'所有商品.xls')
i=0
headers = {'X-Api-Key': 账号API}
for PAGE in range(1, 40):
    star_page = str(100 * (PAGE - 1))
    subm = requests.get('https://hibiscus.5miles.com/api/v1/products/list.json?offset='+star_page+'&limit=100', headers=headers,timeout=50)
    print("status code:", subm.status_code)
    aa = subm.text
    reponse_dicts = json.loads(aa)
    reponse_dicts = reponse_dicts['result']['objects']
    # 2 保存到数据库
    try:
        for reponse_dict in  reponse_dicts:
            products_id = int(reponse_dict['id']) #商品ID')
            goods_no = reponse_dict['goods_no']  # 商品编号')
            i = i + 1
            worksheet.write(i, 0, label=products_id)
            worksheet.write(i, 1, label=goods_no)
            workbook.save(账号名 + '所有商品.xls')
    except:
        print('保存错误')


input("输入回车键结束")
print('******替换完成******')
input("输入回车键结束")