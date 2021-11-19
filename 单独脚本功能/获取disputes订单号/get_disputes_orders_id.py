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

with open('./cookie.txt') as file:
    cookies = file.read()

workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('Disputes_订单')

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
i=0
worksheet.write(0, 0, label='订单ID')
worksheet.write(0, 1, label='SKU')
worksheet.write(0, 2, label='amount')
worksheet.write(0, 3, label='INR')
worksheet.write(0, 4, label='status')
workbook.save('Disputes_订单.xls')
try:
    s = requests.session()
    s.headers.update(headers)
    res = s.get('https://cn.tophatter.com/seller/disputes?filter=closed&refund_status=all&sort=paid_at_asc&tracking_status=all', timeout=60)  #dispute order id
    soup_page = BeautifulSoup(res.text, 'html.parser')
except:
    soup_page = ''

pages = soup_page.find('ul', {"class": "pagination"}).find_all('li')
for pages0 in pages:
    if pages0.text != 'Next →':
        page = pages0.text
print('共多少页：'+page)
for pg in range(1,int(page)+1):
    print('正在获取第几页数据：'+str(pg))
    try:
        s = requests.session()
        s.headers.update(headers)
        res = s.get('https://cn.tophatter.com/seller/disputes?filter=closed&page='+str(pg)+'&refund_status=all&sort=paid_at_asc&tracking_status=all', timeout=60)  #dispute order id
        soup = BeautifulSoup(res.text, 'html.parser')
    except:
        soup = ''
    ####### 获取并分析数据#######
    try:
        html_buynows_4 = soup.find('table', {"class": "table"}).tbody.find_all('tr')
        for html_buynows4 in html_buynows_4:
            html_buynows = html_buynows4.find_all('td')
            buynows_oders_ID = html_buynows[1].text######################## ID
            buynows_oders_SKU = html_buynows[2].text ######################## SKU
            buynows_oders_SKU = re.sub('\n', '', buynows_oders_SKU)
            buynows_oders_amount = html_buynows[3].text  ######################## amount
            buynows_oders_INR = html_buynows[6].text ################### INR
            buynows_oders_status = html_buynows[7].text  ######################## status
            buynows_oders_status = re.sub('\n', '', buynows_oders_status)

            i = i + 1
            # 参数对应 行, 列, 值
            worksheet.write(i, 0, label=buynows_oders_ID)
            worksheet.write(i, 1, label=buynows_oders_SKU)
            worksheet.write(i, 2, label=buynows_oders_amount)
            worksheet.write(i, 3, label=buynows_oders_INR)
            worksheet.write(i, 4, label=buynows_oders_status)
            workbook.save('Disputes_订单.xls')
    except Exception as e:
        print(e)


print('')
print('******获取完成******')
input("输入回车键结束")