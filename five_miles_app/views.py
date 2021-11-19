import json
import datetime,time
import random
import xlrd
# import xlwt
import requests
import re
import csv

from django.http import HttpResponse
from django.shortcuts import render, redirect ,reverse

# Create your views here.
from common_functions_app import models as models_common_functions
from Tophatter_app import models as models_Tophatter
from PruAndLog import models as models_PruAndLog
from user_app import models as models_user_app
from five_miles_app import models  as models_five_miles

from user_app import views  as user_app

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum,Count,Max,Min,Avg,Q
from django.views.generic.base import View
from bs4 import BeautifulSoup
from time import sleep

# 定时后台任务:from apscheduler.scheduler import Scheduler  #版本2.1.2
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

#selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from ast import literal_eval
from django.views.decorators.csrf import csrf_exempt

#所有订单利润统计
def FiveMiles_All_orders_profitStatistics(request):
    user_app.change_info(request, 'FiveMiles_All_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >3:
        return render(request, '../../user_app/templates/404.html')
    try:
        exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
    except:
        exchange_rate = 6.3000
    try:
        打包成本 = models_PruAndLog.key_parameter.objects.filter(USER_ID=USER_ID).values('打包成本').first()['打包成本']
    except:
        打包成本 = 1.8

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            store_name = request.GET.get('store_name', '')  # 店铺名
            order_status = request.GET.get('order_status', '')  # 订单状态
            time_local = request.GET.get('time_local', '')  # 时间段  1
            start_time = request.GET.get('start_time', '')  # 开始时间  1
            end_time = request.GET.get('end_time', '')  # 结束时间  1
            SKU = request.GET.get('SKU', '')  # SKU  1

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

            table_number = request.GET.get('table_number', '')  # 表格序号

            if limit == '' and  page == '' and  table_number == '':
                store_name_users  = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {'store_name_users':list(store_name_users)}
                return render(request, 'five_miles/FiveMiles_All_orders_profitStatistics.html',context0)

            if start_time == '':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                    days=7)).date().strftime('%Y-%m-%d')
            if end_time == '':
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')

            if time_local == 'today':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
            if time_local == 'yesterday':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')
            if time_local == 'yesterday1':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=63)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=63)).date().strftime('%Y-%m-%d')
            if time_local == 'yesterday2':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=87)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=87)).date().strftime('%Y-%m-%d')
            if time_local == 'last_7_days':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                    days=7)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
            if time_local == 'last_30_days':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                    days=30)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
            if time_local == 'last_60_days':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                    days=60)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
            if time_local == 'last_90_days':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                    days=90)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
            if time_local == 'all_time':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                    days=600)).date().strftime('%Y-%m-%d')
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')

            if store_name == '':
                store_name = 'all'
            if order_status == '':
                order_status = '全部订单'

            if Sort_field == '':
                Sort_field = 'product_sum'

            if Sort_order == 'desc' or Sort_order == '':
                Sort_order = '-'
            elif Sort_order == 'asc':
                Sort_order = ''
            else:
                Sort_order = '-'

            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            # 订单数据
            objs = models_five_miles.orders_date_5miles.objects.filter(USER_ID=USER_ID).filter(created_at_data__gte=start_time).filter(created_at_data__lte=end_time)
            if store_name != 'all':
                objs = objs.filter(store_name=store_name)
            if SKU != '':
                objs = objs.filter(sku_no__contains=SKU)
            if order_status != '全部订单':
                objs = objs.filter(state=order_status)

            if table_number == 'table_number_detail':
                count_all = objs.values('sku_no', 'store_name', 'goods_name', 'goods_main_image_url').annotate(product_sum=Count('seq_no')).count()
                objs = objs.values('sku_no', 'store_name', 'goods_name', 'goods_main_image_url'). \
                           annotate(product_sum=Count('seq_no'), \
                                    total_amount=Avg('total_amount'), \
                                    status_Approved=Count('status_Approved'), \
                                    status_Dispatched=Count('status_Dispatched'), \
                                    status_Completed=Count('status_Completed'), \
                                    status_Refunded=Count('status_Refunded'), \
                                    status_Canceled=Count('status_Canceled'), \
                                    status_Closed=Count('status_Closed')).order_by(Sort_order+Sort_field)[page_star:page_end]
            elif  table_number == 'table_number_sum':
                objs = objs.values('sku_no', 'store_name', 'goods_name', 'goods_main_image_url'). \
                           annotate(product_sum=Count('seq_no'), \
                                    total_amount=Avg('total_amount'), \
                                    status_Approved=Count('status_Approved'), \
                                    status_Dispatched=Count('status_Dispatched'), \
                                    status_Completed=Count('status_Completed'), \
                                    status_Refunded=Count('status_Refunded'), \
                                    status_Canceled=Count('status_Canceled'), \
                                    status_Closed=Count('status_Closed'))

            a = max(models_Tophatter.logistics_statistic.objects.filter(USER_ID=USER_ID).values_list('STAR_DATE'))[0]
            Its = models_Tophatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(STAR_DATE=a).values()  # 物流规则数据（匹配下单时间的物流规则）
            普货每克 = (float(Its[0]['美国_每克_普货']) * float(Its[0]['美国_折扣_普货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_每克_普货']) * float(Its[0]['英国_折扣_普货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_每克_普货']) * float(Its[0]['加拿_折扣_普货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_每克_普货']) * float(Its[0]['澳大_折扣_普货']) * float(Its[0]['澳大_销售比']) / 100)
            普货挂号 = (float(Its[0]['美国_挂号_普货']) * float(Its[0]['美国_折扣_普货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_挂号_普货']) * float(Its[0]['英国_折扣_普货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_挂号_普货']) * float(Its[0]['加拿_折扣_普货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_挂号_普货']) * float(Its[0]['澳大_折扣_普货']) * float(Its[0]['澳大_销售比']) / 100)

            带电每克 = (float(Its[0]['美国_每克_带电']) * float(Its[0]['美国_折扣_带电']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_每克_带电']) * float(Its[0]['英国_折扣_带电']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_每克_带电']) * float(Its[0]['加拿_折扣_带电']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_每克_带电']) * float(Its[0]['澳大_折扣_带电']) * float(Its[0]['澳大_销售比']) / 100)
            带电挂号 = (float(Its[0]['美国_挂号_带电']) * float(Its[0]['美国_折扣_带电']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_挂号_带电']) * float(Its[0]['英国_折扣_带电']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_挂号_带电']) * float(Its[0]['加拿_折扣_带电']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_挂号_带电']) * float(Its[0]['澳大_折扣_带电']) * float(Its[0]['澳大_销售比']) / 100)

            特货每克 = (float(Its[0]['美国_每克_特货']) * float(Its[0]['美国_折扣_特货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_每克_特货']) * float(Its[0]['英国_折扣_特货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_每克_特货']) * float(Its[0]['加拿_折扣_特货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_每克_特货']) * float(Its[0]['澳大_折扣_特货']) * float(Its[0]['澳大_销售比']) / 100)
            特货挂号 = (float(Its[0]['美国_挂号_特货']) * float(Its[0]['美国_折扣_特货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_挂号_特货']) * float(Its[0]['英国_折扣_特货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_挂号_特货']) * float(Its[0]['加拿_折扣_特货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_挂号_特货']) * float(Its[0]['澳大_折扣_特货']) * float(Its[0]['澳大_销售比']) / 100)

            COSTF_OF = 0
            NET_PROFIT = 0
            PAID_SUM = 0
            REFUN_SUM_OWN = 0
            REFUNDED_RATE = 0
            EXCHANGE_RATE = 0
            TOTAL_AMOUNT = 0
            TOTAL_AMOUNT_CN = 0
            PROFIT_MARGIN = 0
            打包总成本 = 0
            for obj in objs:
                obj['SKU_freight'] = 0
                obj['status_abnormal'] = obj['status_Refunded'] + obj['status_Canceled'] + obj['status_Closed']
                if obj['product_sum'] != 0:
                    obj['refunded_rate'] = round((obj['status_abnormal'] * 100 / obj['product_sum']), 2)
                else:
                    obj['refunded_rate'] = 0

                obj['total_amount'] = round((obj['total_amount']), 2)
                obj['total_amount_CN'] = round((obj['total_amount']) * exchange_rate, 2)
                ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['sku_no']).values('id').annotate(
                    SKU_price=Max('SKU_price')
                    , SKU_parts_price=Max('SKU_parts_price')
                    , SKU_weight=Max('SKU_weight')  # -------
                    , SKU_parts_weight=Max('SKU_parts_weight')  # -------
                    , SKU_variety=Max('SKU_variety')
                    , HAI_SKU_freight=Max('HAI_SKU_freight')  # -------
                    , Pingyou_min7_SKU_freight=Max('Pingyou_min7_SKU_freight')  # -------
                    , Pingyou_max7_SKU_freight=Max('Pingyou_max7_SKU_freight')  # -------
                    , top_colect=Max('top_colect'))  # -------
                if ob:
                    obj['SKU_price'] = ob[0]['SKU_price']  # 单价
                    obj['SKU_parts_price'] = ob[0]['SKU_parts_price']  # 配件价
                    obj['SKU_weight'] = ob[0]['SKU_weight']  # 单重量
                    obj['SKU_parts_weight'] = ob[0]['SKU_parts_weight']  # 单配件重量
                    obj['SKU_variety'] = ob[0]['SKU_variety']  # 单种类
                    obj['HAI_SKU_freight'] = ob[0]['HAI_SKU_freight']  # 单价运费
                    obj['Pingyou_min7_SKU_freight'] = ob[0]['Pingyou_min7_SKU_freight']  # 小于7美元单价
                    obj['Pingyou_max7_SKU_freight'] = ob[0]['Pingyou_max7_SKU_freight']  # 大于7美元单价
                    obj['top_colect'] = ob[0]['top_colect']  #

                    if obj['SKU_price']:
                        obj['SKU_price'] = obj['SKU_price']
                    else:
                        obj['SKU_price'] = 0

                    if obj['SKU_parts_price']:
                        obj['SKU_parts_price'] = obj['SKU_parts_price']
                    else:
                        obj['SKU_parts_price'] = 0

                    if obj['SKU_weight']:
                        obj['SKU_weight'] = obj['SKU_weight']
                    else:
                        obj['SKU_weight'] = 0

                    if obj['SKU_parts_weight']:
                        obj['SKU_parts_weight'] = obj['SKU_parts_weight']
                    else:
                        obj['SKU_parts_weight'] = 0

                    if obj['SKU_variety']:
                        obj['SKU_variety'] = obj['SKU_variety']
                        if obj['SKU_variety'] == '海运':
                            obj['SKU_variety'] = '输入运费'
                    else:
                        obj['SKU_variety'] = ''

                    if obj['HAI_SKU_freight']:
                        obj['HAI_SKU_freight'] = obj['HAI_SKU_freight']
                    else:
                        obj['HAI_SKU_freight'] = 0

                    if obj['Pingyou_min7_SKU_freight']:
                        obj['Pingyou_min7_SKU_freight'] = obj['Pingyou_min7_SKU_freight']
                    else:
                        obj['Pingyou_min7_SKU_freight'] = 0

                    if obj['Pingyou_max7_SKU_freight']:
                        obj['Pingyou_max7_SKU_freight'] = obj['Pingyou_max7_SKU_freight']
                    else:
                        obj['Pingyou_max7_SKU_freight'] = 0

                    if obj['top_colect']:
                        obj['top_colect'] = obj['top_colect']
                    else:
                        obj['top_colect'] = '否'

                    if obj['SKU_variety'] == '普货':
                        if float(obj['SKU_weight']):
                            obj['SKU_freight'] = round(((float(obj['SKU_weight']) * 普货每克) + 普货挂号), 2)
                        else:
                            obj['SKU_freight'] = 0
                        obj['SKU_parts_freight'] = round(float(obj['SKU_parts_weight']) * 普货每克, 2)
                        obj['SKU_buy_one_freight'] = round(float(obj['SKU_weight']) * 普货每克, 2)
                    elif obj['SKU_variety'] == '带电':
                        if float(obj['SKU_weight']):
                            obj['SKU_freight'] = round(((float(obj['SKU_weight']) * 带电每克) + 带电挂号), 2)
                        else:
                            obj['SKU_freight'] = 0
                        obj['SKU_parts_freight'] = round(float(obj['SKU_parts_weight']) * 带电每克, 2)
                        obj['SKU_buy_one_freight'] = round(float(obj['SKU_weight']) * 带电每克, 2)

                    elif obj['SKU_variety'] == '特货':
                        if float(obj['SKU_weight']):
                            obj['SKU_freight'] = round(((float(obj['SKU_weight']) * 特货每克) + 特货挂号), 2)
                        else:
                            obj['SKU_freight'] = 0
                        obj['SKU_parts_freight'] = round(float(obj['SKU_parts_weight']) * 特货每克, 2)
                        obj['SKU_buy_one_freight'] = round(float(obj['SKU_weight']) * 特货每克, 2)
                    elif obj['SKU_variety'] == '海运' or obj['SKU_variety'] == '输入运费':
                        obj['SKU_freight'] = round(float(obj['HAI_SKU_freight']), 2)
                        obj['SKU_parts_freight'] = 0
                        obj['SKU_buy_one_freight'] = 0
                    elif obj['SKU_variety'] == '平邮':
                        if obj['revenue_avg'] < 7:
                            obj['SKU_freight'] = round(float(obj['Pingyou_min7_SKU_freight']), 2)
                        else:
                            obj['SKU_freight'] = round(float(obj['Pingyou_max7_SKU_freight']), 2)
                        obj['SKU_parts_freight'] = 0
                        obj['SKU_buy_one_freight'] = 0
                    else:
                        obj['SKU_freight'] = 0
                        obj['SKU_parts_freight'] = 0
                        obj['SKU_buy_one_freight'] = 0

                    if obj['SKU_freight'] and obj['SKU_price']:
                        obj['suggest_buynows_price'] = round(((((float(obj['SKU_price']) + float(obj['SKU_freight'])) * 1.4 / exchange_rate) + 1.3) / 0.821) / 0.95, 2)  # 建议一口价
                    else:
                        obj['suggest_buynows_price'] = ''

                    # 实际的统计值，从订单列表获取
                    if obj['product_sum']:
                        obj['SKU_price_sum'] = round(float(obj['SKU_price']) * (
                                obj['product_sum'] - obj['status_Refunded'] - obj['status_Canceled'] - obj[
                            'status_Closed']), 2)  # 总进价
                    else:
                        obj['SKU_price_sum'] = 0

                    if obj['product_sum']:
                        obj['SKU_freight_sum'] = round(float(obj['SKU_freight']) * (
                                obj['product_sum'] - obj['status_Refunded'] - obj['status_Canceled'] - obj[
                            'status_Closed']), 2)  # 总运费
                    else:
                        obj['SKU_freight_sum'] = 0

                    obj['dabaochenben'] = 打包成本 * (obj['status_Approved'] + obj['status_Dispatched'] + obj['status_Completed'])

                    obj['cost_of'] = round((obj['SKU_price_sum'] + obj['SKU_freight_sum'] + obj['dabaochenben']), 2)  # 总成本

                    obj['Net_profit'] = (obj['total_amount_CN'] * 0.821) - (1.3 * exchange_rate)
                    obj['Net_profit'] = round(
                        ((obj['Net_profit']) * (obj['product_sum'] - obj['status_Refunded'] - obj['status_Canceled'] - obj['status_Closed']) - obj['cost_of']), 2)  # 毛利润

                    if (obj['product_sum'] - obj['status_Canceled'] - obj['status_Closed']):
                        obj['Net_profit_avg'] = round((obj['Net_profit']) / (obj['product_sum'] - obj['status_Canceled'] - obj['status_Closed']), 2)  # 平均利润
                    else:
                        obj['Net_profit_avg'] = 0

                    if obj['cost_of']:
                        obj['profit_margin'] = round((obj['Net_profit'] / obj['cost_of']) * 100, 2)  # 利润率
                    else:
                        obj['profit_margin'] = 0

                    COSTF_OF += obj['cost_of']  # 店铺总成本
                    NET_PROFIT += obj['Net_profit']  # 店铺总利润
                    if COSTF_OF:
                        PROFIT_MARGIN = round((NET_PROFIT / COSTF_OF) * 100, 2)
                    else:
                        PROFIT_MARGIN = 0
                    COSTF_OF = round((COSTF_OF), 2)
                    NET_PROFIT = round((NET_PROFIT), 2)
                else:
                    obj['SKU_price'] = ''
                    obj['SKU_parts_price'] = ''
                    obj['SKU_weight'] = ''
                    obj['SKU_parts_weight'] = ''
                    obj['SKU_variety'] = ''
                    obj['HAI_SKU_freight'] = ''
                    obj['Pingyou_min7_SKU_freight'] = ''
                    obj['Pingyou_max7_SKU_freight'] = ''
                    obj['top_colect'] = '否'
                    obj['suggest_buynows_price'] = ''
                    obj['Net_profit'] = ''
                    obj['profit_margin'] = ''
                    obj['Net_profit_avg'] = ''
                PAID_SUM += obj['product_sum']
                REFUN_SUM_OWN += obj['status_abnormal']
                TOTAL_AMOUNT += obj['total_amount']
                TOTAL_AMOUNT_CN += obj['total_amount_CN']

                if PAID_SUM:
                    REFUNDED_RATE = round((REFUN_SUM_OWN / PAID_SUM) * 100, 2)
                    TOTAL_AMOUNT = round((TOTAL_AMOUNT / PAID_SUM), 2)
                    TOTAL_AMOUNT_CN = round((TOTAL_AMOUNT_CN / PAID_SUM), 2)
                else:
                    REFUNDED_RATE = 0
                    TOTAL_AMOUNT = 0
                    TOTAL_AMOUNT_CN = 0

                TOTAL_AMOUNT += obj['total_amount']
                TOTAL_AMOUNT_CN += obj['total_amount_CN']
                TOTAL_AMOUNT = round((TOTAL_AMOUNT), 2)
                TOTAL_AMOUNT_CN = round((TOTAL_AMOUNT_CN), 2)


            EXCHANGE_RATE = exchange_rate

            context_all = {
                'code': 0,
                'msg': 'asdfgh',
                'count': 1,
                'data': [{
                'COSTF_OF': COSTF_OF,
                'NET_PROFIT': NET_PROFIT,
                'PAID_SUM': PAID_SUM,
                'REFUN_SUM_OWN': REFUN_SUM_OWN,
                'REFUNDED_RATE': REFUNDED_RATE,
                'EXCHANGE_RATE': exchange_rate,
                'TOTAL_AMOUNT': TOTAL_AMOUNT,
                'TOTAL_AMOUNT_CN': TOTAL_AMOUNT_CN,
                'PROFIT_MARGIN': PROFIT_MARGIN,

                '打包总成本': 打包总成本,
                }]
            }
            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs),
            }
            if table_number == 'table_number_sum':
                return HttpResponse(json.dumps(context_all))
            elif table_number == 'table_number_detail':
                return HttpResponse(json.dumps(context))
            return render(request, 'five_miles/FiveMiles_All_orders_profitStatistics.html')
#5M 所有商品
def FiveMiles_all_products(request):
    user_app.change_info(request, 'FiveMiles_all_products')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >3:
        return render(request, '../../user_app/templates/404.html')
    try:
        exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
    except:
        exchange_rate = 6.3000
    try:
        打包成本 = models_PruAndLog.key_parameter.objects.filter(USER_ID=USER_ID).values('打包成本').first()['打包成本']
    except:
        打包成本 = 1.8

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            store_name = request.GET.get('store_name', '')  # 店铺名
            colect_pruduct = request.GET.get('colect_pruduct', '')  # 是否收藏
            SKU = request.GET.get('SKU', '')  # SKU  1

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

            if limit == '' and  page == '':
                store_name_users = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {
                            'store_name_users':list(store_name_users),
                            }
                return render(request, 'five_miles/FiveMiles_all_products.html',context0)

            if store_name == '':
                store_name = 'all'
            if colect_pruduct == '':
                colect_pruduct = '所有商品'

            if Sort_field == '':
                Sort_field = 'products_id'

            if Sort_order == 'desc' or Sort_order == '':
                Sort_order = '-'
            elif Sort_order == 'asc':
                Sort_order = ''
            else:
                Sort_order = '-'

            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            try:
                objs = models_five_miles.Products_5miles.objects.filter(USER_ID=USER_ID)
                if store_name != 'all':
                    objs = objs.filter(store_name=store_name)
                if colect_pruduct == '未收藏商品':
                    objs = objs.filter(user_collect=None)
                elif colect_pruduct == '收藏商品':
                    objs = objs.filter(user_collect='11')
                if SKU != '':
                    objs = objs.filter(goods_no__contains=SKU)
                count_all = objs.values('goods_no').count()
                objs = objs.values('store_name', 'products_id', 'goods_no', 'main_image_url', 'cat_name', \
                                   'original_sale_price', 'start_price', 'purchase_price', 'reserve_price', 'shipping_fee', \
                                   'cost_price', 'name', 'description', 'image_set', 'sku_set', 'user_collect' \
                                   ).order_by(Sort_order+Sort_field)[page_star:page_end]

                a = max(models_Tophatter.logistics_statistic.objects.filter(USER_ID=USER_ID).values_list('STAR_DATE'))[0]
                Its = models_Tophatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(STAR_DATE=a).values()  # 物流规则数据（匹配下单时间的物流规则）
                普货每克 = (float(Its[0]['美国_每克_普货']) * float(Its[0]['美国_折扣_普货']) * float(Its[0]['美国_销售比']) / 100) + \
                       (float(Its[0]['英国_每克_普货']) * float(Its[0]['英国_折扣_普货']) * float(Its[0]['英国_销售比']) / 100) + \
                       (float(Its[0]['加拿_每克_普货']) * float(Its[0]['加拿_折扣_普货']) * float(Its[0]['加拿_销售比']) / 100) + \
                       (float(Its[0]['澳大_每克_普货']) * float(Its[0]['澳大_折扣_普货']) * float(Its[0]['澳大_销售比']) / 100)
                普货挂号 = (float(Its[0]['美国_挂号_普货']) * float(Its[0]['美国_折扣_普货']) * float(Its[0]['美国_销售比']) / 100) + \
                       (float(Its[0]['英国_挂号_普货']) * float(Its[0]['英国_折扣_普货']) * float(Its[0]['英国_销售比']) / 100) + \
                       (float(Its[0]['加拿_挂号_普货']) * float(Its[0]['加拿_折扣_普货']) * float(Its[0]['加拿_销售比']) / 100) + \
                       (float(Its[0]['澳大_挂号_普货']) * float(Its[0]['澳大_折扣_普货']) * float(Its[0]['澳大_销售比']) / 100)

                带电每克 = (float(Its[0]['美国_每克_带电']) * float(Its[0]['美国_折扣_带电']) * float(Its[0]['美国_销售比']) / 100) + \
                       (float(Its[0]['英国_每克_带电']) * float(Its[0]['英国_折扣_带电']) * float(Its[0]['英国_销售比']) / 100) + \
                       (float(Its[0]['加拿_每克_带电']) * float(Its[0]['加拿_折扣_带电']) * float(Its[0]['加拿_销售比']) / 100) + \
                       (float(Its[0]['澳大_每克_带电']) * float(Its[0]['澳大_折扣_带电']) * float(Its[0]['澳大_销售比']) / 100)
                带电挂号 = (float(Its[0]['美国_挂号_带电']) * float(Its[0]['美国_折扣_带电']) * float(Its[0]['美国_销售比']) / 100) + \
                       (float(Its[0]['英国_挂号_带电']) * float(Its[0]['英国_折扣_带电']) * float(Its[0]['英国_销售比']) / 100) + \
                       (float(Its[0]['加拿_挂号_带电']) * float(Its[0]['加拿_折扣_带电']) * float(Its[0]['加拿_销售比']) / 100) + \
                       (float(Its[0]['澳大_挂号_带电']) * float(Its[0]['澳大_折扣_带电']) * float(Its[0]['澳大_销售比']) / 100)

                特货每克 = (float(Its[0]['美国_每克_特货']) * float(Its[0]['美国_折扣_特货']) * float(Its[0]['美国_销售比']) / 100) + \
                       (float(Its[0]['英国_每克_特货']) * float(Its[0]['英国_折扣_特货']) * float(Its[0]['英国_销售比']) / 100) + \
                       (float(Its[0]['加拿_每克_特货']) * float(Its[0]['加拿_折扣_特货']) * float(Its[0]['加拿_销售比']) / 100) + \
                       (float(Its[0]['澳大_每克_特货']) * float(Its[0]['澳大_折扣_特货']) * float(Its[0]['澳大_销售比']) / 100)
                特货挂号 = (float(Its[0]['美国_挂号_特货']) * float(Its[0]['美国_折扣_特货']) * float(Its[0]['美国_销售比']) / 100) + \
                       (float(Its[0]['英国_挂号_特货']) * float(Its[0]['英国_折扣_特货']) * float(Its[0]['英国_销售比']) / 100) + \
                       (float(Its[0]['加拿_挂号_特货']) * float(Its[0]['加拿_折扣_特货']) * float(Its[0]['加拿_销售比']) / 100) + \
                       (float(Its[0]['澳大_挂号_特货']) * float(Its[0]['澳大_折扣_特货']) * float(Its[0]['澳大_销售比']) / 100)

                for obj in objs:
                    obj['SKU_freight'] = 0
                    obj['imgs'] = []
                    ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['goods_no']).values('id').annotate(
                        SKU_price=Max('SKU_price')
                        , SKU_parts_price=Max('SKU_parts_price')
                        , SKU_weight=Max('SKU_weight')  # -------
                        , SKU_parts_weight=Max('SKU_parts_weight')  # -------
                        , SKU_variety=Max('SKU_variety')
                        , HAI_SKU_freight=Max('HAI_SKU_freight')  # -------
                        , Pingyou_min7_SKU_freight=Max('Pingyou_min7_SKU_freight')  # -------
                        , Pingyou_max7_SKU_freight=Max('Pingyou_max7_SKU_freight')  # -------
                        , top_colect=Max('top_colect'))  # -------
                    if ob:
                        obj['SKU_price'] = ob[0]['SKU_price']  # 单价
                        obj['SKU_parts_price'] = ob[0]['SKU_parts_price']  # 配件价
                        obj['SKU_weight'] = ob[0]['SKU_weight']  # 单重量
                        obj['SKU_parts_weight'] = ob[0]['SKU_parts_weight']  # 单配件重量
                        obj['SKU_variety'] = ob[0]['SKU_variety']  # 单种类
                        obj['HAI_SKU_freight'] = ob[0]['HAI_SKU_freight']  # 单价运费
                        obj['Pingyou_min7_SKU_freight'] = ob[0]['Pingyou_min7_SKU_freight']  # 小于7美元单价
                        obj['Pingyou_max7_SKU_freight'] = ob[0]['Pingyou_max7_SKU_freight']  # 大于7美元单价
                        obj['top_colect'] = ob[0]['top_colect']  #

                        if obj['SKU_price']:
                            obj['SKU_price'] = obj['SKU_price']
                        else:
                            obj['SKU_price'] = 0

                        if obj['SKU_parts_price']:
                            obj['SKU_parts_price'] = obj['SKU_parts_price']
                        else:
                            obj['SKU_parts_price'] = 0

                        if obj['SKU_weight']:
                            obj['SKU_weight'] = obj['SKU_weight']
                        else:
                            obj['SKU_weight'] = 0

                        if obj['SKU_parts_weight']:
                            obj['SKU_parts_weight'] = obj['SKU_parts_weight']
                        else:
                            obj['SKU_parts_weight'] = 0

                        if obj['SKU_variety']:
                            obj['SKU_variety'] = obj['SKU_variety']
                            if obj['SKU_variety'] == '海运':
                                obj['SKU_variety'] = '输入运费'
                        else:
                            obj['SKU_variety'] = ''

                        if obj['HAI_SKU_freight']:
                            obj['HAI_SKU_freight'] = obj['HAI_SKU_freight']
                        else:
                            obj['HAI_SKU_freight'] = 0

                        if obj['Pingyou_min7_SKU_freight']:
                            obj['Pingyou_min7_SKU_freight'] = obj['Pingyou_min7_SKU_freight']
                        else:
                            obj['Pingyou_min7_SKU_freight'] = 0

                        if obj['Pingyou_max7_SKU_freight']:
                            obj['Pingyou_max7_SKU_freight'] = obj['Pingyou_max7_SKU_freight']
                        else:
                            obj['Pingyou_max7_SKU_freight'] = 0

                        if obj['top_colect']:
                            obj['top_colect'] = obj['top_colect']
                        else:
                            obj['top_colect'] = '否'

                        if obj['SKU_variety'] == '普货':
                            if float(obj['SKU_weight']):
                                obj['SKU_freight'] = round(((float(obj['SKU_weight']) * 普货每克) + 普货挂号), 2)
                            else:
                                obj['SKU_freight'] = 0
                            obj['SKU_parts_freight'] = round(float(obj['SKU_parts_weight']) * 普货每克, 2)
                            obj['SKU_buy_one_freight'] = round(float(obj['SKU_weight']) * 普货每克, 2)
                        elif obj['SKU_variety'] == '带电':
                            if float(obj['SKU_weight']):
                                obj['SKU_freight'] = round(((float(obj['SKU_weight']) * 带电每克) + 带电挂号), 2)
                            else:
                                obj['SKU_freight'] = 0
                            obj['SKU_parts_freight'] = round(float(obj['SKU_parts_weight']) * 带电每克, 2)
                            obj['SKU_buy_one_freight'] = round(float(obj['SKU_weight']) * 带电每克, 2)

                        elif obj['SKU_variety'] == '特货':
                            if float(obj['SKU_weight']):
                                obj['SKU_freight'] = round(((float(obj['SKU_weight']) * 特货每克) + 特货挂号), 2)
                            else:
                                obj['SKU_freight'] = 0
                            obj['SKU_parts_freight'] = round(float(obj['SKU_parts_weight']) * 特货每克, 2)
                            obj['SKU_buy_one_freight'] = round(float(obj['SKU_weight']) * 特货每克, 2)
                        elif obj['SKU_variety'] == '海运' or obj['SKU_variety'] == '输入运费':
                            obj['SKU_freight'] = round(float(obj['HAI_SKU_freight']), 2)
                            obj['SKU_parts_freight'] = 0
                            obj['SKU_buy_one_freight'] = 0
                        elif obj['SKU_variety'] == '平邮':
                            if obj['revenue_avg'] < 7:
                                obj['SKU_freight'] = round(float(obj['Pingyou_min7_SKU_freight']), 2)
                            else:
                                obj['SKU_freight'] = round(float(obj['Pingyou_max7_SKU_freight']), 2)
                            obj['SKU_parts_freight'] = 0
                            obj['SKU_buy_one_freight'] = 0
                        else:
                            obj['SKU_freight'] = 0
                            obj['SKU_parts_freight'] = 0
                            obj['SKU_buy_one_freight'] = 0

                        if obj['SKU_freight'] and obj['SKU_price']:
                            obj['suggest_buynows_price'] = round(((((float(obj['SKU_price']) + float(obj['SKU_freight'])) * 1.4 / exchange_rate) + 1.3) / 0.821) / 0.95, 2)  # 建议一口价
                        else:
                            obj['suggest_buynows_price'] = ''
                    else:
                        obj['SKU_price'] = ''
                        obj['SKU_parts_price'] = ''
                        obj['SKU_weight'] = ''
                        obj['SKU_parts_weight'] = ''
                        obj['SKU_variety'] = ''
                        obj['HAI_SKU_freight'] = ''
                        obj['Pingyou_min7_SKU_freight'] = ''
                        obj['Pingyou_max7_SKU_freight'] = ''
                        obj['top_colect'] = '否'
                        obj['suggest_buynows_price'] = ''




                    for img in literal_eval(obj['image_set']):
                        obj['imgs'].append(img['image_url'])

            except Exception as e:
                print(e)

            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs),
            }
            return HttpResponse(json.dumps(context, cls=CJsonEncoder))
        return render(request, 'five_miles/FiveMiles_all_products.html')
#5M上传单个产品
def FiveMiles_products_update(request):
    user_app.change_info(request, 'uploading_one')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >3:
        return render(request, '../../user_app/templates/404.html')
    try:
        exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
    except:
        exchange_rate = 6.3000
    try:
        打包成本 = models_PruAndLog.key_parameter.objects.filter(USER_ID=USER_ID).values('打包成本').first()['打包成本']
    except:
        打包成本 = 1.8

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            Top主SKU = request.GET.get('Top主SKU', '')
            store_name = request.GET.get('store_name', '')
            FIG = request.GET.get('FIG', '0')

            # 获取产品网页数据
            if FIG == '0' and  Top主SKU != '' and  store_name !='':
                store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]
                try:
                    subm = requests.get('https://tophatter.com/merchant_api/v1/products/retrieve.json?access_token=' + store_APIToken + '&identifier=' + Top主SKU,
                                        timeout=100)  # 2f9a6837ddb548932118fb57b625f3b3
                    aa = subm.text
                    reponse_dict = json.loads(aa)

                    # 2 保存到数据库
                    identifier = reponse_dict.get('identifier')  # SKU
                    primary_image = reponse_dict.get('primary_image')  # 主图
                    buy_now_price = reponse_dict.get('buy_now_price')  # 一口价
                    buy_now_price = str(buy_now_price)
                    buy_now_price = re.sub('\.0', '', buy_now_price)
                    buy_now_price = re.sub('None', '', buy_now_price)

                    cost_basis = reponse_dict.get('cost_basis')  # 目标价
                    cost_basis = str(cost_basis)
                    cost_basis = re.sub('\.0', '', cost_basis)
                    cost_basis = re.sub('None', '', cost_basis)

                    retail_price = reponse_dict.get('retail_price')  # 零售价
                    retail_price = str(retail_price)
                    retail_price = re.sub('\.0', '', retail_price)
                    retail_price = re.sub('None', '', retail_price)

                    reserve_price = reponse_dict.get('reserve_price')  # 底价
                    reserve_price = str(reserve_price)
                    reserve_price = re.sub('\.0', '', reserve_price)
                    reserve_price = re.sub('[None]', '', reserve_price)

                    scheduling_fee_bid = reponse_dict.get('scheduling_fee_bid')  # SFB
                    scheduling_fee_bid = str(scheduling_fee_bid)
                    scheduling_fee_bid = re.sub('None', '', scheduling_fee_bid)

                    shipping_price = reponse_dict.get('shipping_price')  # 运费
                    shipping_price = str(shipping_price)
                    shipping_price = re.sub('\.0', '', shipping_price)
                    shipping_price = re.sub('None', '', shipping_price)

                    campaign_name = reponse_dict.get('campaign_name')  # camp 名字
                    campaign_name = str(campaign_name)
                    campaign_name = re.sub('None', '', campaign_name)

                    accessory_price = ''
                    accessory_description = ''
                    upsells = reponse_dict.get('upsells')  # 运费
                    if upsells != '[]':
                        upsells = literal_eval(str(upsells))
                        if len(upsells) == 1:
                            accessory_price = str(upsells[0]['amount'])  # 运费价格
                            accessory_price = re.sub('\.0', '', accessory_price)
                            accessory_price = re.sub('None', '', accessory_price)
                            accessory_description = upsells[0]['description']  # 运费描述
                        elif len(upsells) == 2:
                            accessory_price = str(upsells[1]['amount'])  # 运费价格
                            accessory_price = re.sub('\.0', '', accessory_price)
                            accessory_price = re.sub('None', '', accessory_price)
                            accessory_description = upsells[1]['description']  # 运费描述
                except Exception as e:
                    print(e)

                context = {
                    'identifier': identifier,
                    'primary_image': primary_image,
                    'buy_now_price': buy_now_price,
                    'cost_basis': cost_basis,
                    'retail_price': retail_price,
                    'reserve_price': reserve_price,

                    'scheduling_fee_bid': scheduling_fee_bid,
                    'shipping_price': shipping_price,
                    'campaign_name': campaign_name,
                    'accessory_price': accessory_price,
                    'accessory_description': accessory_description,
                    'store_name': store_name,
                }
                return render(request, 'Tophatter/Top_products_update.html', context)

            if FIG == 'FIG':
                identifier = request.GET.get('identifier', '')
                store_name = request.GET.get('store_name', '')

                buy_now_price = request.GET.get('buy_now_price', '')
                cost_basis = request.GET.get('cost_basis', '')
                retail_price = request.GET.get('retail_price', '')
                reserve_price = request.GET.get('reserve_price', '')
                scheduling_fee_bid = request.GET.get('scheduling_fee_bid', '')
                shipping_price = request.GET.get('shipping_price', '')
                配件价格 = request.GET.get('配件价格', '')
                配件描述1 = request.GET.get('配件描述1', '')
                配件描述2 = request.GET.get('配件描述2', '')
                CAMPAIGN_1 = request.GET.get('CAMPAIGN_1', '')
                CAMPAIGN_2 = request.GET.get('CAMPAIGN_2', '')


                # 上传数据到店铺
                try:
                    errmsg_1 = ''
                    errmsg_2 = ''
                    extra_images = ''

                    store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]
                    data_variations = {}
                    data_msg = {'msg_1': '无', 'msg_2': '无', }

                    # 店铺模板
                    identifier = identifier  # Product Unique ID

                    if shipping_price and shipping_price != '0':
                        shipping_price = int(shipping_price)  # Shipping Price
                    else:
                        shipping_price = None

                    if buy_now_price and buy_now_price != '0':
                        buy_now_price = int(buy_now_price)  # Buy Now Price
                    else:
                        buy_now_price = None

                    if cost_basis and cost_basis != '0':
                        cost_basis = int(cost_basis)  # Target Price
                    else:
                        cost_basis = None  # Target Price

                    if retail_price and retail_price != '0':
                        retail_price = int(retail_price)  # Retail Price
                    else:
                        retail_price = ''  # Retail Price

                    if reserve_price and reserve_price != '0':
                        reserve_price = int(float(reserve_price))  # Reserve Price
                    else:
                        reserve_price = ''

                    if scheduling_fee_bid and scheduling_fee_bid != '0':
                        scheduling_fee_bid = float(scheduling_fee_bid)  # Scheduling Fee Bid
                    else:
                        scheduling_fee_bid = 0

                    if shipping_price and shipping_price != '0':
                        shipping_price = int(shipping_price)  # Shipping Price
                    else:
                        shipping_price = 0

                    if 配件价格 and 配件价格 != '0':
                        accessory_price = int(配件价格)  # Accessory Price
                    else:
                        accessory_price = None
                    accessory_description = 配件描述1 + 配件描述2  # Accessory Description

                    campaign_name = CAMPAIGN_1 + CAMPAIGN_2  # campaign_name
                    if campaign_name != '':
                        campaign_name = campaign_name  # Accessory Price
                    else:
                        campaign_name = None

                    data = {
                        'access_token': store_APIToken,  # '2f9a6837ddb548932118fb57b625f3b3',  # 实验账号
                        'identifier': identifier,
                        'cost_basis': cost_basis,
                        'buy_now_price': buy_now_price,
                        'retail_price': retail_price,
                        'reserve_price': reserve_price,
                        'scheduling_fee_bid': scheduling_fee_bid,
                        'shipping_price': shipping_price,

                        'accessory_price': accessory_price,
                        'accessory_description': accessory_description,
                        'campaign_name': campaign_name
                    }

                    # print('开始更新')
                    try:
                        subm = requests.post('https://tophatter.com/merchant_api/v1/products/update.json', data=data, timeout=30)
                        if subm.status_code == 200:
                            # 获取更新完的产品信息
                            try:
                                subm = requests.get(
                                    'https://tophatter.com/merchant_api/v1/products/retrieve.json?access_token=' + store_APIToken + '&identifier=' + identifier,
                                    timeout=100)  # 2f9a6837ddb548932118fb57b625f3b3
                                aa = subm.text
                                reponse_dict = json.loads(aa)
                                # 2 保存到数据库
                                identifier = reponse_dict.get('identifier')
                                internal_id = reponse_dict.get('internal_id')
                                category = reponse_dict.get('category')
                                title = reponse_dict.get('title')
                                description = reponse_dict.get('description')
                                condition = reponse_dict.get('condition')
                                brand = reponse_dict.get('brand')
                                material = reponse_dict.get('material')
                                available_quantity = reponse_dict.get('available_quantity')
                                variations = reponse_dict.get('variations')

                                retail_price = reponse_dict.get('retail_price')
                                cost_basis = reponse_dict.get('cost_basis')
                                minimum_bid_amount = reponse_dict.get('minimum_bid_amount')
                                max_daily_schedules = reponse_dict.get('max_daily_schedules')
                                scheduling_fee_bid = reponse_dict.get('scheduling_fee_bid')
                                reserve_price = reponse_dict.get('reserve_price')
                                shipping_price = reponse_dict.get('shipping_price')
                                shipping_origin = reponse_dict.get('shipping_origin')
                                fulfillment_partner = reponse_dict.get('fulfillment_partner')
                                weight = reponse_dict.get('weight')
                                days_to_fulfill = reponse_dict.get('days_to_fulfill')
                                days_to_deliver = reponse_dict.get('days_to_deliver')

                                expedited_shipping_price = reponse_dict.get('expedited_shipping_price')
                                expedited_days_to_deliver = reponse_dict.get('expedited_days_to_deliver')
                                buy_one_get_one_price = reponse_dict.get('buy_one_get_one_price')
                                upsells = reponse_dict.get('upsells')
                                primary_image = reponse_dict.get('primary_image')
                                extra_images = reponse_dict.get('extra_images')
                                all_images = reponse_dict.get('all_images')
                                ratings_count = reponse_dict.get('ratings_count')
                                ratings_average = reponse_dict.get('ratings_average')
                                campaign_name = reponse_dict.get('campaign_name')
                                buy_now_price = reponse_dict.get('buy_now_price')

                                created_at = reponse_dict.get('created_at')
                                if created_at:
                                    created_at = reponse_dict.get('created_at')[0:18]
                                else:
                                    created_at = None

                                updated_at = reponse_dict.get('updated_at')
                                if updated_at:
                                    updated_at = reponse_dict.get('updated_at')[0:18]
                                else:
                                    updated_at = None

                                disabled_at = reponse_dict.get('disabled_at')
                                if disabled_at:
                                    disabled_at = reponse_dict.get('disabled_at')[0:18]
                                else:
                                    disabled_at = None

                                idenx = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=identifier)
                                if idenx:
                                    try:
                                        models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=identifier) \
                                            .update(store_name=store_name,
                                                    identifier=identifier,
                                                    internal_id=internal_id,
                                                    category=category,
                                                    title=title,
                                                    description=description,
                                                    condition=condition,
                                                    brand=brand,
                                                    material=material,
                                                    available_quantity=available_quantity,
                                                    variations=variations,

                                                    retail_price=retail_price,
                                                    cost_basis=cost_basis,
                                                    minimum_bid_amount=minimum_bid_amount,
                                                    max_daily_schedules=max_daily_schedules,
                                                    scheduling_fee_bid=scheduling_fee_bid,
                                                    reserve_price=reserve_price,
                                                    shipping_price=shipping_price,
                                                    shipping_origin=shipping_origin,
                                                    fulfillment_partner=fulfillment_partner,
                                                    weight=weight,
                                                    days_to_fulfill=days_to_fulfill,
                                                    days_to_deliver=days_to_deliver,

                                                    expedited_shipping_price=expedited_shipping_price,
                                                    expedited_days_to_deliver=expedited_days_to_deliver,
                                                    buy_one_get_one_price=buy_one_get_one_price,
                                                    upsells=upsells,
                                                    primary_image=primary_image,
                                                    extra_images=extra_images,
                                                    all_images=all_images,
                                                    ratings_count=ratings_count,
                                                    ratings_average=ratings_average,
                                                    campaign_name=campaign_name,
                                                    buy_now_price=buy_now_price,

                                                    created_at=created_at,
                                                    updated_at=updated_at,
                                                    disabled_at=disabled_at
                                                    )
                                        # print(store_name + '商品数据保存 success')
                                    except Exception as e:
                                        print(e)
                                        print('商品数据替换  faile')
                                else:
                                    try:
                                        twz = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).create(
                                            store_name=store_name,
                                            identifier=identifier,
                                            internal_id=internal_id,
                                            category=category,
                                            title=title,
                                            description=description,
                                            condition=condition,
                                            brand=brand,
                                            material=material,
                                            available_quantity=available_quantity,
                                            variations=variations,

                                            retail_price=retail_price,
                                            cost_basis=cost_basis,
                                            minimum_bid_amount=minimum_bid_amount,
                                            max_daily_schedules=max_daily_schedules,
                                            scheduling_fee_bid=scheduling_fee_bid,
                                            reserve_price=reserve_price,
                                            shipping_price=shipping_price,
                                            shipping_origin=shipping_origin,
                                            fulfillment_partner=fulfillment_partner,
                                            weight=weight,
                                            days_to_fulfill=days_to_fulfill,
                                            days_to_deliver=days_to_deliver,

                                            expedited_shipping_price=expedited_shipping_price,
                                            expedited_days_to_deliver=expedited_days_to_deliver,
                                            buy_one_get_one_price=buy_one_get_one_price,
                                            upsells=upsells,
                                            primary_image=primary_image,
                                            extra_images=extra_images,
                                            all_images=all_images,
                                            ratings_count=ratings_count,
                                            ratings_average=ratings_average,
                                            campaign_name=campaign_name,
                                            buy_now_price=buy_now_price,

                                            created_at=created_at,
                                            updated_at=updated_at,
                                            disabled_at=disabled_at
                                        )
                                        twz.save()
                                        # print(store_name + '商品数据保存 success')
                                    except Exception as e:
                                        print(e)
                                        print('商品数据保存  faile')
                            except Exception as e:
                                print(e)
                                print('not this Pruducts 数据')
                                return False

                            errmsg_1 = errmsg_1 + identifier
                        else:
                            errmsg_2 = errmsg_2 + identifier
                    except Exception as e:
                        print(e)
                        errmsg_2 = errmsg_2 + identifier
                    data_msg['msg_1'] = errmsg_1
                    data_msg['msg_2'] = errmsg_2
                    return HttpResponse(json.dumps(data_msg))
                except Exception as e:
                    data_msg_e = {'msg_e': str(e)}
                    print(data_msg_e)
                    return HttpResponse(json.dumps(data_msg_e))

            return render(request, 'Tophatter/Top_products_update.html')
# 5M店铺资金
def FiveMiles_founds(request):
    user_app.change_info(request, 'FiveMiles_founds')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >3:
        return render(request, '../../user_app/templates/404.html')
    try:
        exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
    except:
        exchange_rate = 6.3000

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            cols = request.GET.get('cols', '')  # cols
            if limit == '' and  page == '' and cols == '':
                store_name_users = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {
                            'store_name_users':list(store_name_users),
                            }
                return render(request, 'five_miles/FiveMiles_founds.html',context0)
            if cols == 'cols':
                store_name_users = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).values('store_name')
                i = 0
                for store_name_user in store_name_users:
                    i = i+1
                    store_name_user['field'] = str(i)

                context1 = { 'store_name_users':list(store_name_users), }
                return HttpResponse(json.dumps(context1))

            count_all = 0
            objs = models_five_miles.funds_5miles_date.objects.filter(USER_ID=USER_ID).values('Time_Date').annotate(store_name_count=Count('店铺名')).order_by('-Time_Date')
            count_all = objs.count()
            store_name_users = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).values('store_name')
            for obj in objs:
                i = 0
                obj['可提']=0
                obj['待确'] = 0
                obj['提现'] = 0
                obj['SUM_UP_PE'] = 0
                obj['SUM_UP_PE_REN'] = 0
                obj['SUM_UP_PE_92'] = 0
                for store_name_user in store_name_users:
                    i = i + 1
                    可提现 =  0
                    待确认  =  0
                    提现中 = 0
                    sum_up_pe = 0
                    oa = models_five_miles.funds_5miles_date.objects.filter(USER_ID=USER_ID).filter(店铺名=store_name_user['store_name']).filter(Time_Date=obj['Time_Date'])\
                         .values('店铺名','可提现','待确认','提现中','Time_Date','save_time')
                    if oa:
                        if oa[0]['可提现'] or  oa[0]['待确认'] or  oa[0]['提现中']:
                            可提现 = float(oa[0]['可提现'])
                            待确认 = float(oa[0]['待确认'])
                            提现中 = float(oa[0]['提现中'])
                            sum_up_pe = round(可提现 + 待确认+ 提现中,2)
                            obj[str(i)] = oa[0]['可提现'] + ' / ' +  oa[0]['待确认']  +' / '+  oa[0]['提现中']  +' / '+ str(sum_up_pe)
                        else:
                            obj[str(i)] = '未获取'
                    else:
                        obj[str(i)] = '未获取'
                    obj['可提'] += 可提现
                    obj['待确'] += 待确认
                    obj['提现'] += 提现中
                    obj['SUM_UP_PE'] += sum_up_pe
                obj['SUM_UP_PE_REN'] = obj['SUM_UP_PE'] * exchange_rate
                obj['SUM_UP_PE_92'] = obj['SUM_UP_PE_REN']*0.92
                obj['可提'] = round(obj['可提'],2)
                obj['待确'] = round(obj['待确'],2)
                obj['提现'] = round(obj['提现'], 2)
                obj['SUM_UP_PE'] = round(obj['SUM_UP_PE'], 2)
                obj['SUM_UP_PE_REN'] = round(obj['SUM_UP_PE_REN'], 2)
                obj['SUM_UP_PE_92'] = round(obj['SUM_UP_PE_92'], 2)
            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs),
            }
            return HttpResponse(json.dumps(context, cls=CJsonEncoder))
#5M店铺信息
def FiveMiles_store_msg(request):
    user_app.change_info(request, 'FiveMiles_seller')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID','PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >3:
        return render(request, '../../user_app/templates/404.html')
    try:
        exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
    except:
        exchange_rate = 6.3000

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            caozuo_status = request.GET.get('caozuo_status', '')
            store_name_edit = request.GET.get('store_name_edit', '')
            field_edit = request.GET.get('field_edit', '')
            value_edit = request.GET.get('value_edit', '')
            store_name_add = request.GET.get('store_name_add', '')
            store_name_del = request.GET.get('store_name_del', '')
            #编辑已有数据
            if caozuo_status== 'edit':
                try:
                    if field_edit == 'store_APIToken':
                        models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).update(store_APIToken=value_edit,updated_time = datetime.datetime.now())
                    # elif field_edit == 'seller_id':
                    #     models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(seller_id=value_edit,updated_time = datetime.datetime.now())
                    # elif field_edit == 'IP_address':
                    #     models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(IP_address=value_edit,updated_time = datetime.datetime.now())
                    elif field_edit == 'store_cookie':
                        models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(store_cookie=value_edit,updated_time = datetime.datetime.now())
                    elif field_edit == 'beizhu':
                        models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(beizhu=value_edit,updated_time = datetime.datetime.now())
                    data_msg_e = {'msg_e': '替换成功'}
                    return HttpResponse(json.dumps(data_msg_e))
                except:
                    data_msg_e = {'msg_e': '替换失败'}
                    return HttpResponse(json.dumps(data_msg_e))
            #增加新数据
            if caozuo_status == 'add':
                try:
                    if store_name_add :
                        index = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_add)
                        if index:
                            data_msg_e = {'msg_e': '该账号名已存在'}
                            return HttpResponse(json.dumps(data_msg_e))
                        else:
                            models_five_miles.APIAccessToken_5miles.objects.create(USER_ID=USER_ID,store_name=store_name_add,created_time=datetime.datetime.now(),updated_time = datetime.datetime.now()).save()
                            data_msg_e = {'msg_e': '创建成功'}
                            return HttpResponse(json.dumps(data_msg_e))
                    data_msg_e = {'msg_e': '请输入店铺名称！'}
                    return HttpResponse(json.dumps(data_msg_e))
                except:
                    data_msg_e = {'msg_e': '创建失败'}
                    return HttpResponse(json.dumps(data_msg_e))
            #增加新数据
            if caozuo_status == 'delete':
                try:
                    if store_name_del :
                        models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_del).delete()
                        data_msg_e = {'msg_e': '删除成功'}
                        return HttpResponse(json.dumps(data_msg_e))
                except:
                    data_msg_e = {'msg_e': '删除失败'}
                    return HttpResponse(json.dumps(data_msg_e))

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式
            if Sort_field == '':
                Sort_field = 'created_time'

            if Sort_order == 'desc' or Sort_order == '':
                Sort_order = '-'
            elif Sort_order == 'asc':
                Sort_order = ''
            else:
                Sort_order = '-'

            if limit == '' and page == '':
                return render(request, 'five_miles/FiveMiles_store_msg.html')
            try:
                page_star = int(limit) * (int(page) - 1)
                page_end = page_star + int(limit)

                objs = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).values()
                count_all = objs.count()
                objs = objs.order_by(Sort_order+Sort_field)[page_star:page_end]  # 已备注的卖家

            except Exception as e:
                print(e)

            context = {
                'code': 0,
                'msg': '',
                'count': count_all,
                'data': list(objs),
            }
            if page:
                return HttpResponse(json.dumps(context, cls=CJsonEncoder))
            return render(request, 'five_miles/FiveMiles_store_msg.html')
#日期转换成JOSN的解码函数
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

