import re
import datetime
import requests
import time
from bs4 import BeautifulSoup, Tag
import xlrd
from xlutils.copy import copy
import xlwt

print('使用注意：1、cookies过期需要替换。')
print('欢迎使用获取untrackable订单信息工具，正在请求、请稍后……')

now = datetime.datetime.now() - datetime.timedelta(hours=16)
now = now.strftime('%Y-%m-%d %H:%M:%S')

with open('./cookie.txt') as file:
    cookies = file.read()
print(cookies)

workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('untrackable订单号运单号')

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',#
    'cookie': cookies,  #实验账号: 'uuid=26145870; uuid=26145870; attendee_session_id=9940bc25-32fc-4da2-9a50-e6db06dd85a0; visit_uuid=671b4637-3810-47bb-9f34-47c102d151d3; visit_user_id=26145870; ab.storage.userId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%2226145870%22%2C%22c%22%3A1608200097851%2C%22l%22%3A1608200097851%7D; ab.storage.deviceId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%22d0a74439-be33-6ca1-e689-b910b818e7c1%22%2C%22c%22%3A1608200097858%2C%22l%22%3A1608200097858%7D; uuid=26145870; hubspotutk=39fa1c72fcb1e0fb4ba9eb61e0753db4; __hssrc=1; referrer=https%3A%2F%2Fcn.tophatter.com%2Fseller%2Forders; ab.storage.sessionId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%2288938eb3-4237-f23e-2172-75d7a7925589%22%2C%22e%22%3A1611320399632%2C%22c%22%3A1611318599634%2C%22l%22%3A1611318599634%7D; _auction_session=PwDtc4XiXldfukDykiqTw0gFPHg%2B4BhqFpo%2B3dhrMEdyI%2F51AVEAV%2BkGFY5MB%2FPQcmRpmxZYZVlqIxIuJlr1Wq5DvXjU7989%2FZ6gMhYptK%2BcdbHtqZLzbTRYU94DdzErvEJyA6qcoz8Gdz%2FPtI0%2FDPUuUN0eqtCt%2Bfv8iOJC1JiMz0tTpP9XqyYK51kLENCBedG04yCwRD6QLplWv0DwKV0m8Z%2F%2BCzYW7VtD39RvfHFTJG0hnP%2FT5DTffKobblvW63xOj%2BCjebAPQmDWwI8q%2BoQUGf%2Bp551Khs1bc54YrisfjMEkouhlpo2%2Bx%2BagQcoMvwgezRzoVOX%2Fc2uWKR4gB0%2FAWg26UoZFlslyY1LJSJ6bj66OWFnIk%2BFGBn5EF%2ByIqH1ST%2BbkjJyipbQK3mh4ZLfFC3QNiKoUfd1Wdot%2BLP6sScrpZichbDXudHR%2F%2FbxegAAXDLiwcVYg5p%2BkrRU59ubkMOmNHApcq%2FLelc4bZ0dpi4OWEC40bJGOlAx2zrp7V7nv5WYUKJviATEQJJ50fY1K6g3bSQAxY8ZKJMLQsqOdyH%2B3iPMkWErkbxHXp90GS7H2HVMOQ2bmF%2BZV4%2FwObRqpnyW4k6nflJfk3F%2FYwvZ7fDal1r%2BdLXXLfRGOBjw694S3%2FAHfPdbN1JNtNGzIuc9lIBFZjRFRP%2F44ciM3U3meE0o%2Fqk%2BjhesRkD7%2FBFzCHH3AFNnXh4%2BXrf3DxyNiwCzm9%2FCrC%2FvoNsldhQ5gIKQ7a8FZ9OOwNv4ys2EvBaXoIL9%2Br%2BySwPJ9iwFTeESKVzRxD0J6%2FJhfrD9TPHI9KX3X8bohlbvecAKP6f9TrMO50ZE8Eji6A0m7--ptL8f49vTASeBNwW--RyuL%2FUtZRDPR2wcFyT5R5w%3D%3D; __hstc=55247156.39fa1c72fcb1e0fb4ba9eb61e0753db4.1608200178815.1611316843387.1611324403568.152; __hssc=55247156.1.1611324403568',
    'HOST': 'cn.tophatter.com',
    'referer': 'https://cn.tophatter.com/seller/orders?filter=shipped&tracking_status=unknown',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
}
i=0
worksheet.write(0, 0, label='订单ID')
worksheet.write(0, 1, label='承运商')
worksheet.write(0, 2, label='运单号')
worksheet.write(0, 3, label='物流状态')
workbook.save('untrackable订单.xls')
try:
    s = requests.session()
    s.headers.update(headers)
    # proxy = {
    #     'https': 'socks5://114.115.132.69:1081',#  (I)
    #     'http' : 'socks5://114.115.132.69:1081'
    # }
    # s.proxies.update(proxy)
    res = s.get('https://cn.tophatter.com/seller/orders?filter=shipped&tracking_status=unknown', timeout=60)  #dispute order id
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
    loop = 1
    while loop:
        try:
            s0 = requests.session()
            s0.headers.update(headers)
            # s0.proxies.update(proxy)
            res = s0.get('https://cn.tophatter.com/seller/orders?filter=shipped&page='+str(pg)+'&tracking_status=unknown', timeout=60)  #dispute order id
            soup = BeautifulSoup(res.text, 'html.parser')
            loop = 0
        except:
            soup = ''
            print('重复访问')
            loop = 1
    ####### 获取并分析数据#######
    try:
        html_buynows_4 = soup.find('table', {"class": "table"}).tbody.find_all('tr', recursive=False)
        for html_buynows4 in html_buynows_4:
            try:
                buynows_oders_ID = html_buynows4.find('a', {"class": "left5"}).text######################## oders_ID
                buynows_oders_ID = re.sub('\n', '', buynows_oders_ID)

                buynows_oders_wuliu = html_buynows4.find('table',{"class":"table-bordered"}).tbody.find_all('tr', recursive=False)[-1]

                buynows_oders_chengyunshang = buynows_oders_wuliu.find_all('td')[0].text  ######################## chengyunshang
                buynows_oders_yundangID     = buynows_oders_wuliu.find_all('td')[1].text  ######################## yundangID
                buynows_oders_wuliuzhuagtai = buynows_oders_wuliu.find_all('td')[2].text  ######################## wuliuzhuagtai

                i = i + 1
                # 参数对应 行, 列, 值
                worksheet.write(i, 0, label=buynows_oders_ID)
                worksheet.write(i, 1, label=buynows_oders_chengyunshang)
                worksheet.write(i, 2, label=buynows_oders_yundangID)
                worksheet.write(i, 3, label=buynows_oders_wuliuzhuagtai)
                workbook.save('untrackable订单.xls')
                print('第'+ str(i) + '个数据保存成功')
            except Exception as e:
                print('第'+ str(i) + '个数据保存失败')
                print(e)
    except Exception as e:
        print(e)


print('')
print('******获取完成******')
input("输入回车键结束")