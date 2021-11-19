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

import http.client
import hashlib
import urllib
import random
import json

print('******开始翻译******')
sleep(1)
workbook1 = xlrd.open_workbook('./热搜词-EN.xlsx')  # 文件路径
da = workbook1.sheet_by_name("Sheet0")
xlsc = copy(workbook1)  # 将xlrd对象拷贝转化为xlwt对象
shtc = xlsc.get_sheet(0)  # 获取转化后工作簿中的第一个表格
热搜词_英文 = da._cell_values
i=0
for row in 热搜词_英文:
    try:
        sleep(1)
        目标词 = row[2]
        appid = '20200320000401524'  # 填写你的appid
        secretKey = 'wfZF8NSk_uL32Jjkc76B'  # 填写你的密钥
        httpClient = None
        myurl = '/api/trans/vip/translate'
        fromLang = 'auto'   #原文语种
        toLang = 'zh'   #译文语种
        salt = random.randint(32768, 65536)
        q= 目标词
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            # print (result)
        except Exception as e:
            print (e)
        finally:
            if httpClient:
                httpClient.close()

        aa = result['trans_result'][0]['dst']
        shtc.write(row[0], 3, aa)
        print(row[2]+'翻译为：'+ aa)
        xlsc.save('热搜词-英到汉.xlsx')  # 保存文件名
    except:
        print(目标词 + '-》翻译错误')
print('******翻译完成******')
input("输入回车键结束")
