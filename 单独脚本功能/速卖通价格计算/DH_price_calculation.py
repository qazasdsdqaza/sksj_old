import re
import datetime
import requests
from bs4 import BeautifulSoup
import xlrd
import xlwings as xw
# import pandas as pd


# df = xw.Book('./速卖通前三十国物流方式.xlsx').sheets('公斤价格').range('A1:T78')
# da = df.value
# # DA = da[2][2]
# dd = pd.read_excel('速卖通前三十国物流方式.xlsx',sheet_name='公斤价格')
# data = dd.values.tolist()


aa = xlrd.open_workbook('速卖通前三十国物流方式.xlsx')
ab = aa.sheet_by_name("公斤价格")
ac = ab._cell_values

af = ac[2][6]
for row in ab._cell_values:
    orderid = row[0]
    shipno = row[1]



now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d %H:%M:%S')

sheet1 = de.sheet_by_name("公斤价格")
# A1 = sheet1._cell_values[4]
# A11 = A1[1]

# for row in sheet1._cell_values:
#     if row[0]!='订单号':
#         orderid = str(round(row[0]))
#         shipno = row[1]
#         if shipno.startswith('TH'):
#             carrier = 'yanwen'
#         elif shipno.startswith('L'):
#             carrier = 'china-ems'
#         elif shipno.startswith('YT'):
#             carrier = 'yunexpress'
#         else:
#             carrier = 'sf-express'
#         url = 'https://cn.tophatter.com/seller/orders/'+orderid+'/fulfill.json'
#         params = {
#             'utf8': '✓',
#             'shipped_at': '{now} -0700',
#             'tracking_number': shipno,
#             'tracking_type': carrier,
#             'commit': 'Save Tracking #',
#         }
#         print(orderid+'单号更换为:',shipno,carrier)
#         # res = s.post(url, params)
#         try:
#             res = res.json()
#             print(orderid, res['action']+'更换成功')
#             print('')
#         except:
#             print(orderid+'： 更换失败')
#             print('')
print('')
print('******替换完成******')
input("输入回车键结束")