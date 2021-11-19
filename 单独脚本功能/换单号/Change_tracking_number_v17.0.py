import re
import datetime
import requests
import time
from bs4 import BeautifulSoup, Tag
import xlrd
from xlutils.copy import copy
import xlwt

print('使用注意：1、cookies过期需要替换。2、请将要替换的定单号和目标物流号填到指定的input.xlsx文件中')
print('')
print('欢迎使用运单号替换工具，正在请求、请稍后……')

now = datetime.datetime.now() - datetime.timedelta(hours=16)
now = now.strftime('%Y-%m-%d %H:%M:%S')

de = xlrd.open_workbook('./input.xlsx')

with open('./cookie.txt') as file:
    cookies = file.read()

workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('失败单号')

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie':cookies,  #实验账号  '_gcl_au=1.1.1351296750.1581612440; _ga=GA1.2.168407198.1581612441; visit_uuid=41af207c-b589-4762-91d6-868be3f3b18e; visit_user_id=19087314; ab.storage.userId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%2219087314%22%2C%22c%22%3A1583159089805%2C%22l%22%3A1583159089805%7D; ab.storage.deviceId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%22dab2f6bd-16a1-945e-1770-c9b6a84bab53%22%2C%22c%22%3A1583159089813%2C%22l%22%3A1583159089813%7D; pulse_badge=true; _fbp=fb.1.1588208304086.817096557; messagesUtk=ce77cda940b249ae95e6e5cda4f247b6; hubspotutk=27fc68c8b19ac3c4fc1a82298dc99ed6; attendee_session_id=14e809a8-8ee6-4be1-a6d3-ea63f2673060; __hssrc=1; referrer=https%3A%2F%2Fcn.tophatter.com%2Fseller%2Fpayouts%3Ftype%3Dready; __hstc=55247156.27fc68c8b19ac3c4fc1a82298dc99ed6.1589902135884.1594140916116.1594298605925.30; ab.storage.sessionId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%2254c02f03-e120-6cac-178a-4144fbab621a%22%2C%22e%22%3A1594300438413%2C%22c%22%3A1594298598321%2C%22l%22%3A1594298638413%7D; _auction_session=BAh7C0kiD3Nlc3Npb25faWQGOgZFVEkiJTVmNGQxNjAwMzI3NzU0NWVjZGNmMmNkNWE3OTk4NTNhBjsAVEkiEWluaXRpYXRlZF9hdAY7AEZJdToJVGltZQ3HEB6A4h0vhQo6DW5hbm9fbnVtaQLiAToNbmFub19kZW5pBjoNc3VibWljcm8iB0ggOgtvZmZzZXRp%2FpCdOgl6b25lSSIIUERUBjsARkkiDnJldHVybl90bwY7AEYiBi9JIhBfY3NyZl90b2tlbgY7AEZJIjFENDVtTERLRWlGQXBteWtUMUQvVWxrU0VtaVhBZDhDREZWYlBZdTVzK0ZZPQY7AEZJIgx1c2VyX2lkBjsARmkE0j8jAUkiD2V4cGlyZXNfYXQGOwBGVTogQWN0aXZlU3VwcG9ydDo6VGltZVdpdGhab25lWwhJdTsGDU8UHsB0RqVwCTsHaQKtAzsIaQY7CSIHlBA7C0kiCFVUQwY7AEZJIh9QYWNpZmljIFRpbWUgKFVTICYgQ2FuYWRhKQY7AFRJdTsGDUgUHsB0RqVwCTsHaQKtAzsIaQY7CSIHlBA7C0AV--98c72e07a7566445de2a7456b9cfee153586def9; __hssc=55247156.3.1594298605925' ,
    'HOST': 'cn.tophatter.com',
    'referer': 'https://cn.tophatter.com/seller/orders?filter=shipped&tracking_status=unknown',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
}
s = requests.session()
s.headers.update(headers)
res = s.get('https://cn.tophatter.com/seller/orders?filter=shipped&sort=paid_at_asc',timeout=30)

if res.status_code != 200:
    print('cookie过期，请更新！')
    input("输入回车键结束")
else:
    print('cookie正常！')
soup = BeautifulSoup(res.text, 'html.parser')

csrf_token = soup.find('meta', {"name":"csrf-token"})['content']
source = re.search(r'"secret": "(\S+)",', res.text)
secret = source.group(1)

# print(csrf_token,'secret:'+secret)
s.headers.update({
    'X-CSRF-Token':csrf_token,
    'X-Requested-With': 'XMLHttpRequest',
    'X-User-Secret': secret,
})
# print(csrf_token,secret)
print('正在进行单号替换……')
sheet1 = de.sheet_by_name("Sheet1")
i = 0
worksheet.write(0, 0, label='订单号')
worksheet.write(0, 1, label='物流单号')
worksheet.write(0, 2, label='失败类型')
workbook.save('替换失败订单.xls')
for row in sheet1._cell_values:
    if row[0]!='订单号':
        try:
            orderid = str(int(row[0]))
        except:
            orderid = row[0]
        shipno = str(row[1])
        if shipno.startswith('TH'):
            carrier = 'yanwen'  # 燕文
        elif shipno.startswith('LY'):
            carrier = 'china-ems'  # e邮宝
        elif shipno.startswith('YT') or shipno.startswith('TP'):
            carrier = 'yunexpress'  # 云途
        elif shipno[0:2] == '92':
            carrier = 'usps'  # usps
        elif shipno[0:3] == '420' or shipno[0:2] == 'WL':
            carrier = 'ydh-express'  # 易达
        elif shipno[0:2] == '61':
            shipno = '92' + shipno  # 若usps头为61，则头前加92
            carrier = 'usps'  # usps
        elif shipno[0:3] == 'F39':
            carrier = 'flytexpress'  # 飞特
        elif shipno[0:3] == 'CUS' or shipno[0:3] == 'GCL' or shipno[0:3] == 'USE' or shipno[0:3] == 'SCL' \
             or shipno[0:3] == 'GCA' or shipno[0:3] == 'CKT' or shipno[0:3] == 'CUG' or shipno[0:3] == 'SUT':
            carrier = 'ec-firstclass'  # 出口易
        elif shipno[0:2] == 'SF':
            carrier = 'sf-express'  # 顺丰
        elif shipno[0:3] == 'WNB':
            carrier = 'wanbexpress'  # 万邦
        elif shipno[0:3] == '302' or shipno[0:3] == '303':
            carrier = '4px'  # 递四方
        elif shipno[0:3] == 'HHW':
            carrier = 'hh-exp'  # 华翰
        elif shipno[0:5] == 'TYZPH':
            carrier = 'topyou'  # 通邮
        else:
            carrier = '1'  # 无法识别
        if carrier != '1':
            url = 'https://cn.tophatter.com/seller/orders/'+orderid+'/fulfill.json'
            params = {
                'utf8': '✓',
                'shipped_at': now+' -0700',
                'tracking_number': shipno,
                'tracking_type': carrier,
                'commit': 'Save Tracking #',
            }
            print(orderid+'单号更换为:',shipno,carrier)
            res = s.post(url, params)
            try:
                res = res.json()
                print(orderid, res['action']+'更换成功')
                print('')
            except:
                print(orderid+'： 单号更换失败')
                print('')
                i = i+1
                # 参数对应 行, 列, 值
                worksheet.write(i, 0, label=orderid)
                worksheet.write(i, 1, label=shipno)
                worksheet.write(i, 2, label='替换失败')
                workbook.save('替换失败订单.xls')
        else:
            print(orderid + '： 无法识别' + shipno[0:3])
            print('')

            i = i + 1
            # 参数对应 行, 列, 值
            worksheet.write(i, 0, label=orderid)
            worksheet.write(i, 1, label=shipno)
            worksheet.write(i, 2, label='无法识别')
            workbook.save('替换失败订单.xls')
print('')
print('******替换完成******')
input("输入回车键结束")