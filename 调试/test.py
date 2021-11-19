import re
import datetime
import requests
import time
from bs4 import BeautifulSoup, Tag
import xlrd, json, csv
from ast import literal_eval
import xlwt

from selenium import webdriver
from time import sleep
from selenium.common.exceptions import TimeoutException

print('获取5miles 资金数据')
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive',
#     'Cookie': 'ga=GA1.2.1015007459.1587694690; lang=ZH_CN; csrfToken=40MempJI-AX6sScZMJUfzV0U; _gid=GA1.2.1054963006.1591959976; x_header=%7B%22userId%22%3A19021255%2C%22userName%22%3A%22519761979@qq.com%22%2C%22role%22%3A%22Seller%20Backend%22%2C%22email%22%3A%22519761979@qq.com%22%2C%22token%22%3A%22eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTE5NjAwMzQuOTUyLCJleHAiOjE1OTQ1NTIwMzQuOTUyLCJwYXlsb2FkIjp7InVzZXJJZCI6MTkwMjEyNTUsInVzZXJOYW1lIjoiNTE5NzYxOTc5QHFxLmNvbSJ9fQ.yWeF8TF1UnNcZFwcH6cqpJ6hy0X3x_HlQl20tG9dcI4%22%2C%22account%22%3A%225%22%7D; _gat_gtag_UA_51595858_21=1; EGG_SESS=4V96HOMfDP1tnlI3rqREjXgEPzb7-nyfY5Sbqi9oEdW5SrWniLzyDQcBWIfLQX8u8WwXY8SxH4Q5KnTAxH5O43PvcUNBcqgTfpljvBp7wxz3Rt201vElRdc1RE3-44cBZ4Ttv0e_PVl7nDh5lhVHTRIIzlYq5vGT7IiMuESGmEGVw75GoNA3qzWq9KEqDUPi7EItju7c3pcGvEfZ7IBOEYiu4hhvHNKYTmjZ2rolfj5akURc48B7b8v11TekttpCNYqDAOYWSP4bTswALXsJiA==; RT="z=1&dm=5milesapp.com&si=d6afa183-c886-475a-a5e0-295a54391404&ss=kbc3v52b&sl=4&tt=97l&obo=1&rl=1&nu=529e4p9o&cl=2dzc&ld=2dzd&r=34lcqbuv&ul=2dze"',
#     'Host': 'b.5milesapp.com',
#     'Referer': 'https://b.5milesapp.com/payment/balance',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
# }
# time.sleep(2)  # 延时2秒，避免请求过于频繁。
# ######################################## upcoming ###############################
# s = requests.session()
# s.headers.update(headers)
# res = s.get('https://b.5milesapp.com/payment/balance', timeout=60)
# if res.status_code != 200:
#     print('cookie过期，请更新！')
#     input("输入回车键结束")
# else:
#     print('cookie正常！')
# soup = BeautifulSoup(res.text, 'html.parser')
# csrf_token_0 = soup.find('table', {"class": "order-info-table"}).text
# # print(csrf_token_0)
# 可提现 = re.search(r'(?<=[现]).*?(?=[待确认])', csrf_token_0).group(0)
# 可提现 = re.sub('[,]', '', 可提现)
# 可提现 = re.sub('[ ]', '', 可提现)
# 可提现 = re.sub('[$]', '', 可提现)
#
# 待确认 = re.search(r'(?<=[认]).*?(?=[提现中])', csrf_token_0).group(0)
# 待确认 = re.sub('[,]', '', 待确认)
# 待确认 = re.sub('[ ]', '', 待确认)
# 待确认 = re.sub('[$]', '', 待确认)
#
# 提现中 = re.search(r'[^提现中]+$', csrf_token_0).group(0)
# 提现中 = re.sub('[,]', '', 提现中)
# 提现中 = re.sub('[ ]', '', 提现中)
# 提现中 = re.sub('[$]', '', 提现中)

print('获取正确的Lots_ID')
# 获取正确的Lots_ID
# try:
#     # 1 获取正确的Lots_ID
#     url = ('https://cn.tophatter.com/lots/' + str(156097195))
#     # t = requests.session()
#     # t.proxies.update(proxy)
#     LOTS = requests.get(url, timeout=20)
#     lots_id = str(158451638)
#     print(LOTS.status_code)
#     if LOTS.status_code == 200:
#         lots_id = LOTS.url
#         lots_id = re.findall(r'com/lots/(.+?)$', lots_id)[0]
# except:
#     lots_id = str('没有')
#
# print(lots_id)

print('获取网页数据')
# #获取网页数据
# try:
#     driver = webdriver.Chrome('F:\E_commerce\e_commerce_app\chromedriver.exe')
#     driver.set_page_load_timeout(120)
#     try:
#         driver.get('https://cn.tophatter.com/lots/' + str(79423859))
#     except TimeoutException:
#         print('！time out after 10 seconds when loading page！')
#         driver.execute_script("window.stop()")
#     sleep(3)
#
#     产品标题 = driver.find_element_by_xpath('//*[@id="lot-modal"]/h3').text
#
#     items = True
#     line = 0
#     while items:
#         try:
#             line = line + 1
#             Its_0 = driver.find_element_by_xpath('//*[@id="details"]/div/div['+str(line)+']/h5').text
#             if Its_0 == 'Description:':
#                 items = False
#         except:
#             items = True
#             line = line + 1
#     print(line)
#
#     try:
#         Its_1 = driver.find_element_by_xpath('//*[@id="details"]/div/div['+str(line)+']/p[1]').text
#     except:
#         Its_1 = ''
#     try:
#         Its_2 = driver.find_element_by_xpath('//*[@id="details"]/div/div['+str(line)+']/p[2]').text
#     except:
#         Its_2 = ''
#     try:
#         Its_3 = driver.find_element_by_xpath('//*[@id="details"]/div/div['+str(line)+']/p[3]').text
#     except:
#         Its_3 = ''
#     try:
#         Its_4 = driver.find_element_by_xpath('//*[@id="details"]/div/div['+str(line)+']/p[4]').text
#     except:
#         Its_4 = ''
#     try:
#         Its_5 = driver.find_element_by_xpath('//*[@id="details"]/div/div['+str(line)+']/p[5]').text
#     except:
#         Its_5 = ''
#
#     产品材料=''
#     产品条件=''
#     产品尺寸=''
#     产品颜色=''
#     产品描述=''
#
#     if Its_1[0:8] == 'Material':
#         产品材料 = Its_1[10:]
#     elif Its_1[0:9]=='Condition':
#         产品条件 = Its_1[11:]
#     elif Its_1[0:15]=='Available Sizes':
#         产品尺寸 = Its_1[17:]
#     elif Its_1[0:16]=='Available Colos':
#         产品颜色 = Its_1[18:]
#     elif Its_1 !='':
#         产品描述 = Its_1
#     else:
#         Its_1 =Its_1
#
#     if Its_2[0:9]=='Condition':
#         产品条件 = Its_2[11:]
#     elif Its_2[0:15]=='Available Sizes':
#         产品尺寸 = Its_2[17:]
#     elif Its_2[0:16]=='Available Colors':
#         产品颜色 = Its_2[18:]
#     elif Its_2 !='':
#         产品描述 = Its_2
#     else:
#         Its_2 =Its_2
#
#     if Its_3[0:15]=='Available Sizes':
#         产品尺寸 = Its_3[17:]
#     elif Its_3[0:16]=='Available Colors':
#         产品颜色 = Its_3[18:]
#     elif Its_3 !='':
#         产品描述 = Its_3
#     else:
#         Its_3 =Its_3
#
#     if Its_4[0:15]=='Available Sizes':
#         产品尺寸 = Its_4[17:]
#     elif Its_4[0:16]=='Available Colors':
#         产品颜色 = Its_4[18:]
#     elif Its_4 !='':
#         产品描述 = Its_4
#     else:
#         Its_4 =Its_4
#
#     if Its_5[0:15]=='Available Sizes':
#         产品尺寸 = Its_5[17:]
#     elif Its_5[0:16]=='Available Colors':
#         产品颜色 = Its_5[18:]
#     elif Its_5 !='':
#         产品描述 = Its_5
#     else:
#         Its_5 =Its_5
#
#
#     # print(产品标题)
#     #
#     # print('产品材料:'+产品材料)
#     # print('产品条件:'+产品条件)
#     # print('产品尺寸：'+产品尺寸)
#     # print('产品颜色:'+产品颜色)
#     # print('产品描述:'+产品描述)
#
#
#     try:
#         产品图片1 = driver.find_element_by_xpath('//*[@id="lot-modal"]/div/div/div[2]/div/img[1]').get_attribute('src')
#     except:
#         产品图片1 = ''
#     try:
#         产品图片2 = driver.find_element_by_xpath('//*[@id="lot-modal"]/div/div/div[2]/div/img[2]').get_attribute('src')
#     except:
#         产品图片2 = ''
#     try:
#         产品图片3 = driver.find_element_by_xpath('//*[@id="lot-modal"]/div/div/div[2]/div/img[3]').get_attribute('src')
#     except:
#         产品图片3 = ''
#     try:
#         产品图片4 = driver.find_element_by_xpath(
#             '//*[@id="lot-modal"]/div/div/div[2]/div/img[4]').get_attribute('src')
#     except:
#         产品图片4 = ''
#     try:
#         产品图片5 = driver.find_element_by_xpath(
#             '//*[@id="lot-modal"]/div/div/div[2]/div/img[5]').get_attribute('src')
#     except:
#         产品图片5 = ''
#     try:
#         产品图片6 = driver.find_element_by_xpath(
#             '//*[@id="lot-modal"]/div/div/div[2]/div/img[6]').get_attribute('src')
#     except:
#         产品图片6 = ''
#     try:
#         产品图片7 = driver.find_element_by_xpath(
#             '//*[@id="lot-modal"]/div/div/div[2]/div/img[7]').get_attribute('src')
#     except:
#         产品图片7 = ''
#     try:
#         产品图片8 = driver.find_element_by_xpath(
#             '//*[@id="lot-modal"]/div/div/div[2]/div/img[8]').get_attribute('src')
#     except:
#         产品图片8 = ''
#     try:
#         产品图片9 = driver.find_element_by_xpath(
#             '//*[@id="lot-modal"]/div/div/div[2]/div/img[9]').get_attribute('src')
#     except:
#         产品图片9 = ''
#
#     # print(产品图片1)
#     # print(产品图片2)
#     # print(产品图片3)
#     # print(产品图片4)
#     # print(产品图片5)
#     # print(产品图片6)
#     # print(产品图片7)
#     # print(产品图片8)
#     driver.close()
# except Exception as e:
#     print(e)

print('5mils上传产品调试')
# headers = {'X-Api-Key': '1QWINZM8lW8HqQOfO4HVP1WGyh0J1B0c77fesHXz' }
# values ={
#     "goods_no": "test111",
#     "name": "My Goods 002",
#     "main_image_url": "https://www.baidu.com/cache/icon/favicon.ico",
#     "cat_name": "Electronics",
#     "description": "p descadddddddddddaffddddddsssssddddddddddddddddddddddfffffffffffffffffffffffffffffffffeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
#     "purchase_price": 30,
#     "min_delivery_days": 40,
#     "max_delivery_days": 50,
#     "delivery_address": "CN",
#     "weight": "99g",
#     "image_set": [
#       {
#         "image_url": "https://www.baidu.com/cache/icon/favicon.ico"
#       }
#     ],
#     "sku_set": [
#       {
#         "sku_no": "01",
#         "total_stock": 6,
#         "color": "blue",
#         "size": "em do"
#       }
#     ]
#   }
# data=json.dumps(values)
# subm = requests.post('https://hibiscus.5miles.com/api/v1/products.json', data=data, headers=headers, timeout=20)
# print("status code:", subm.status_code)
# aa = subm.text
# reponse_dicts = json.loads(aa)
# print(reponse_dicts)

print('5mils获取订单调试')
# headers = {'X-Api-Key': '1QWINZM8lW8HqQOfO4HVP1WGyh0J1B0c77fesHXz'}
# subm = requests.get(
#     # 'https://hibiscus.5miles.com/api/v2/orders.json?offset=0&limit=10&state=&created_at_start=2020-06-06&created_at_end=2020-06-12',
#     'https://hibiscus.5miles.com/api/v1/metadata/categories.json',
#     headers=headers, timeout=20)
# print("status code:", subm.status_code)
# aa = subm.text
# reponse_dicts = json.loads(aa)
# print(reponse_dicts['result']['objects'])

print('获取TOP网页图片')
# url = 'https://images.tophatter.com/c9dd82e1d6c21de8724b347f085d64b8/original.jpg'
# subm = requests.get(url,timeout=20)
# print("status code:", subm.status_code)
# open('C:\\IMG_TOP\\TOPIMG-'+url[29:-13]+'.jpg', 'wb').write(subm.content)
# print(subm.content)

print('获取top单个商品')
subm = requests.get(
    'https://tophatter.com/merchant_api/v1/products/retrieve.json?access_token=2f9a6837ddb548932118fb57b625f3b3&identifier=C-Bluetooth-200604',timeout=100)
# subm = requests.get('https://tophatter.com/merchant_api/v1/products.json?access_token='+store_APIToken+'&identifier=6631A',timeout=100)
print("status code:", subm.status_code)
aa = subm.text
reponse_dict = json.loads(aa)

# # 2 保存到数据库
# identifier = reponse_dict.get('identifier') #SKU
# buy_now_price = reponse_dict.get('buy_now_price') #一口价
# cost_basis = reponse_dict.get('cost_basis') #目标价
# retail_price = reponse_dict.get('retail_price') #零售价
# reserve_price = reponse_dict.get('reserve_price')#底价
# scheduling_fee_bid = reponse_dict.get('scheduling_fee_bid') #SFB
# shipping_price = reponse_dict.get('shipping_price') #运费
# campaign_name = reponse_dict.get('campaign_name') #camp 名字
#
# upsells = reponse_dict.get('upsells') #运费
# print(upsells)
# upsells = literal_eval(str(upsells))
# if len(upsells) == 1:
#     accessory_price = str(upsells[0]['amount']) #运费价格
#     accessory_price = re.sub('[.0]', '', accessory_price)
#     accessory_description = upsells[0]['description'] #运费描述
# elif len(upsells) == 2:
#     accessory_price = str(upsells[1]['amount'])  # 运费价格
#     accessory_price = re.sub('[.0]', '', accessory_price)
#     accessory_description = upsells[1]['description']  # 运费描述

print('获取top单个订单')
# subm = requests.get(
#     'https://tophatter.com/merchant_api/v1/orders/retrieve.json?access_token=f3dd4e25dd83481203342913a1f9fcf6&order_id=119885462', #119885462
#     timeout=100)
# # subm = requests.get('https://tophatter.com/merchant_api/v1/products.json?access_token='+store_APIToken+'&identifier=6631A',timeout=100)
# print("status code:", subm.status_code)
# aa = subm.text
# reponse_dict = json.loads(aa)
# print(reponse_dict)

print('获取top的campaign')
# subm = requests.get(
#     'https://tophatter.com/merchant_api/v1/campaigns.json?access_token=419ec468e95f54e9eb0dabb281726dc1', #119885462
#     timeout=100)
# print("status code:", subm.status_code)
# aa = subm.text
# reponse_dict = json.loads(aa)
# print(reponse_dict)


print('获取1688商品')
# headers = {
#                 'accept': 'application/json, text/plain, */*',
#                 'accept-encoding': 'gzip, deflate, br',
#                 'accept-language': 'zh-CN,zh;q=0.9',
#                 'cookie':'cna=EmrOFp/BljACAdzK4SGLlsdj; UM_distinctid=17221e73df55f1-0deb8a9bf6a3c7-366b420b-1fa400-17221e73df67d6; taklid=e70ffddee78949d496ad00ce0896b5b7; ali_ab=223.104.130.126.1592382840551.6; h_keys="%u9648%u82e5%u4eea%u540c%u6b3e#454"; lid=%E8%8C%B6%E5%B1%B1%E6%99%93; ali_apache_track=c_mid=b2b-1048120505|c_lid=%E8%8C%B6%E5%B1%B1%E6%99%93|c_ms=1; cookie2=1a28d52b2254d35ca8a211750761d3bf; t=e5084e9ae4073198a5f697306fa6ce47; _tb_token_=f58b515583775; ad_prefer="2020/07/30 22:12:17"; _m_h5_tk=84ab115100e95bc30009843cb46505a6_1596128417228; _m_h5_tk_enc=7012748d0da76d881d0fe20e4842140a; alicnweb=touch_tb_at%3D1596118339585%7Clastlogonid%3D%25E8%258C%25B6%25E5%25B1%25B1%25E6%2599%2593%7Cshow_inter_tips%3Dfalse; ali_apache_tracktmp=c_w_signed=Y; last_mid=b2b-1048120505; _is_show_loginId_change_block_=b2b-1048120505_false; _show_force_unbind_div_=b2b-1048120505_false; _show_sys_unbind_div_=b2b-1048120505_false; _show_user_unbind_div_=b2b-1048120505_false; __rn_alert__=false; CNZZDATA1253659577=2143456442-1589704349-https%253A%252F%252Fszyx.1688.com%252F%7C1596114362; x5sec=7b226c61707574613b32223a22386431326165313736326466303230633231646633333634343666623132346543495375692f6b46454d6532364e79512b71723862513d3d227d; tfstk=cmEGBOgZkPusVDu3PGi_3sSMJFbdZ_-qZorQYlBidMDrjoEFiQLezwqhKfVgDE1..; cookie1=AQXGWdmblW5WoXqI4XsGrARSKvRfthmAJbkcMuRFVtE%3D; cookie17=UoH7I2hF38Rqwg%3D%3D; sg=%E6%99%9353; csg=13c9c2b9; unb=1048120505; uc4=nk4=0%400xJhXEjJrQTti6eUhc5lddo%3D&id4=0%40UOnkRzNd%2FFJGBMlLp9eH5YYND9vo; __cn_logon__=true; __cn_logon_id__=%E8%8C%B6%E5%B1%B1%E6%99%93; _nk_=%5Cu8336%5Cu5C71%5Cu6653; _csrf_token=1596119064044; JSESSIONID=219DA53A5BD4EDA9DC1CFFD3B7BB1FCE; l=eBad4Om4Qc-2c5GEBO5aourza779wIRb4sPzaNbMiInca6gPEFZtONQq0FWvmdtjgt1xKeKrbrEboRLHR3fG-vlmF41FS-eInxf..; isg=BPf3gThPZOxN3eE4KWnhYyqshutBvMse8soB8kmkokYt-Bc6UI47brWS2limEKOW',
#                 'HOST': 'detail.1688.com',
#                 'referer': 'https://cn.tophatter.com/seller/orders?filter=shipped&tracking_status=unknown',
#                 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#                 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#             }
# s = requests.session()
# s.headers.update(headers)
# res = s.get('https://detail.1688.com/offer/565980387287.html?spm=a262or.11066063.pdtodl.dlitm1.1c5f8f33vS4EmB',timeout=60)  # home页 GOTO 提醒数据
# print("status code:", res.status_code)
# soup_home_GOTO = BeautifulSoup(res.text, 'html.parser')
# html_home_GOTOS_name = soup_home_GOTO.find('a',{"class": "box-img"}).find_all()
# print(html_home_GOTOS_name)
# # # 2 保存到数据库

print('测试代理IP')
# IP = '175.6.146.250' + ':' + '1081' #182.61.13.26
# proxies_founds = {
#     'http': 'socks5://{}'.format(IP),
#     'https': 'socks5://{}'.format(IP)
# }
# s = requests.session()
# s.proxies.update(proxies_founds)
# res = s.get('http://myip.ipip.net/')
# soup = BeautifulSoup(res.text, 'html.parser').text[:-1]
# print(soup)
# time.sleep(2) #延时2秒，避免请求过于频繁。

print('议价商品接收或拒绝')
# try:
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'accept-encoding': 'gzip, deflate, br',
#         'accept-language': 'zh-CN,zh;q=0.9',
#         'cookie': 'uuid=25720956; visit_uuid=c8f8465d-10c5-4a0c-b0f8-98b4f3481653; visit_user_id=25720956; ab.storage.userId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%2225720956%22%2C%22c%22%3A1596707672630%2C%22l%22%3A1596707672630%7D; ab.storage.deviceId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%22cb9dd17c-bb75-4639-bd4a-e79b15144626%22%2C%22c%22%3A1596707672635%2C%22l%22%3A1596707672635%7D; messagesUtk=ca0bf6ee5cdc4c2a90db4e1d0cb77434; hubspotutk=02aef7cc29c87be19803a7938c2100ca; pulse_badge=true; _ga=GA1.2.1040056036.1597054143; _gcl_au=1.1.1735805522.1601104436; ab.storage.sessionId.b7f13edb-826b-483c-aaa5-db246d0be23e=%7B%22g%22%3A%2258c07729-f712-2062-e752-ba91cf7487be%22%2C%22e%22%3A1607669021551%2C%22c%22%3A1607667221552%2C%22l%22%3A1607667221552%7D; attendee_session_id=5095a5e2-a165-4589-8890-88b6707dc322; __hssrc=1; referrer=https%3A%2F%2Fcn.tophatter.com%2Fseller%2Fname_your_price_offers%3Fcounter%3Duncountered%26filter%3Dall%26page%3D1%26per_page%3D10%26sort%3Ddate_desc%26status%3Dall; campaign=%7B%22type%22%3D%3E%22NameYourPriceCampaign%22%2C+%22name%22%3D%3E%22YJ2.55%22%2C+%22lifetime_budget%22%3D%3E%221000000%22%2C+%22bid_amount%22%3D%3E%222.55%22%2C+%22daily_budget_per_product%22%3D%3E%22%22%2C+%22daily_budget%22%3D%3E%22%22%2C+%22lifetime_budget_per_product%22%3D%3E%22%22%2C+%22hourly_schedule%22%3D%3E%3CActionController%3A%3AParameters+%7B%220%22%3D%3E%221%22%2C+%221%22%3D%3E%221%22%2C+%222%22%3D%3E%221%22%2C+%223%22%3D%3E%221%22%2C+%224%22%3D%3E%221%22%2C+%225%22%3D%3E%221%22%2C+%226%22%3D%3E%221%22%2C+%227%22%3D%3E%221%22%7D+permitted%3A+true%3E%7D; __hstc=55247156.02aef7cc29c87be19803a7938c2100ca.1596707701227.1608272516791.1608277806036.592; __hstc=55247156.02aef7cc29c87be19803a7938c2100ca.1596707701227.1608272516791.1608277806036.592; __hssc=55247156.18.1608277806036; _auction_session=XPJlAQkAgLM6d4yt1VkCQAplAIugM4wRsiPrAT32K1ZB4i%2FKlmEgaKCpxJRm92Mh0qXrSs%2FFF%2B9oN0ZmN6NbhWrjjxrwP77RdZScRI79qwXzwggm%2FnD8DGOqR7YgL2Za0IR%2BrlbIzuRaVu%2BB3x7XmJeNCfe3dz%2Bs4Etacvg9z8HzOVqZ7H%2BRJD9ex6FRLMhUZnsD6vqQQ%2B%2ByPTNW10fVgfe0T8vT8KVFmcPKWMBD8QeibMBNIzfItqRT4CmYnOh%2BtnK7U21SK1gyBSstKn1fWGzelAMFxjWrplr3t384437loPGr2Fc9rD1JYjeFJFAkkFARVCotZMlQL673fLCl7Q6VnjWN%2BcfnnYjwXz%2FMVv2Gfr6ZSjhxbqRX%2Fkq%2Fc49kLS9lwDVggYSthgtvBgIwav9z5OlgCW0z7v9783oFdcoHF47e2fzdXluIdTdMsuIybmiIi9RvMJv7nSE6I1T8y6m%2Fq%2FSbrWB%2BVOgb%2BEv5rErbglRSQT0OStLUFG0WfGtU3J2Fdnhsk%2BAEPkCr3VV5PJ1Q%2FpwOBkO3T6mogI45BUNjm8Yr6W9K%2F%2BSJZ2%2B%2FTVusd%2BzxDTlBbjqvvcVDjG%2FClehtZXYiM1Bso%2FuEcTaBQQwDZBVtRButlUOMs50vai54ONcXEdIMaDnFk%2FmUtu1lMZ0PVSHiCAN7GZ8vFD2OwSYV%2F0pe8oXcQ05NhUXUU7t4gH1UPCo5Wbi8YdHEvQ5YbPcmo0wgulypO%2FCwZfPZCNj9zSi0bM13oD71T4jhmk13CX5rp3T67urdGCgIJtU6c%2BIT753YmyhBuWXWl4SNmJT6gGq8B7gTbgX2Xbm3CBmQ2vfGF7cAvkRp4hmRTRSXkyGK1KQ3A7yXzHW8VNxsnFfddk0%2FkLTEU4GYqOu4OBV5PH987doDn5f5Z160Ma2YHxZ%2FPEAWv2%2BYbohWZB0a2pTplh4GwS480mW4yqMsut4VeRMAa28RJyyJITSldQB3e%2B9EGnuQSCHa92IwcrFMA5j9hMTApn7%2FK0VrBFPkyEH6aCs9%2BeY%3D--dfltaYNJbigmQnsZ--QXA8pdFoYNnWTZu0GZh9VQ%3D%3D',
#         'HOST': 'cn.tophatter.com',
#         # 'referer': 'https://cn.tophatter.com/seller/name_your_price_offers?counter=uncountered&filter=all&page=1&per_page=10&sort=date_desc&status=all',
#         'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     }
#
#     ######################################## IP地址数据 ########################
#     # s = requests.session()
#     # s.proxies.update(proxy)
#     # res = s.get('http://myip.ipip.net/')
#     # soup = BeautifulSoup(res.text, 'html.parser').text[:-1]
#     # print(soup)
#     # time.sleep(2)  # 延时2秒，避免请求过于频繁。
#
#     ######################################## upcoming ###############################
#     s = requests.session()
#     s.headers.update(headers)
#     proxy = {
#         'https': 'socks5://139.159.191.92:1081',
#         'http': 'socks5://139.159.191.92:1081'
#     }
#     s.proxies.update(proxy)
#     res = s.get('https://cn.tophatter.com/seller/name_your_price_offers?counter=uncountered&filter=all&page=1&per_page=25&sort=date_desc&status=all', timeout=60)
#     if res.status_code != 200:
#         print('cookie过期，请更新！')
#         input("输入回车键结束")
#     else:
#         print('cookie正常！')
#     soup = BeautifulSoup(res.text, 'html.parser')
#     name_your_price_offers = soup.find('table', {"class": "table"}).tbody.find_all('tr',recursive=False)
#     authenticity_token = csrf_token = soup.find('meta', {"name":"csrf-token"})['content']
#     for name_your_price_offer in name_your_price_offers:
#         try:
#             actions_status = name_your_price_offer.find('div', {"class": "text-muted text-small top5"}).text
#             if actions_status :
#                 actions_status_work = actions_status[13:21]
#                 if actions_status_work == 'accepted':
#                     actions_ID = name_your_price_offer.find('input').get('name')
#                     actions_herf ='https://cn.tophatter.com'+name_your_price_offer.find('a', {"class": "btn btn-sm btn-success"}).get('href')
#                     params = {'authenticity_token': authenticity_token}
#                     res = s.post(actions_herf, params)
#                     if res.status_code == 200:
#                         print('接收正常—accepted')
#                     else:
#                         print('接收失败—accepted！')
#                 elif actions_status_work == 'rejected':
#                     actions_ID = name_your_price_offer.find('input').get('name')
#                     actions_herf = 'https://cn.tophatter.com' + name_your_price_offer.find('a', {"class": "btn btn-sm btn-danger"}).get('href')
#                     params = {'authenticity_token': authenticity_token}
#                     res = s.post(actions_herf, params)
#                     if res.status_code == 200:
#                         print('接收正常—rejected')
#                     else:
#                         print('接收失败—rejected！')
#         except Exception as e:
#             print(e)
# except Exception as e:
#     print(e)


print('******店铺资金获取完成******')
input("输入回车键结束")

# {'primary_image': 'https://images.tophatter.com/0e988b55071713e4ea9112322db3e223/original.jpg',
#  'material': 'Silver',
#  'available_quantity': 20000,
#  'upsells': [{'description': 'Buy one get one', 'image': None, 'amount': '7.0', 'type_description': 'accessory','identifier': None}],
#  'ratings_average': None,
#  'disabled_at': None,
#  'description': 'Hello! Welcome to wis store!\n\nQuality is the first with best service. customers all are our friends. \nDescriptions:\n \nThis awesome mini wireless bluetooth headset will be a smart choice for you, looking for a pair of headphones both fashionable and popular.\nIt supports a microphone that allows you to take calls or listen to music anytime, anywhere. I\nt comes with 700mAh large charging case, charge your headphones while you do not use, up to 70 hours of music playback time.\nGet one to bring something new to your life!\n \nSpecifications:\nColor: Black\n \nMaterial: Plastic\nSize: 1,4x1,2x4cm\n \nRange: 10m\n \nBattery: 700mAh\n \nTalk time: 8 hours\n \nListen to music: About 8/70 (total) hours\n \nCharging time: about 1.2 hours\n Compatible with most Bluetooth enabled devices such as mobile phones, tablets PC and more.\nBuilt-in microphone. A key to answer a call.\n \nnvisible, smallest and ultralight design. Get rid of the cable connection, bring more comfort in sports, sports and other activities. Get rid of the problems wire.\n It comes with 700mAh large charging case, charge your headphones while you do not use, up to 70 hours of music playback time.\n \nPacking Included:\n1 x headphones\n1 x case\n\nThere is 2-3% difference according to manual measurement.\nplease check the measurement chart carefully before you buy the item.\nPlease note that slight color difference should be acceptable due to the light and screen.',
#  'all_images': [{'large': 'https://images.tophatter.com/0e988b55071713e4ea9112322db3e223/large.jpg',
#                  'thumbnail': 'https://images.tophatter.com/0e988b55071713e4ea9112322db3e223/thumbnail.jpg',
#                  'original': 'https://images.tophatter.com/0e988b55071713e4ea9112322db3e223/original.jpg',
#                  'medium': 'https://images.tophatter.com/0e988b55071713e4ea9112322db3e223/medium.jpg',
#                  'square': 'https://images.tophatter.com/0e988b55071713e4ea9112322db3e223/square.jpg'},
#                 {'large': 'https://images.tophatter.com/423763accc724e612272c7f57cec1a29/large.jpg',
#                  'thumbnail': 'https://images.tophatter.com/423763accc724e612272c7f57cec1a29/thumbnail.jpg',
#                  'original': 'https://images.tophatter.com/423763accc724e612272c7f57cec1a29/original.jpg',
#                  'medium': 'https://images.tophatter.com/423763accc724e612272c7f57cec1a29/medium.jpg',
#                  'square': 'https://images.tophatter.com/423763accc724e612272c7f57cec1a29/square.jpg'},
#                 {'large': 'https://images.tophatter.com/0ee26b99c6d39dfc3b2d08b7ac34c610/large.jpg',
#                  'thumbnail': 'https://images.tophatter.com/0ee26b99c6d39dfc3b2d08b7ac34c610/thumbnail.jpg',
#                  'original': 'https://images.tophatter.com/0ee26b99c6d39dfc3b2d08b7ac34c610/original.jpg',
#                  'medium': 'https://images.tophatter.com/0ee26b99c6d39dfc3b2d08b7ac34c610/medium.jpg',
#                  'square': 'https://images.tophatter.com/0ee26b99c6d39dfc3b2d08b7ac34c610/square.jpg'},
#                 {'large': 'https://images.tophatter.com/d7e599717e62dbdd87082b4adfe6f246/large.jpg',
#                  'thumbnail': 'https://images.tophatter.com/d7e599717e62dbdd87082b4adfe6f246/thumbnail.jpg',
#                  'original': 'https://images.tophatter.com/d7e599717e62dbdd87082b4adfe6f246/original.jpg',
#                  'medium': 'https://images.tophatter.com/d7e599717e62dbdd87082b4adfe6f246/medium.jpg',
#                  'square': 'https://images.tophatter.com/d7e599717e62dbdd87082b4adfe6f246/square.jpg'},
#                 {'large': 'https://images.tophatter.com/92278fff72d68fcec8c32235ea45a0a8/large.jpg',
#                  'thumbnail': 'https://images.tophatter.com/92278fff72d68fcec8c32235ea45a0a8/thumbnail.jpg',
#                  'original': 'https://images.tophatter.com/92278fff72d68fcec8c32235ea45a0a8/original.jpg',
#                  'medium': 'https://images.tophatter.com/92278fff72d68fcec8c32235ea45a0a8/medium.jpg',
#                  'square': 'https://images.tophatter.com/92278fff72d68fcec8c32235ea45a0a8/square.jpg'},
#                 {'large': 'https://images.tophatter.com/a4c30468fe77e92af14f3498093d7934/large.jpg',
#                  'thumbnail': 'https://images.tophatter.com/a4c30468fe77e92af14f3498093d7934/thumbnail.jpg',
#                  'original': 'https://images.tophatter.com/a4c30468fe77e92af14f3498093d7934/original.jpg',
#                  'medium': 'https://images.tophatter.com/a4c30468fe77e92af14f3498093d7934/medium.jpg',
#                  'square': 'https://images.tophatter.com/a4c30468fe77e92af14f3498093d7934/square.jpg'},
#                 {'large': 'https://images.tophatter.com/ef826adf9f14c07515b19d11ee1d450a/large.jpg',
#                  'thumbnail': 'https://images.tophatter.com/ef826adf9f14c07515b19d11ee1d450a/thumbnail.jpg',
#                  'original': 'https://images.tophatter.com/ef826adf9f14c07515b19d11ee1d450a/original.jpg',
#                  'medium': 'https://images.tophatter.com/ef826adf9f14c07515b19d11ee1d450a/medium.jpg',
#                  'square': 'https://images.tophatter.com/ef826adf9f14c07515b19d11ee1d450a/square.jpg'}],
#  'expedited_shipping_price': None,
#  'days_to_deliver': 14,
#  'campaign_name': None,
#  'created_at': '2020-06-04T07:22:10-07:00',
#  'brand': '',
#  'buy_one_get_one_price': None,
#  'reserve_price': None,
#  'ratings_count': 0,
#  'title': 'Bluetooth 5.0 Sport Wireless Headphone Earbuds HIFI Headset Mini True',
#  'extra_images': 'https://images.tophatter.com/423763accc724e612272c7f57cec1a29/original.jpg|https://images.tophatter.com/0ee26b99c6d39dfc3b2d08b7ac34c610/original.jpg|https://images.tophatter.com/d7e599717e62dbdd87082b4adfe6f246/original.jpg|https://images.tophatter.com/92278fff72d68fcec8c32235ea45a0a8/original.jpg|https://images.tophatter.com/a4c30468fe77e92af14f3498093d7934/original.jpg|https://images.tophatter.com/ef826adf9f14c07515b19d11ee1d450a/original.jpg',
#  'condition': 'New',
#  'minimum_bid_amount': 1.0,
#  'retail_price': 15,
#  'shipping_origin': 'China',
#  'fulfillment_partner': None,
#  'scheduling_fee_bid': None,
#  'category': 'Electronics | Other',
#  'variations': [
#     {'identifier': 'C-Bluetooth-Black-200604', 'created_at': '2020-06-04T07:22:10-07:00', 'internal_id': 64445680,
#      'disabled_at': None, 'quantity': 10000, 'color': 'Black', 'size': None, 'deleted_at': None},
#     {'identifier': 'C-Bluetooth-White-200604', 'created_at': '2020-06-04T07:22:10-07:00', 'internal_id': 64445679,
#      'disabled_at': None, 'quantity': 10000, 'color': 'White', 'size': None, 'deleted_at': None}],
#  'buy_now_price': '10.0',
#  'cost_basis': 10.0,
#  'buy_one_get_one_available': False,
#  'weight': None,
#  'expedited_days_to_deliver': None,
#  'internal_id': 25056280,
#  'shipping_price': 0,
#  'max_daily_schedules': None,
#  'updated_at': '2020-06-04T14:19:29-07:00',
#  'deleted_at': None,
#  'identifier': 'C-Bluetooth-200604',
#  'days_to_fulfill': 5}


