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

# Create your views here.

#所有订单利润统计
def All_orders_profitStatistics(request):
    user_app.change_info(request, 'All_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            time_local_load_orders = request.GET.get('time_local_load_orders', '')  # 导出订单时间段
            if time_local_load_orders:
                user_app.change_info(request, 'All_orders_profitStatistics')
                if time_local_load_orders == '一星期':
                    start_time_0 = (datetime.datetime.now() - datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
                    end_time_0 = datetime.datetime.now().date().strftime('%Y-%m-%d')
                if time_local_load_orders == '一个月':
                    start_time_0 = (datetime.datetime.now() - datetime.timedelta(days=30)).date().strftime('%Y-%m-%d')
                    end_time_0 = datetime.datetime.now().date().strftime('%Y-%m-%d')
                if time_local_load_orders == '三个月':
                    start_time_0 = (datetime.datetime.now() - datetime.timedelta(days=90)).date().strftime('%Y-%m-%d')
                    end_time_0 = datetime.datetime.now().date().strftime('%Y-%m-%d')
                if time_local_load_orders == '6个月':
                    start_time_0 = (datetime.datetime.now() - datetime.timedelta(days=180)).date().strftime('%Y-%m-%d')
                    end_time_0 = datetime.datetime.now().date().strftime('%Y-%m-%d')
                if time_local_load_orders == '所有':
                    start_time_0 = (datetime.datetime.now() - datetime.timedelta(days=600)).date().strftime('%Y-%m-%d')
                    end_time_0 = datetime.datetime.now().date().strftime('%Y-%m-%d')
                try:
                    objs_load_orders = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(data_time_created_at__gte=start_time_0).filter(
                        data_time_created_at__lte=end_time_0).values_list(
                        'store_name', 'order_id', 'status', 'status_paid', 'status_shipped', 'status_refunded', 'related_order_ids', 'service_type', 'carrier',
                        'tracking_number', 'fulfillment_partner', 'product_name', 'product_identifier', 'product_internal_id',
                        'variation_identifier', 'variation_internal_id', 'customer_id', 'customer_name', 'address1', 'address2',
                        'city', 'state', 'postal_code', 'country', 'available_refunds_buyer_fee', 'refund_amount', 'disbursement_amount', \
                        'seller_fees_amount', 'seller_fees_type_sfb', 'seller_fees_type_buy_nows', 'seller_fees_type_buy_nows_price', \
                        'seller_fees_amount_sfb', 'seller_fees_type_com', 'seller_fees_amount_com', 'seller_fees_type_pro', 'seller_fees_amount_pro', \
                        'upsells_type_description1', 'upsells_amount1', 'upsells_description1', 'upsells_type_description2', 'upsells_amount2', 'upsells_description2', \
                        'refunded_at', 'paid_at', 'created_at', 'updated_at', 'canceled_at', 'refunded_at_own', 'refunded_at_buyer', 'refund_amount_own', 'refund_amount_buyer', \
                        'canceled_refund_amount', 'canceled_disbursement_amount', 'canceled_seller_fees_amount', 'save_time', 'product_quantity', 'data_time_created_at', \
                        'data_time_paid_at', 'hours_time_created_at', 'SKU_price', 'SKU_parts_price', 'SKU_freight', 'SKU_parts_freight', 'SKU_buy_one_price',
                        'SKU_buy_one_freight', 'dxm_总', 'dxm_未查到', 'dxm_已签收', 'dxm_有异常', 'dxm_运输过久', 'dxm_运输中').order_by('-created_at')
                    load_orders = [(
                        'store_name', 'order_id', 'status', 'status_paid', 'status_shipped', 'status_refunded', 'related_order_ids', 'service_type', 'carrier',
                        'tracking_number', 'fulfillment_partner', 'product_name', 'product_identifier', 'product_internal_id',
                        'variation_identifier', 'variation_internal_id', 'customer_id', 'customer_name', 'address1', 'address2',
                        'city', 'state', 'postal_code', 'country', 'available_refunds_buyer_fee', 'refund_amount', 'disbursement_amount', \
                        'seller_fees_amount', 'seller_fees_type_sfb', 'seller_fees_type_buy_nows', 'seller_fees_type_buy_nows_price', \
                        'seller_fees_amount_sfb', 'seller_fees_type_com', 'seller_fees_amount_com', 'seller_fees_type_pro', 'seller_fees_amount_pro', \
                        'upsells_type_description1', 'upsells_amount1', 'upsells_description1', 'upsells_type_description2', 'upsells_amount2', 'upsells_description2', \
                        'refunded_at', 'paid_at', 'created_at', 'updated_at', 'canceled_at', 'refunded_at_own', 'refunded_at_buyer', 'refund_amount_own', 'refund_amount_buyer', \
                        'canceled_refund_amount', 'canceled_disbursement_amount', 'canceled_seller_fees_amount', 'save_time', 'product_quantity', 'data_time_created_at', \
                        'data_time_paid_at', 'hours_time_created_at', 'SKU_price', 'SKU_parts_price', 'SKU_freight', 'SKU_parts_freight', 'SKU_buy_one_price',
                        'SKU_buy_one_freight', 'dxm_总', 'dxm_未查到', 'dxm_已签收', 'dxm_有异常', 'dxm_运输过久', 'dxm_运输中', '主图', '标准ID')]
                    for obj_load in objs_load_orders:
                        oa = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=obj_load[12]).values('primary_image', 'standard_product_id')
                        主图_load = None
                        标准ID_load = None
                        if oa:
                            主图_load = oa[0]['primary_image']  # 主图
                            标准ID_load = oa[0]['standard_product_id']  # 标准ID
                        tuple1 = (主图_load, 标准ID_load)
                        tuple12 = obj_load + tuple1
                        load_orders.append(tuple12)
                    students = load_orders
                    with open("C:\\shengkongshuju\\static\\user_files_directory\\导出平台数据\\所有店铺_商品详情.csv", 'w', encoding='utf-8', newline='') as fp:
                    # with open("F:\\E_commerce\\static\\Detailed_orders_files\\订单详情.csv", 'w', encoding='utf-8', newline='') as fp: #本地调试地址
                        writer = csv.writer(fp, dialect='excel')
                        # writer.writerow(headers)  # 写入一行
                        writer.writerows(students)  # 写入多行
                except Exception as e:
                    Detailed_orders = {'Detailed_orders': '0', 'msge': '失败'}
                    return HttpResponse(json.dumps(Detailed_orders))

                Detailed_orders = {'Detailed_orders': '1', 'msge': '成功'}
                return HttpResponse(json.dumps(Detailed_orders))

            # 编辑产品信息
            SKU_name = request.GET.get('SKU_name', '')
            if SKU_name != '':
                user_app.change_info(request, '编辑产品信息')
                SKU_price = request.GET.get('SKU_price', '')
                SKU_weight = request.GET.get('SKU_weight', '')
                SKU_parts_price = request.GET.get('SKU_parts_price', '')
                SKU_parts_weight = request.GET.get('SKU_parts_weight', '')
                SKU_variety = request.GET.get('SKU_variety', '')
                HAI_SKU_freight = request.GET.get('HAI_SKU_freight', '')
                Pingyou_min7_SKU_freight = request.GET.get('Pingyou_min7_SKU_freight', '')
                Pingyou_max7_SKU_freight = request.GET.get('Pingyou_max7_SKU_freight', '')
                top_colect = request.GET.get('top_colect', '')

                change_standard_product = request.GET.get('change_standard_product', '')
                standard_product_id_edit = request.GET.get('standard_product_id_edit', '')

                if top_colect != '':
                    models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=SKU_name).update(user_collect=top_colect,colloct_at=datetime.datetime.now())
                    models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=SKU_name).update(top_colect=top_colect, data_date=datetime.datetime.now())

                index = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=SKU_name)
                if index:
                    if change_standard_product == '是':
                        if standard_product_id_edit:
                            index1 = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(standard_product_id=standard_product_id_edit)
                            if index1:
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(standard_product_id=standard_product_id_edit).update(SKU_price=SKU_price,
                                                                                                          SKU_weight=SKU_weight,
                                                                                                          SKU_parts_price=SKU_parts_price,
                                                                                                          SKU_parts_weight=SKU_parts_weight,
                                                                                                          SKU_variety=SKU_variety,
                                                                                                          HAI_SKU_freight=HAI_SKU_freight,
                                                                                                          Pingyou_min7_SKU_freight = Pingyou_min7_SKU_freight,
                                                                                                          Pingyou_max7_SKU_freight = Pingyou_max7_SKU_freight,
                                                                                                          data_date=datetime.datetime.now())
                                data_msg_e = {'msg_e': '替换成功(标准ID)'}
                                return HttpResponse(json.dumps(data_msg_e))
                            else:
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=SKU_name).update(standard_product_id=standard_product_id_edit)
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(standard_product_id=standard_product_id_edit).update(SKU_price=SKU_price,
                                                                                                                                   SKU_weight=SKU_weight,
                                                                                                                                   SKU_parts_price=SKU_parts_price,
                                                                                                                                   SKU_parts_weight=SKU_parts_weight,
                                                                                                                                   SKU_variety=SKU_variety,
                                                                                                                                   HAI_SKU_freight=HAI_SKU_freight,
                                                                                                                                   Pingyou_min7_SKU_freight=Pingyou_min7_SKU_freight,
                                                                                                                                   Pingyou_max7_SKU_freight=Pingyou_max7_SKU_freight,
                                                                                                                                   data_date=datetime.datetime.now())
                                data_msg_e = {'msg_e': '替换成功(标准ID)'}
                                return HttpResponse(json.dumps(data_msg_e))
                        else:
                            data_msg_e = {'msg_e': '失败! 该SKU无标准ID'}
                            return HttpResponse(json.dumps(data_msg_e))
                    else:
                        models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=SKU_name).update(SKU_price=SKU_price,
                                                                                                  SKU_weight=SKU_weight,
                                                                                                  SKU_parts_price=SKU_parts_price,
                                                                                                  SKU_parts_weight=SKU_parts_weight,
                                                                                                  SKU_variety=SKU_variety,
                                                                                                  HAI_SKU_freight=HAI_SKU_freight,
                                                                                                  Pingyou_min7_SKU_freight = Pingyou_min7_SKU_freight,
                                                                                                  Pingyou_max7_SKU_freight = Pingyou_max7_SKU_freight,
                                                                                                  data_date=datetime.datetime.now())
                        data_msg_e = {'msg_e': '替换成功(SKU)'}
                        return HttpResponse(json.dumps(data_msg_e))
                else:
                    models_Tophatter.Price_Freight.objects.create(identifier=SKU_name,
                                                                  USER_ID=USER_ID,
                                                                  standard_product_id=standard_product_id_edit,
                                                                  SKU_price=SKU_price,
                                                                  SKU_weight=SKU_weight,
                                                                  SKU_parts_price=SKU_parts_price,
                                                                  SKU_parts_weight=SKU_parts_weight,
                                                                  SKU_variety=SKU_variety,
                                                                  HAI_SKU_freight=HAI_SKU_freight,
                                                                  Pingyou_min7_SKU_freight=Pingyou_min7_SKU_freight,
                                                                  Pingyou_max7_SKU_freight=Pingyou_max7_SKU_freight,
                                                                  data_date=datetime.datetime.now()).save()
                    data_msg_e = {'msg_e': '保存成功'}
                    return HttpResponse(json.dumps(data_msg_e))

            store_name = request.GET.get('store_name', '')  # 店铺名
            start_time = request.GET.get('start_time', '')  # 统计时间
            end_time = request.GET.get('end_time', '')  # 统计时间
            time_local = request.GET.get('time_local', '')  # 统计时间
            product_identifier = request.GET.get('product_identifier', '')  # 商品名称
            product_type = request.GET.get('product_type', '')  # 订单类型  1
            related_order_ids = request.GET.get('related_order_ids', '')
            service_type = request.GET.get('service_type', '')
            input_order_type = request.GET.get('input_order_type', '')
            承运商 = request.GET.get('承运商', '')

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

            table_number = request.GET.get('table_number', '')  # 表格序号

            if limit == '' and  page == '' and  table_number == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {'store_name_users':list(store_name_users)}
                return render(request, 'Tophatter/All_orders_profitStatistics.html',context0)

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

            if product_type == '':
                product_type = '全部订单'

            if related_order_ids == '':
                related_order_ids = '全部订单'

            if service_type == '':
                service_type = '全部订单'
            if service_type == '全程追踪':
                service_type = 'full_tracking'
            if service_type == '部分追踪':
                service_type = 'partial_tracking'
            if service_type == '没有最后一英里追踪':
                service_type = 'no_last_mile_tracking'

            if input_order_type == '':
                input_order_type = '全部订单'

            if 承运商 == '':
                承运商 = '全部订单'

            if Sort_field == '':
                Sort_field = 'paid_at'

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
            objs1 = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time).filter(canceled_at=None)
            if store_name != 'all':
                objs1 = objs1.filter(store_name=store_name)

            if product_type == '一口价':
                objs1 = objs1.filter(~Q(seller_fees_type_buy_nows=None))
            if product_type == '竞拍价':
                objs1 = objs1.filter(seller_fees_type_buy_nows=None)

            if related_order_ids == '非关系订单':
                objs1 = objs1.filter(Q(related_order_ids=None) & Q(related_order_ids='[]'))
            if related_order_ids == '关系订单':
                objs1 = objs1.filter(~Q(related_order_ids=None) & ~Q(related_order_ids='[]'))

            if service_type != '全部订单':
                objs1 = objs1.filter(service_type=service_type)

            if input_order_type == '有状态订单':
                objs1 = objs1.filter(~Q(ht_物流状态=None))
            elif input_order_type == 'Delivered':
                objs1 = objs1.filter(ht_物流状态='Delivered')
            elif input_order_type == 'Exception':
                objs1 = objs1.filter(ht_物流状态='Exception')
            elif input_order_type == 'InfoReceived':
                objs1 = objs1.filter(ht_物流状态='InfoReceived')
            elif input_order_type == 'InTransit':
                objs1 = objs1.filter(ht_物流状态='InTransit')
            elif input_order_type == 'OutForDelivery':
                objs1 = objs1.filter(ht_物流状态='OutForDelivery')

            if 承运商 == '有承运商订单':
                objs1 = objs1.filter(~Q(carrier=None))
            elif 承运商 == '无承运商订单':
                objs1 = objs1.filter(carrier=None)
            elif 承运商 != '全部订单' and 承运商 != '有承运商订单' and 承运商 != '无承运商订单':
                objs1 = objs1.filter(carrier=承运商)

            if product_identifier != '':
                objs1 = objs1.filter(product_identifier__contains=product_identifier)

            if table_number == 'table_number_detail':
                count_all = objs1.values('product_internal_id').annotate(paid_at=Count('paid_at')).count()
                objs1 = objs1.values('product_internal_id').annotate(created_at=Count('created_at')
                                                                     , status_paid=Count('status_paid')
                                                                     , status_shipped=Count('status_shipped')
                                                                     , status_refunded=Count('status_refunded')
                                                                     , refunded_at_own=Count('refunded_at_own')
                                                                     , refunded_at_buyer=Count('refunded_at_buyer')
                                                                     , refund_amount_own=Sum('refund_amount_own')
                                                                     , refund_amount=Sum('refund_amount')
                                                                     , canceled_at=Count('canceled_at')
                                                                     , refunded_at=Count('refunded_at')
                                                                     , SKU=Max('product_identifier')
                                                                     , store_name=Max('store_name')
                                                                     , paid_at=Count('paid_at')
                                                                     , product_name=Max('product_name')
                                                                     , seller_fees_amount_Avg=Avg('seller_fees_amount')
                                                                     , upsells_type_description1=Count('upsells_type_description1')
                                                                     , upsells_type_description2=Count('upsells_type_description2')
                                                                     , upsells_amount2=Sum('upsells_amount2')
                                                                     , disbursement_amount_Sum=Sum('disbursement_amount')
                                                                     , SKU_price_sum=Sum('SKU_price')
                                                                     , SKU_parts_price_sum=Sum('SKU_parts_price')
                                                                     , SKU_freight_sum=Sum('SKU_freight')
                                                                     , SKU_parts_freight_sum=Sum('SKU_parts_freight')
                                                                     , SKU_buy_one_price_sum=Sum('SKU_buy_one_price')
                                                                     , SKU_buy_one_freight_sum=Sum('SKU_buy_one_freight')
                                                                     ).order_by(Sort_order+Sort_field)[page_star:page_end]
            elif  table_number == 'table_number_sum':
                objs1 = objs1.values('product_internal_id').annotate(created_at=Count('created_at')
                                                                     , status_paid=Count('status_paid')
                                                                     , status_shipped=Count('status_shipped')
                                                                     , status_refunded=Count('status_refunded')
                                                                     , refunded_at_own=Count('refunded_at_own')
                                                                     , refunded_at_buyer=Count('refunded_at_buyer')
                                                                     , refund_amount_own=Sum('refund_amount_own')
                                                                     , refund_amount=Sum('refund_amount')
                                                                     , canceled_at=Count('canceled_at')
                                                                     , refunded_at=Count('refunded_at')
                                                                     , SKU=Max('product_identifier')
                                                                     , store_name=Max('store_name')
                                                                     , paid_at=Count('paid_at')
                                                                     , product_name=Max('product_name')
                                                                     , seller_fees_amount_Avg=Avg('seller_fees_amount')
                                                                     , upsells_type_description1=Count('upsells_type_description1')
                                                                     , upsells_type_description2=Count('upsells_type_description2')
                                                                     , upsells_amount2=Sum('upsells_amount2')
                                                                     , disbursement_amount_Sum=Sum('disbursement_amount')
                                                                     , SKU_price_sum=Sum('SKU_price')
                                                                     , SKU_parts_price_sum=Sum('SKU_parts_price')
                                                                     , SKU_freight_sum=Sum('SKU_freight')
                                                                     , SKU_parts_freight_sum=Sum('SKU_parts_freight')
                                                                     , SKU_buy_one_price_sum=Sum('SKU_buy_one_price')
                                                                     , SKU_buy_one_freight_sum=Sum('SKU_buy_one_freight')
                                                                     )

            DIS_AMOUT1 = 0  # 总成交价 人命币
            DIS_AMOUT2 = 0  # 总成交价 美元
            PAID_SUM = 0  # 订单总数

            REFUN_SUM_OWN = 0  # 退款总数_自己
            REFUN_SUM_BUYER = 0  # 退款总数_买家
            REFUN_SUM = 0  # 退款总数
            PROFIT_REFUN_OWN = 0  # 退款率_自己
            PROFIT_REFUN_BUYER = 0  # 退款率_买家
            PROFIT_REFUN = 0  # 退款率

            COSTF_OF = 0  # 店铺总成本
            NET_PROFIT_sfb = 0  # 流拍费
            NET_PROFIT = 0  # 店铺总利润
            EXCHANGE_RATE = 0  # 汇率
            展示总数 = 0
            拍卖总数 = 0
            SFB总 = 0
            拍卖成交率 = 0
            均SFB = 0
            总流拍费 = 0
            打包总成本 = 0
            for obj in objs1:
                # performance 数据
                obj['orders_performence'] = 0  # 总成交次数
                obj['schedules_performence'] = 0  # 总展示次数
                obj['scheduling_fees_performence'] = 0  # 平均SFB
                obj['dabaochenben'] = 0  # 打包成本
                objs2 = models_Tophatter.Performance_hours_time.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).filter(time_local__gte=start_time).filter(time_local__lte=end_time) \
                    .filter(time_hours_local=None).filter(Q(TIME_SELECT=None) | Q(TIME_SELECT='today'))
                if store_name != 'all':
                    objs2 = objs2.filter(store_name=store_name)
                if product_identifier != '':
                    objs2 = objs2.filter(identifier__contains=product_identifier)
                objs2 = objs2.values('identifier').annotate(schedules=Sum('schedules')
                                                            , orders=Sum('orders')
                                                            , scheduling_fees=Sum('scheduling_fees')).order_by('-schedules')
                if objs2:
                    obj['orders_performence'] = round((objs2[0]['orders']), 2)  # 成交次数
                    obj['schedules_performence'] = round((objs2[0]['schedules']), 2)  # 展示次数
                    obj['scheduling_fees_performence'] = round(objs2[0]['scheduling_fees'] / objs2[0]['schedules'], 2)  # 平均SFB
                    展示总数 += objs2[0]['schedules']
                    拍卖总数 += objs2[0]['orders']
                    SFB总 += objs2[0]['scheduling_fees']

                obj['seller_fees_amount'] = round((obj['seller_fees_amount_Avg'] * exchange_rate), 2)  # 平均平台费用

                if obj['paid_at']:
                    obj['disbursement_amount1'] = round((obj['disbursement_amount_Sum'] / obj['paid_at']), 2)  # 平均总到手价
                    obj['disbursement_amount2'] = round(((obj['disbursement_amount_Sum'] / obj['paid_at']) * exchange_rate), 2)  # 平均总到手价人民币
                    obj['closing_owe'] = round((obj['refunded_at_own'] / obj['paid_at']) * 100, 2)  # 自己的退货率
                    obj['closing_buyer'] = round((obj['refunded_at_buyer'] / obj['paid_at']) * 100, 2)  # 客户的退货率
                    obj['buy_one_closing'] = round((obj['upsells_type_description1'] / obj['paid_at']) * 100, 2)  # 加售率
                    obj['parts_closing'] = round((obj['upsells_type_description2'] / obj['paid_at']) * 100, 2)  # 配件率
                else:
                    obj['disbursement_amount1'] = 0
                    obj['disbursement_amount2'] = 0
                    obj['closing_owe'] = 0
                    obj['closing_buyer'] = 0
                    obj['buy_one_closing'] = 0
                    obj['parts_closing'] = 0

                if obj['seller_fees_amount'] != None:
                    obj['SKU_SFB_sum'] = obj['seller_fees_amount'] * obj['created_at']  # 平台花费
                else:
                    obj['SKU_SFB_sum'] = 0

                obj['disbursement_amount_Sum'] = round((obj['disbursement_amount_Sum']), 2)  # 净销售额
                obj['NET_PROFIT_sfb'] = round((obj['schedules_performence'] - obj['orders_performence']) * obj['scheduling_fees_performence'], 2)  # 流拍费

                oa = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(primary_image=Max('primary_image'),
                                                                                                 standard_product_id=Max('standard_product_id'))
                if oa:
                    obj['primary_image'] = oa[0]['primary_image']  # 主图
                    obj['standard_product_id'] = oa[0]['standard_product_id']  # 标准ID
                else:
                    obj['primary_image'] = ''  # 主图
                    obj['standard_product_id'] = ''  # 标准ID

                oc=models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=obj['store_name']).values('seller_id')
                if oc:
                    obj['seller_id'] = oc[0]['seller_id']
                else:
                    obj['seller_id'] = ''

                if obj['SKU'][-8:] == '-DELETED':
                    obj['T_SKU'] = obj['SKU'][:-15]
                else:
                    obj['T_SKU'] = obj['SKU']

                ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
                      SKU_price=Max('SKU_price')
                    , SKU_parts_price=Max('SKU_parts_price')
                    , SKU_weight=Max('SKU_weight')  # -------
                    , SKU_parts_weight=Max('SKU_parts_weight')  # -------
                    , SKU_variety=Max('SKU_variety')
                    , HAI_SKU_freight=Max('HAI_SKU_freight')  # -------
                    , Pingyou_min7_SKU_freight=Max('Pingyou_min7_SKU_freight')  # -------
                    , Pingyou_max7_SKU_freight=Max('Pingyou_max7_SKU_freight')  # -------
                    , top_colect = Max('top_colect'))  # -------
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


                    # 实际的统计值，从订单列表获取
                    if obj['SKU_price_sum']:
                        obj['SKU_price_sum'] = round(float(obj['SKU_price_sum']), 2)  # 总进价
                    else:
                        obj['SKU_price_sum'] = 0

                    if obj['SKU_freight_sum']:
                        obj['SKU_freight_sum'] = round(float(obj['SKU_freight_sum']), 2)  # 总运费
                    else:
                        obj['SKU_freight_sum'] = 0

                    if obj['SKU_parts_price_sum']:
                        obj['SKU_parts_price_sum'] = round(float(obj['SKU_parts_price_sum']), 2)  # 总配件价
                    else:
                        obj['SKU_parts_price_sum'] = 0

                    if obj['SKU_parts_freight_sum']:
                        obj['SKU_parts_freight_sum'] = round(float(obj['SKU_parts_freight_sum']), 2)  # 总配件运费
                    else:
                        obj['SKU_parts_freight_sum'] = 0

                    if obj['SKU_buy_one_price_sum']:
                        obj['SKU_buy_one_price_sum'] = round(float(obj['SKU_buy_one_price_sum']), 2)  # 总买一得一进价
                    else:
                        obj['SKU_buy_one_price_sum'] = 0

                    if obj['SKU_buy_one_freight_sum']:
                        obj['SKU_buy_one_freight_sum'] = round(float(obj['SKU_buy_one_freight_sum']), 2)  # 总买一得一运费
                    else:
                        obj['SKU_buy_one_freight_sum'] = 0

                    if (obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum']):
                        if obj['upsells_amount2']:
                            obj['upsells_amount2'] = obj['upsells_amount2']
                        else:
                            obj['upsells_amount2'] = 0
                        obj['parts_prf'] = (float(obj['upsells_amount2']) * exchange_rate - (
                                obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum'])) / (
                                                   obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum'])
                        obj['parts_prf'] = round(obj['parts_prf'] * 100, 2)
                    else:
                        obj['parts_prf'] = 0

                    if obj['refund_amount_own']:
                        obj['dabaochenben'] = 打包成本 * (obj['paid_at'] - obj['refunded_at_own'])
                    else:
                        obj['dabaochenben'] = 打包成本 * obj['paid_at']

                    obj['cost_of'] = round((obj['SKU_price_sum'] + obj['SKU_freight_sum'] + obj['SKU_parts_price_sum'] +
                                            obj['SKU_parts_freight_sum'] + obj['SKU_buy_one_price_sum'] + obj[
                                                'SKU_buy_one_freight_sum'] + obj['dabaochenben']), 2)  # 总成本

                    if obj['refunded_at_own']:
                        obj['cost_of'] = round((obj['cost_of'] - (obj['refunded_at_own'] * (float(obj['SKU_price'])))),2)  # 总成本
                    else:
                        obj['cost_of'] = obj['cost_of']

                    obj['Net_profit'] = round(((obj['disbursement_amount_Sum'] * exchange_rate) - obj['cost_of']), 2)  # 毛利润(有自己主动退款)

                    if obj['paid_at']:
                        obj['Net_profit_avg'] = round((obj['Net_profit'] / obj['paid_at']), 2)  # 平均利润
                    else:
                        obj['Net_profit_avg'] = 0

                    if obj['cost_of']:
                        obj['profit_margin'] = round((obj['Net_profit'] / obj['cost_of']) * 100, 2)  # 利润率
                    else:
                        obj['profit_margin'] = 0

                    obj['dabaochenben'] = round(obj['dabaochenben'], 2)

                    COSTF_OF += obj['cost_of']  # 店铺总成本
                    打包总成本 = 打包总成本 + obj['dabaochenben']  # 店铺发货总成本
                    NET_PROFIT += obj['Net_profit']  # 店铺总利润
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

                    obj['profit_margin'] = '--'
                    obj['Net_profit_avg'] = '--'
                    obj['Net_profit'] = '--'
                    obj['cost_of'] = '--'



                DIS_AMOUT1 += (obj['disbursement_amount1'] * obj['created_at'])  # 总到手价人命币
                DIS_AMOUT2 += (obj['disbursement_amount2'] * obj['created_at'])  # 总到手价 美元
                PAID_SUM += obj['paid_at']  # 店铺总订单

                REFUN_SUM_OWN += obj['refunded_at_own']  # 店铺总退货_自己
                REFUN_SUM += obj['refunded_at']  # 店铺总退货
                NET_PROFIT_sfb += obj['NET_PROFIT_sfb']  # 店铺总流拍费

                if PAID_SUM:
                    PROFIT_REFUN_OWN = round(((REFUN_SUM_OWN / PAID_SUM) * 100), 2)  # 总退货率_自己
                else:
                    PROFIT_REFUN_OWN = 0

                if PAID_SUM:
                    PROFIT_REFUN_BUYER = round(((REFUN_SUM_BUYER / PAID_SUM) * 100), 2)  # 总退货率_买家
                else:
                    PROFIT_REFUN_BUYER = 0

                if PAID_SUM:
                    PROFIT_REFUN = round(((REFUN_SUM / PAID_SUM) * 100), 2)  # 总退货率
                else:
                    PROFIT_REFUN = 0

                if 展示总数:
                    拍卖成交率 = round((拍卖总数 / 展示总数) * 100, 2)
                    均SFB = round((SFB总 / 展示总数), 2)
                else:
                    拍卖成交率 = 0
                    均SFB = 0

            if PAID_SUM:
                DIS_AMOUT1_AVG = round((DIS_AMOUT1 / PAID_SUM), 2)
                DIS_AMOUT2_AVG = round((DIS_AMOUT2 / PAID_SUM), 2)
            else:
                DIS_AMOUT1_AVG = '0'
                DIS_AMOUT2_AVG = '0'

            COSTF_OF = round(COSTF_OF, 2)  # 店铺总成本
            打包总成本 = round(打包总成本, 2)  # 店铺打包总成本
            # NET_PROFIT_sfb = PAID_SUM * (1 - 总预估成家率) * 总均SFB * exchange_rate  #,总预估成家率,总均SFB
            NET_PROFIT_sfb = round(NET_PROFIT_sfb, 2)  # 店铺总成本
            NET_PROFIT = round(NET_PROFIT - NET_PROFIT_sfb * exchange_rate, 2)  # 店铺总利润

            if COSTF_OF:
                PROFIT_MARGIN = round((NET_PROFIT / COSTF_OF) * 100, 2)  # 利润率
            else:
                PROFIT_MARGIN = '0'

            EXCHANGE_RATE = exchange_rate

            context_all = {
                'code': 0,
                'msg': 'asdfgh',
                'count': 1,
                'data': [{
                'DIS_AMOUT1_AVG': DIS_AMOUT1_AVG,
                'DIS_AMOUT2_AVG': DIS_AMOUT2_AVG,
                'PAID_SUM': PAID_SUM,
                'REFUN_SUM_OWN': REFUN_SUM_OWN,
                'REFUN_SUM_BUYER': REFUN_SUM_BUYER,
                'REFUN_SUM': REFUN_SUM,
                'PROFIT_REFUN_OWN': PROFIT_REFUN_OWN,
                'PROFIT_REFUN_BUYER': PROFIT_REFUN_BUYER,
                'PROFIT_REFUN': PROFIT_REFUN,
                'COSTF_OF': COSTF_OF,
                'NET_PROFIT': NET_PROFIT,
                'PROFIT_MARGIN': PROFIT_MARGIN,
                'EXCHANGE_RATE': EXCHANGE_RATE,
                '拍卖成交率': 拍卖成交率,
                '均SFB': 均SFB,
                '总流拍费': NET_PROFIT_sfb,
                '打包成本': 打包成本,
                '打包总成本': 打包总成本,
                }]
            }
            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs1),
            }
            if table_number == 'table_number_sum':
                return HttpResponse(json.dumps(context_all))
            elif table_number == 'table_number_detail':
                return HttpResponse(json.dumps(context))
            return render(request, 'Tophatter/All_orders_profitStatistics.html')
#拍卖订单利润统计
def Auction_orders_profitStatistics(request):
    user_app.change_info(request, 'Auction_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            start_time = request.GET.get('start_time', '')  # 统计时间
            end_time = request.GET.get('end_time', '')  # 统计时间
            time_local = request.GET.get('time_local', '')  # 统计时间
            product_identifier = request.GET.get('product_identifier', '')  # 商品名称

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式
            table_number = request.GET.get('table_number', '')  # 表格序号

            if limit == '' and  page == '' and  table_number == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {'store_name_users':list(store_name_users)}
                return render(request, 'Tophatter/Auction_orders_profitStatistics.html',context0)

            if start_time == '':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
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

            start_time_combine = (datetime.datetime.now() - datetime.timedelta(hours=159)).date().strftime('%Y-%m-%d')
            end_time_combine = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')

            if store_name == '':
                store_name = 'all'

            if Sort_field == '':
                Sort_field = 'paid_at'

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
            objs1 = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time) \
                .filter(canceled_at=None).filter(seller_fees_type_buy_nows=None)
            if store_name != 'all':
                objs1 = objs1.filter(store_name=store_name)
            if product_identifier != '':
                objs1 = objs1.filter(product_identifier__contains=product_identifier)

            if table_number == 'table_number_detail':
                count_all = objs1.values('product_internal_id').annotate(paid_at=Count('paid_at')).count()
                objs1 = objs1.values('product_internal_id').annotate(created_at=Count('created_at')
                                                                     , status_paid=Count('status_paid')
                                                                     , status_shipped=Count('status_shipped')
                                                                     , status_refunded=Count('status_refunded')
                                                                     , refunded_at_own=Count('refunded_at_own')
                                                                     , refunded_at_buyer=Count('refunded_at_buyer')
                                                                     , refund_amount_own=Sum('refund_amount_own')
                                                                     , refund_amount_buyer=Sum('refund_amount_buyer')
                                                                     , refund_amount=Sum('refund_amount')
                                                                     , canceled_at=Count('canceled_at')
                                                                     , refunded_at=Count('refunded_at')
                                                                     , SKU=Max('product_identifier')
                                                                     , store_name=Max('store_name')
                                                                     , paid_at=Count('paid_at')
                                                                     , product_name=Max('product_name')
                                                                     , disbursement_amount_Avg=Avg('disbursement_amount')
                                                                     , seller_fees_amount_Avg=Avg('seller_fees_amount')
                                                                     , upsells_type_description1=Count('upsells_type_description1')
                                                                     , upsells_type_description2=Count('upsells_type_description2')
                                                                     , upsells_amount2=Sum('upsells_amount2')
                                                                     , disbursement_amount_Sum=Sum('disbursement_amount')

                                                                     , SKU_price_sum=Sum('SKU_price')
                                                                     , SKU_parts_price_sum=Sum('SKU_parts_price')
                                                                     , SKU_freight_sum=Sum('SKU_freight')
                                                                     , SKU_parts_freight_sum=Sum('SKU_parts_freight')
                                                                     , SKU_buy_one_price_sum=Sum('SKU_buy_one_price')
                                                                     , SKU_buy_one_freight_sum=Sum('SKU_buy_one_freight')
                                                                     ).order_by(Sort_order+Sort_field)[page_star:page_end]
            elif  table_number == 'table_number_sum':
                objs1 = objs1.values('product_internal_id').annotate(created_at=Count('created_at')
                                                                     , status_paid=Count('status_paid')
                                                                     , status_shipped=Count('status_shipped')
                                                                     , status_refunded=Count('status_refunded')
                                                                     , refunded_at_own=Count('refunded_at_own')
                                                                     , refunded_at_buyer=Count('refunded_at_buyer')
                                                                     , refund_amount_own=Sum('refund_amount_own')
                                                                     , refund_amount_buyer=Sum('refund_amount_buyer')
                                                                     , refund_amount=Sum('refund_amount')
                                                                     , canceled_at=Count('canceled_at')
                                                                     , refunded_at=Count('refunded_at')
                                                                     , SKU=Max('product_identifier')
                                                                     , store_name=Max('store_name')
                                                                     , paid_at=Count('paid_at')
                                                                     , product_name=Max('product_name')
                                                                     , disbursement_amount_Avg=Avg('disbursement_amount')
                                                                     , seller_fees_amount_Avg=Avg('seller_fees_amount')
                                                                     , upsells_type_description1=Count('upsells_type_description1')
                                                                     , upsells_type_description2=Count('upsells_type_description2')
                                                                     , upsells_amount2=Sum('upsells_amount2')
                                                                     , disbursement_amount_Sum=Sum('disbursement_amount')

                                                                     , SKU_price_sum=Sum('SKU_price')
                                                                     , SKU_parts_price_sum=Sum('SKU_parts_price')
                                                                     , SKU_freight_sum=Sum('SKU_freight')
                                                                     , SKU_parts_freight_sum=Sum('SKU_parts_freight')
                                                                     , SKU_buy_one_price_sum=Sum('SKU_buy_one_price')
                                                                     , SKU_buy_one_freight_sum=Sum('SKU_buy_one_freight')
                                                                     )

            DIS_AMOUT1 = 0  # 总成交价 人命币
            DIS_AMOUT2 = 0  # 总成交价 美元
            PAID_SUM = 0  # 订单总数

            REFUN_SUM_OWN = 0  # 退款总数_自己
            REFUN_SUM_BUYER = 0  # 退款总数_买家
            REFUN_SUM = 0  # 退款总数
            PROFIT_REFUN_OWN = 0  # 退款率_自己
            PROFIT_REFUN_BUYER = 0  # 退款率_买家
            PROFIT_REFUN = 0  # 退款率
            COSTF_OF = 0  # 店铺总成本
            NET_PROFIT = 0  # 店铺总利润

            SAVE_TIME = 0  # 更新数据时间 北京
            SAVE_TIME_UTC = 0  # 更新数据时间 太平洋
            SCHEDULES = 0  # 总展示次数
            ORDERS = 0  # 总成交次数
            ORDERS_PRO = 0  # 成交率
            SFB_AVG = 0  # 平均SFB
            REVENUE_AVG = 0  # 平均销售额
            REVENUE_AVG_1 = 0
            REVENUE_AVG_2 = 0
            REVENUE_SUM = 0  # 平均销售额
            REVENUE_SUM_1 = 0
            REVENUE_SUM_2 = 0

            EXCHANGE_RATE = 0  # 汇率
            打包总成本 = 0

            for obj in objs1:
                obj['line_cost'] = 0  # 图表
                obj['scheduling_fees_performence'] = 0  # 平均安排费
                obj['schedules_performence'] = 0  # 总排单
                obj['orders_performence'] = 0  # 总出单
                obj['dabaochenben'] = 0  # 打包成本

                # performance 数据
                objs2 = models_Tophatter.Performance_hours_time.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']) \
                    .filter(time_local__gte=start_time).filter(time_local__lte=end_time).filter(time_hours_local=None) \
                    .filter(Q(TIME_SELECT=None) | Q(TIME_SELECT='today'))
                if store_name != 'all':
                    objs2 = objs2.filter(store_name=store_name)
                if product_identifier != '':
                    objs2 = objs2.filter(identifier__contains=product_identifier)
                objs2 = objs2.values('identifier').annotate(cost_basis=Max('cost_basis')
                                                            , store_name=Max('store_name')
                                                            , SKU=Max('identifier')
                                                            , schedules=Sum('schedules')
                                                            , orders=Sum('orders')
                                                            , revenue=Sum('revenue')
                                                            , fees=Sum('fees')
                                                            , save_time=Min('save_time')
                                                            , scheduling_fees=Sum('scheduling_fees')) \
                    .order_by('-schedules')
                if objs2:
                    SAVE_TIME = objs2[0]['save_time']
                    SAVE_TIME_UTC = objs2[0]['save_time'] - datetime.timedelta(hours=15)
                    obj['closing_performence'] = round(((objs2[0]['orders'] / objs2[0]['schedules']) * 100), 2)  # 成交率
                    obj['orders_performence'] = round((objs2[0]['orders']), 2)  # 成交次数
                    obj['schedules_performence'] = round((objs2[0]['schedules']), 2)  # 展示次数
                    obj['scheduling_fees_performence'] = round((objs2[0]['scheduling_fees'] / objs2[0]['schedules']), 2)  # 平均SFB
                    if objs2[0]['orders']:
                        obj['revenue_performence_1'] = round((objs2[0]['revenue'] / objs2[0]['orders']), 2)  # 平均销售额
                    else:
                        obj['revenue_performence_1'] = 0  # 平均销售额
                    obj['revenue_performence_2'] = round((obj['revenue_performence_1'] * exchange_rate), 2)  # 平均销售额

                    if objs2[0]['orders']:
                        obj['revenue_performence_3'] = round(
                            ((objs2[0]['revenue'] - objs2[0]['fees']) / objs2[0]['orders']), 2)  # 平均到手
                    else:
                        obj['revenue_performence_3'] = 0  # 平均到手
                    obj['revenue_performence_4'] = round((obj['revenue_performence_3'] * exchange_rate), 2)  # 平均到手

                    SCHEDULES += objs2[0]['schedules']  # 总展示次数
                    ORDERS += objs2[0]['orders']  # 总成交次数
                    SFB_AVG += objs2[0]['scheduling_fees']  # 总共的SFB
                    REVENUE_AVG += objs2[0]['revenue']  # 总共销售额
                    REVENUE_SUM += (objs2[0]['revenue'] - objs2[0]['fees'])  # 总共花费
                else:
                    obj['closing_performence'] = 0.0
                    obj['revenue_performence_1'] = 0
                    obj['revenue_performence_2']=0


                objs3 = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(product_identifier=obj['SKU']) \
                    .filter(data_time_created_at__gte=start_time_combine).filter(data_time_created_at__lte=end_time_combine) \
                    .filter(canceled_at=None)
                if store_name != 'all':
                    objs3 = objs3.filter(store_name=store_name)
                if product_identifier != '':
                    objs3 = objs3.filter(product_identifier__contains=product_identifier)
                objs3 = objs3.values('product_identifier') \
                    .annotate(created_at=Count('created_at', distinct=True), customer_name=Count('customer_name', distinct=True)) \
                    .order_by('-created_at')
                # print(objs3)
                if objs3:
                    if objs3[0]['created_at']:
                        obj['customer_name_pro'] = round(
                            ((objs3[0]['created_at'] - objs3[0]['customer_name']) / objs3[0]['created_at']) * 100,
                            2)  # 5天合并率
                    else:
                        obj['customer_name_pro'] = 0  # 5天合并率

                obj['disbursement_amount1'] = round((obj['disbursement_amount_Avg'] + obj['seller_fees_amount_Avg']), 2)  # 平均成交价
                obj['disbursement_amount2'] = round(((obj['disbursement_amount_Avg'] + obj['seller_fees_amount_Avg']) * exchange_rate), 2)  # 平均成交价人民币
                obj['seller_fees_amount'] = round((obj['seller_fees_amount_Avg'] * exchange_rate), 2)  # 平均平台费用

                if obj['paid_at']:
                    obj['closing_owe'] = round((obj['refunded_at_own'] / obj['paid_at']) * 100, 2)  # 自己的退货率
                    obj['closing_buyer'] = round((obj['refunded_at_buyer'] / obj['paid_at']) * 100, 2)  # 客户的退货率
                    obj['buy_one_closing'] = round((obj['upsells_type_description1'] / obj['paid_at']) * 100, 2)  # 加售率
                    obj['parts_closing'] = round((obj['upsells_type_description2'] / obj['paid_at']) * 100, 2)  # 配件率
                else:
                    obj['closing_owe'] = 0
                    obj['closing_buyer'] = 0
                    obj['buy_one_closing'] = 0
                    obj['parts_closing'] = 0


                if obj['seller_fees_amount'] != None:
                    obj['SKU_SFB_sum'] = obj['seller_fees_amount'] * obj['created_at']  # 平台花费
                else:
                    obj['SKU_SFB_sum'] = 0

                It = models_Tophatter.closing_buyer.objects.filter(USER_ID=USER_ID).filter(SKU=obj['SKU']).values('closing_buyer_1')
                if It:
                    obj['closing_buyer_1'] = float(It[0]['closing_buyer_1'])
                else:
                    obj['closing_buyer_1'] = 6.5

                obj['disbursement_amount_Sum'] = round((obj['disbursement_amount_Sum'] * (1 - (obj['closing_buyer_1']) / 100)), 2) # 净销售额（自己计算退货率）
                obj['NET_PROFIT_sfb'] = round((obj['schedules_performence'] - obj['orders_performence']) * obj['scheduling_fees_performence'], 2)  # 流拍费
                obj['disbursement_amount_Sum'] = obj['disbursement_amount_Sum'] - obj['NET_PROFIT_sfb']  # 除去流拍的安排费

                oa = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
                    primary_image=Max('primary_image', distinct=True),
                    standard_product_id=Max('standard_product_id', distinct=True))
                if oa:
                    obj['primary_image'] = oa[0]['primary_image']  # 主图
                    obj['standard_product_id'] = oa[0]['standard_product_id']  # 标准ID

                oc = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=obj['store_name']).values('seller_id')
                if oc:
                    obj['seller_id'] = oc[0]['seller_id']
                else:
                    obj['seller_id'] = ''

                ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
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

                    # 实际的统计值，从订单列表获取
                    if obj['SKU_price_sum']:
                        obj['SKU_price_sum'] = round(float(obj['SKU_price_sum']), 2)  # 总进价
                    else:
                        obj['SKU_price_sum'] = 0

                    if obj['SKU_freight_sum']:
                        obj['SKU_freight_sum'] = round(float(obj['SKU_freight_sum']), 2)  # 总运费
                    else:
                        obj['SKU_freight_sum'] = 0

                    if obj['SKU_parts_price_sum']:
                        obj['SKU_parts_price_sum'] = round(float(obj['SKU_parts_price_sum']), 2)  # 总配件价
                    else:
                        obj['SKU_parts_price_sum'] = 0

                    if obj['SKU_parts_freight_sum']:
                        obj['SKU_parts_freight_sum'] = round(float(obj['SKU_parts_freight_sum']), 2)  # 总配件运费
                    else:
                        obj['SKU_parts_freight_sum'] = 0

                    if obj['SKU_buy_one_price_sum']:
                        obj['SKU_buy_one_price_sum'] = round(float(obj['SKU_buy_one_price_sum']), 2)  # 总买一得一进价
                    else:
                        obj['SKU_buy_one_price_sum'] = 0

                    if obj['SKU_buy_one_freight_sum']:
                        obj['SKU_buy_one_freight_sum'] = round(float(obj['SKU_buy_one_freight_sum']), 2)  # 总买一得一运费
                    else:
                        obj['SKU_buy_one_freight_sum'] = 0

                    if (obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum']):
                        if obj['upsells_amount2']:
                            obj['upsells_amount2'] = obj['upsells_amount2']
                        else:
                            obj['upsells_amount2'] = 0
                        obj['parts_prf'] = (float(obj['upsells_amount2']) * exchange_rate - (
                                obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum'])) / (
                                                   obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum'])
                        obj['parts_prf'] = round(obj['parts_prf'] * 100, 2)
                    else:
                        obj['parts_prf'] = 0

                    obj['dabaochenben'] = 打包成本 * obj['paid_at']

                    obj['cost_of'] = round((obj['SKU_price_sum'] + obj['SKU_freight_sum'] + obj['SKU_parts_price_sum'] +
                                            obj['SKU_parts_freight_sum'] + obj['SKU_buy_one_price_sum'] + obj[
                                                'SKU_buy_one_freight_sum'] + obj['dabaochenben']), 2)  # 总成本

                    if obj['refunded_at_own']:
                        obj['cost_of'] = round((obj['cost_of'] - (obj['refunded_at_own'] * (float(obj['SKU_price'])))),2)  # 总成本
                    else:
                        obj['cost_of'] = obj['cost_of']

                    obj['Net_profit'] = round(((obj['disbursement_amount_Sum'] * exchange_rate) - obj['cost_of']),
                                              2)  # 毛利润(有自己主动退款)

                    if obj['paid_at']:
                        obj['Net_profit_avg'] = round((obj['Net_profit'] / obj['paid_at']), 2)  # 平均利润
                    else:
                        obj['Net_profit_avg'] = 0

                    if obj['cost_of']:
                        obj['profit_margin'] = round((obj['Net_profit'] / obj['cost_of']) * 100, 2)  # 利润率
                    else:
                        obj['profit_margin'] = 0

                    obj['dabaochenben'] = round(obj['dabaochenben'], 2)

                    打包总成本 += obj['dabaochenben']
                    COSTF_OF += obj['cost_of']  # 店铺总成本
                    NET_PROFIT += obj['Net_profit']  # 店铺总利润
                    # obj['line_cost'] = round((float(obj['SKU_price']) + float(obj['SKU_freight'])), 2)  # 总成本
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

                    obj['profit_margin'] = '--'
                    obj['Net_profit_avg'] = '--'
                    obj['Net_profit'] = '--'
                    obj['cost_of'] = '--'

                DIS_AMOUT1 += (obj['disbursement_amount1'] * obj['created_at'])  # 总成交价人命币
                DIS_AMOUT2 += (obj['disbursement_amount2'] * obj['created_at'])  # 总成交价 美元
                PAID_SUM += obj['paid_at']  # 店铺总订单

                REFUN_SUM_OWN += obj['refunded_at_own']  # 店铺总退货_自己
                REFUN_SUM_BUYER += obj['refunded_at_buyer']  # 店铺总退货_买家
                REFUN_SUM += obj['refunded_at']  # 店铺总退货

                if PAID_SUM:
                    PROFIT_REFUN_OWN = round(((REFUN_SUM_OWN / PAID_SUM) * 100), 2)  # 总退货率_自己
                else:
                    PROFIT_REFUN_OWN = 0

                if PAID_SUM:
                    PROFIT_REFUN_BUYER = round(((REFUN_SUM_BUYER / PAID_SUM) * 100), 2)  # 总退货率_买家
                else:
                    PROFIT_REFUN_BUYER = 0

                if PAID_SUM:
                    PROFIT_REFUN = round(((REFUN_SUM / PAID_SUM) * 100), 2)  # 总退货率
                else:
                    PROFIT_REFUN = 0

            if SCHEDULES:
                ORDERS_PRO = round(((ORDERS / SCHEDULES) * 100), 2)  # 总成交率
            else:
                ORDERS_PRO = 0

            if SCHEDULES:
                SFB_AVG = round((SFB_AVG / SCHEDULES), 2)  # 平均SFB
            else:
                SFB_AVG = 0

            if ORDERS:
                REVENUE_AVG_1 = round((REVENUE_AVG / ORDERS), 2)  # 平均销售额
                REVENUE_AVG_2 = round(((REVENUE_AVG / ORDERS) * exchange_rate), 2)  # 平均销售额
            else:
                REVENUE_AVG_1 = 0
                REVENUE_AVG_2 = 0

            if ORDERS:
                REVENUE_SUM_1 = round((REVENUE_SUM / ORDERS), 2)  # 平均到手
                REVENUE_SUM_2 = round(((REVENUE_SUM / ORDERS) * exchange_rate), 2)  # 平均到手
            else:
                REVENUE_SUM_1 = 0
                REVENUE_SUM_2 = 0

            if PAID_SUM:
                DIS_AMOUT1_AVG = round((DIS_AMOUT1 / PAID_SUM), 2)  # 均销售额
                DIS_AMOUT2_AVG = round((DIS_AMOUT2 / PAID_SUM), 2)
            else:
                DIS_AMOUT1_AVG = '0'
                DIS_AMOUT2_AVG = '0'

            打包总成本 = round(打包总成本, 2)  # 打包总成本
            COSTF_OF = round(COSTF_OF, 2)  # 店铺总成本
            NET_PROFIT = round(NET_PROFIT, 2)  # 店铺总利润

            if COSTF_OF:
                PROFIT_MARGIN = round((NET_PROFIT / COSTF_OF) * 100, 2)  # 利润率
            else:
                PROFIT_MARGIN = '0'

            EXCHANGE_RATE = exchange_rate

            context_all = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': [{
                # 统计数据
                'DIS_AMOUT1_AVG': DIS_AMOUT1_AVG,
                'DIS_AMOUT2_AVG': DIS_AMOUT2_AVG,
                'PAID_SUM': PAID_SUM,
                'REFUN_SUM_OWN': REFUN_SUM_OWN,
                'REFUN_SUM_BUYER': REFUN_SUM_BUYER,
                'REFUN_SUM': REFUN_SUM,
                'PROFIT_REFUN_OWN': PROFIT_REFUN_OWN,
                'PROFIT_REFUN_BUYER': PROFIT_REFUN_BUYER,
                'PROFIT_REFUN': PROFIT_REFUN,
                'COSTF_OF': COSTF_OF,
                'NET_PROFIT': NET_PROFIT,
                'PROFIT_MARGIN': PROFIT_MARGIN,

                'SAVE_TIME': SAVE_TIME,
                'SAVE_TIME_UTC': SAVE_TIME_UTC,
                'SCHEDULES': SCHEDULES,
                'ORDERS': ORDERS,
                'ORDERS_PRO': ORDERS_PRO,
                'SFB_AVG': SFB_AVG,
                'REVENUE_AVG_1': REVENUE_AVG_1,
                'REVENUE_AVG_2': REVENUE_AVG_2,
                'REVENUE_SUM_1': REVENUE_SUM_1,
                'REVENUE_SUM_2': REVENUE_SUM_2,
                '打包总成本': 打包总成本,

                'EXCHANGE_RATE': EXCHANGE_RATE,
                }]
            }
            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs1)
            }
            if table_number == 'table_number_sum':
                return HttpResponse(json.dumps(context_all, cls=CJsonEncoder))
            elif table_number == 'table_number_detail':
                return HttpResponse(json.dumps(context))
            return render(request, 'Tophatter/Auction_orders_profitStatistics.html')
#拍卖实时统计
def Auction_orders_profitStatistics_now(request):
    user_app.change_info(request, 'Auction_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            time_local = request.GET.get('time_local', '')  # 时间区间
            store_name = request.GET.get('store_name', '')  # 店铺名
            identifier = request.GET.get('product_identifier', '')  # SKU名

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式
            table_number = request.GET.get('table_number', '')  # 表格序号

            if limit == '' and  page == '' and  table_number == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {'store_name_users':list(store_name_users)}
                return render(request, 'Tophatter/Auction_orders_profitStatistics_now.html',context0)

            if time_local == '':
                time_local = 'today'

            if store_name == '':
                store_name = 'all'

            if Sort_field == '':
                Sort_field = 'schedules'

            if Sort_order == 'desc' or Sort_order == '':
                Sort_order = '-'
            elif Sort_order == 'asc':
                Sort_order = ''
            else:
                Sort_order = '-'

            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            objs1 = models_Tophatter.Performance_hours_time.objects.filter(USER_ID=USER_ID).filter(~Q(TIME_SELECT=None)).filter(TIME_SELECT=time_local)
            if store_name != 'all':
                objs1 = objs1.filter(store_name=store_name)
            if identifier != '':
                objs1 = objs1.filter(identifier__contains=identifier)

            if table_number == 'table_number_detail':
                count_all = objs1.values('id').annotate(schedules=Max('schedules')).count()
                objs1 = objs1.values('id').annotate(  cost_basis=Max('cost_basis')
                                                    , store_name=Max('store_name')
                                                    , SKU=Max('identifier')
                                                    , schedules=Max('schedules')
                                                    , orders=Max('orders')
                                                    , revenue=Max('revenue')
                                                    , fees=Max('fees')
                                                    , save_time=Min('save_time')
                                                    , scheduling_fees=Avg('scheduling_fees')).order_by(Sort_order+Sort_field)[page_star:page_end]
            elif  table_number == 'table_number_sum':
                objs1 = objs1.values('id').annotate(  cost_basis=Max('cost_basis')
                                                    , store_name=Max('store_name')
                                                    , SKU=Max('identifier')
                                                    , schedules=Max('schedules')
                                                    , orders=Max('orders')
                                                    , revenue=Max('revenue')
                                                    , fees=Max('fees')
                                                    , save_time=Min('save_time')
                                                    , scheduling_fees=Avg('scheduling_fees'))
                # home 页 提醒数据
                TODO_datas = models_Tophatter.TODO.objects.filter(USER_ID=USER_ID).values()  # home页数据
                for TODO_data in TODO_datas:
                    TODO_data['name'] = literal_eval(TODO_data['name'])
                    TODO_data['data'] = literal_eval(TODO_data['data'])

            SCHEDULES = 0  # 总展示次数
            ORDERS = 0  # 总成交次数
            ORDERS_PRO = 0  # 成交率
            SFB_AVG = 0  # 平均SFB
            FEES_SUM = 0  # 总成本
            PROFIT_SUM = 0  # 总利润
            PROFIT_PRO = 0  # 利润率
            PROFIT_AVG = 0  # 平均的利润
            SAVE_TIME = 0  # 保存时间
            SAVE_TIME_UTC = 0  # utc时间
            打包总成本 = 0  # 打包总成本

            EXCHANGE_RATE = 0  # 汇率

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

            for obj in objs1:
                obj['line_cost'] = 0  # 图表数据
                SAVE_TIME = obj['save_time']
                obj['dabaochenben'] = 0
                SAVE_TIME_UTC = obj['save_time'] - datetime.timedelta(hours=15)
                obj['closing'] = round(((obj['orders'] / obj['schedules']) * 100), 2)  # 成交率
                if obj['orders']:
                    obj['revenue_avg'] = round((obj['revenue'] / obj['orders']), 2)  # 平台总费用
                else:
                    obj['revenue_avg'] = 0
                obj['fees_sum'] = round((obj['fees']), 2)  # 平台总费用
                obj['fees_avg'] = round((obj['fees_sum'] / obj['schedules']), 2)  # 平台平均费用
                obj['SFB_avg'] = round((obj['scheduling_fees'] / obj['schedules']), 2)  # 平均SFB

                obj['top_profit_sum'] = round((obj['revenue'] - obj['fees_sum']), 2)  # 总平台利

                if obj['orders']:
                    obj['top_profit_avg'] = round((obj['top_profit_sum'] / obj['orders']), 2)  # 平均平台利
                else:
                    obj['top_profit_avg'] = 0

                oa = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
                    primary_image=Max('primary_image', distinct=True),
                    standard_product_id=Max('standard_product_id', distinct=True))
                if oa:
                    obj['primary_image'] = oa[0]['primary_image']  # 主图
                    obj['standard_product_id'] = oa[0]['standard_product_id']  # 标准ID

                oc = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=obj['store_name']).values('seller_id')
                if oc:
                    obj['seller_id'] = oc[0]['seller_id']
                else:
                    obj['seller_id'] = ''

                ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
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

                    obj['dabaochenben'] = 打包成本

                    obj['profit_sum'] = round(((obj['top_profit_sum'] * exchange_rate) - ((float(obj['SKU_price']) + float(obj['SKU_freight'])) * obj['orders'])), 2)  # 毛利润
                    obj['pay_self_sum'] = round(((float(obj['SKU_price']) + float(obj['SKU_freight']) + obj['dabaochenben']) * obj['orders']), 2)  # 总成本

                    if obj['pay_self_sum']:
                        obj['profit_pro'] = round(((obj['profit_sum'] / obj['pay_self_sum']) * 100), 2)  #
                    else:
                        obj['profit_pro'] = 0

                    if obj['orders']:
                        obj['profit_sum_avg'] = round((obj['profit_sum'] / obj['orders']), 2)  # 平均毛利润
                    else:
                        obj['profit_sum_avg'] = 0

                    obj['dabaochenben'] = round(obj['dabaochenben'] * obj['orders'], 2)

                    打包总成本 += obj['dabaochenben']  # 打包总成本
                    FEES_SUM += round((obj['pay_self_sum']), 2)  # 总成本
                    PROFIT_SUM += obj['profit_sum']  # 总毛润
                    obj['line_cost'] = round((float(obj['SKU_price'])), 2)  # 总成本
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

                    obj['profit_margin'] = '--'
                    obj['Net_profit_avg'] = '--'
                    obj['Net_profit'] = '--'
                    obj['cost_of'] = '--'

                SCHEDULES += obj['schedules']  # 总展示次数
                ORDERS += obj['orders']  # 总成交次数
                SFB_AVG += obj['scheduling_fees']  # 总共的SFB

            if SCHEDULES:
                ORDERS_PRO = round(((ORDERS / SCHEDULES) * 100), 2)
            else:
                ORDERS_PRO = 0

            if FEES_SUM:
                PROFIT_PRO = round(((PROFIT_SUM / FEES_SUM) * 100), 2)  # 利润率
            else:
                PROFIT_PRO = 0

            if SCHEDULES:
                SFB_AVG = SFB_AVG / SCHEDULES  # 平均SFB
            else:
                SFB_AVG = 0

            打包总成本 = round(打包总成本, 2)
            FEES_SUM = round((FEES_SUM), 2)
            PROFIT_SUM = round((PROFIT_SUM), 2)
            SFB_AVG = round((SFB_AVG), 2)

            EXCHANGE_RATE = exchange_rate

            # 5m 订单
            try:
                start_time_1 = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                end_time_1 = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                start_time_2 = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')
                end_time_2 = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')
                start_time_3 = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
                end_time_3 = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                M5_TODAY_ODERS = models_five_miles.orders_date_5miles.objects.filter(USER_ID=USER_ID).filter(created_at_data__gte=start_time_1).filter(created_at_data__lte=end_time_1).count()
                M5_YESTODAY_ODERS = models_five_miles.orders_date_5miles.objects.filter(USER_ID=USER_ID).filter(created_at_data__gte=start_time_2).filter(created_at_data__lte=end_time_2).count()
                M5_SEVENDAYS_ODERS = models_five_miles.orders_date_5miles.objects.filter(USER_ID=USER_ID).filter(created_at_data__gte=start_time_3).filter(created_at_data__lte=end_time_3).count()
            except:
                M5_TODAY_ODERS = 0
                M5_YESTODAY_ODERS = 0
                M5_SEVENDAYS_ODERS = 0

            if table_number == 'table_number_sum':
                context_all = {
                    'code': 0,
                    'msg': 'asdfgh',
                    'count': 1,
                    'data': [{
                        # 'TODO_datas': TODO_datas,
                        # 统计数据
                        'EXCHANGE_RATE': EXCHANGE_RATE,
                        'SCHEDULES': SCHEDULES,
                        'ORDERS': ORDERS,
                        'ORDERS_PRO': ORDERS_PRO,
                        'SFB_AVG': SFB_AVG,
                        'FEES_SUM': FEES_SUM,
                        'PROFIT_SUM': PROFIT_SUM,
                        'PROFIT_PRO': PROFIT_PRO,
                        'SAVE_TIME': SAVE_TIME,
                        'SAVE_TIME_UTC': SAVE_TIME_UTC,
                        '打包总成本': 打包总成本,

                        # 5M数据
                        'M5_TODAY_ODERS': M5_TODAY_ODERS,
                        'M5_YESTODAY_ODERS': M5_YESTODAY_ODERS,
                        'M5_SEVENDAYS_ODERS': M5_SEVENDAYS_ODERS,
                    }]
                }
                return HttpResponse(json.dumps(context_all, cls=CJsonEncoder))
            elif table_number == 'table_number_detail':
                context = {
                    'code': 0,
                    'msg': 'asdfgh',
                    'count': count_all,
                    'data': list(objs1)
                }
                return HttpResponse(json.dumps(context, cls=CJsonEncoder))
            return render(request, 'Tophatter/Auction_orders_profitStatistics_now.html')
#一口价利润统计
def Buynow_orders_profitStatistics(request):
    user_app.change_info(request, 'Buynow_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            start_time = request.GET.get('start_time', '')  # 统计时间
            end_time = request.GET.get('end_time', '')  # 统计时间
            time_local = request.GET.get('time_local', '')  # 统计时间
            product_identifier = request.GET.get('product_identifier', '')  # 商品名称

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式
            table_number = request.GET.get('table_number', '')  # 表格序号

            if limit == '' and  page == '' and  table_number == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {'store_name_users':list(store_name_users)}
                return render(request, 'Tophatter/Buynow_orders_profitStatistics.html',context0)

            if start_time == '':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
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

            start_time_combine = (datetime.datetime.now() - datetime.timedelta(hours=159)).date().strftime('%Y-%m-%d')
            end_time_combine = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')

            if store_name == '':
                store_name = 'all'

            if Sort_field == '':
                Sort_field = 'store_name'

            if Sort_order == 'desc' :
                Sort_order = '-'
            elif Sort_order == 'asc'or Sort_order == '':
                Sort_order = ''
            else:
                Sort_order = ''

            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            # 订单数据
            objs1 = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None).filter(~Q(seller_fees_type_buy_nows=None)).filter(
                data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time)
            if store_name != 'all':
                objs1 = objs1.filter(store_name=store_name)
            if product_identifier != '':
                objs1 = objs1.filter(product_identifier__contains=product_identifier)
            if table_number == 'table_number_detail':
                count_all = objs1.values('product_internal_id').annotate(paid_at=Count('paid_at')).count()
                objs1 = objs1.values('product_internal_id').annotate(  created_at=Count('created_at')
                                                                     , status_paid=Count('status_paid')
                                                                     , status_shipped=Count('status_shipped')
                                                                     , status_refunded=Count('status_refunded')
                                                                     , refunded_at_own=Count('refunded_at_own')
                                                                     , refunded_at_buyer=Count('refunded_at_buyer')
                                                                     , refund_amount_own=Sum('refund_amount_own')
                                                                     , refund_amount_buyer=Sum('refund_amount_buyer')
                                                                     , refund_amount=Sum('refund_amount')
                                                                     , canceled_at=Count('canceled_at')
                                                                     , refunded_at=Count('refunded_at')
                                                                     , SKU=Max('product_identifier')
                                                                     , store_name=Max('store_name')
                                                                     , paid_at=Count('paid_at')
                                                                     , product_name=Max('product_name')
                                                                     , disbursement_amount_Avg=Avg('disbursement_amount')
                                                                     , seller_fees_amount_Avg=Avg('seller_fees_amount')
                                                                     , upsells_type_description1=Count('upsells_type_description1')
                                                                     , upsells_type_description2=Count('upsells_type_description2')
                                                                     , upsells_amount2=Sum('upsells_amount2')
                                                                     , disbursement_amount_Sum=Sum('disbursement_amount')

                                                                     , SKU_price_sum=Sum('SKU_price')
                                                                     , SKU_parts_price_sum=Sum('SKU_parts_price')
                                                                     , SKU_freight_sum=Sum('SKU_freight')
                                                                     , SKU_parts_freight_sum=Sum('SKU_parts_freight')
                                                                     , SKU_buy_one_price_sum=Sum('SKU_buy_one_price')
                                                                     , SKU_buy_one_freight_sum=Sum('SKU_buy_one_freight')
                                                                     ).order_by(Sort_order+Sort_field)[page_star:page_end]
            elif  table_number == 'table_number_sum':
                objs1 = objs1.values('product_internal_id').annotate(  created_at=Count('created_at')
                                                                     , status_paid=Count('status_paid')
                                                                     , status_shipped=Count('status_shipped')
                                                                     , status_refunded=Count('status_refunded')
                                                                     , refunded_at_own=Count('refunded_at_own')
                                                                     , refunded_at_buyer=Count('refunded_at_buyer')
                                                                     , refund_amount_own=Sum('refund_amount_own')
                                                                     , refund_amount_buyer=Sum('refund_amount_buyer')
                                                                     , refund_amount=Sum('refund_amount')
                                                                     , canceled_at=Count('canceled_at')
                                                                     , refunded_at=Count('refunded_at')
                                                                     , SKU=Max('product_identifier')
                                                                     , store_name=Max('store_name')
                                                                     , paid_at=Count('paid_at')
                                                                     , product_name=Max('product_name')
                                                                     , disbursement_amount_Avg=Avg('disbursement_amount')
                                                                     , seller_fees_amount_Avg=Avg('seller_fees_amount')
                                                                     , upsells_type_description1=Count('upsells_type_description1')
                                                                     , upsells_type_description2=Count('upsells_type_description2')
                                                                     , upsells_amount2=Sum('upsells_amount2')
                                                                     , disbursement_amount_Sum=Sum('disbursement_amount')

                                                                     , SKU_price_sum=Sum('SKU_price')
                                                                     , SKU_parts_price_sum=Sum('SKU_parts_price')
                                                                     , SKU_freight_sum=Sum('SKU_freight')
                                                                     , SKU_parts_freight_sum=Sum('SKU_parts_freight')
                                                                     , SKU_buy_one_price_sum=Sum('SKU_buy_one_price')
                                                                     , SKU_buy_one_freight_sum=Sum('SKU_buy_one_freight')
                                                                     )

            DIS_AMOUT1 = 0  # 总成交价 人命币
            DIS_AMOUT2 = 0  # 总成交价 美元
            PAID_SUM = 0  # 订单总数

            REFUN_SUM_OWN = 0  # 退款总数_自己
            REFUN_SUM_BUYER = 0  # 退款总数_买家
            REFUN_SUM = 0  # 退款总数
            PROFIT_REFUN_OWN = 0  # 退款率_自己
            PROFIT_REFUN_BUYER = 0  # 退款率_买家
            PROFIT_REFUN = 0  # 退款率
            COSTF_OF = 0  # 店铺总成本
            NET_PROFIT = 0  # 店铺总利润

            SAVE_TIME = 0  # 更新数据时间 北京
            SAVE_TIME_UTC = 0  # 更新数据时间 太平洋
            SCHEDULES = 0  # 总展示次数
            ORDERS = 0  # 总成交次数
            ORDERS_PRO = 0  # 成交率
            SFB_AVG = 0  # 平均SFB
            REVENUE_AVG = 0  # 平均销售额
            REVENUE_AVG_1 = 0
            REVENUE_AVG_2 = 0
            REVENUE_SUM = 0  # 平均销售额
            REVENUE_SUM_1 = 0
            REVENUE_SUM_2 = 0

            EXCHANGE_RATE = 0  # 汇率
            打包总成本 = 0

            for obj in objs1:
                obj['line_cost'] = 0  # 图表

                objs3 = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(product_identifier=obj['SKU']) \
                    .filter(data_time_created_at__gte=start_time_combine).filter(data_time_created_at__lte=end_time_combine) \
                    .filter(canceled_at=None)
                if store_name != 'all':
                    objs3 = objs3.filter(store_name=store_name)
                if product_identifier != '':
                    objs3 = objs3.filter(product_identifier__contains=product_identifier)
                objs3 = objs3.values('product_identifier') \
                    .annotate(created_at=Count('created_at', distinct=True), customer_name=Count('customer_name', distinct=True)) \
                    .order_by('-created_at')
                # print(objs3)
                if objs3:
                    if objs3[0]['created_at']:
                        obj['customer_name_pro'] = round(
                            ((objs3[0]['created_at'] - objs3[0]['customer_name']) / objs3[0]['created_at']) * 100,
                            2)  # 5天合并率
                    else:
                        obj['customer_name_pro'] = 0  # 5天合并率
                else:
                    obj['customer_name_pro'] = 0  # 5天合并率

                obj['disbursement_amount1'] = round((obj['disbursement_amount_Avg'] + obj['seller_fees_amount_Avg']), 2)  # 平均成交价
                obj['disbursement_amount2'] = round(((obj['disbursement_amount_Avg'] + obj['seller_fees_amount_Avg']) * exchange_rate), 2)  # 平均成交价人民币
                obj['seller_fees_amount'] = round((obj['seller_fees_amount_Avg'] * exchange_rate), 2)  # 平均平台费用

                if obj['paid_at']:
                    obj['closing_owe'] = round((obj['refunded_at_own'] / obj['paid_at']) * 100, 2)  # 自己的退货率
                    obj['closing_buyer'] = round((obj['refunded_at_buyer'] / obj['paid_at']) * 100, 2)  # 客户的退货率
                    obj['buy_one_closing'] = round((obj['upsells_type_description1'] / obj['paid_at']) * 100, 2)  # 加售率
                    obj['parts_closing'] = round((obj['upsells_type_description2'] / obj['paid_at']) * 100, 2)  # 配件率
                else:
                    obj['closing_owe'] = 0
                    obj['closing_buyer'] = 0
                    obj['buy_one_closing'] = 0
                    obj['parts_closing'] = 0


                if obj['seller_fees_amount'] != None:
                    obj['SKU_SFB_sum'] = obj['seller_fees_amount'] * obj['created_at']  # 平台花费
                else:
                    obj['SKU_SFB_sum'] = 0

                oa = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
                    primary_image=Max('primary_image', distinct=True),
                    standard_product_id=Max('standard_product_id', distinct=True))
                if oa:
                    obj['primary_image'] = oa[0]['primary_image']  # 主图
                    obj['standard_product_id'] = oa[0]['standard_product_id']  # 标准ID

                oc = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=obj['store_name']).values('seller_id')
                if oc:
                    obj['seller_id'] = oc[0]['seller_id']
                else:
                    obj['seller_id'] = ''

                ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
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

                    # 实际的统计值，从订单列表获取
                    if obj['SKU_price_sum']:
                        obj['SKU_price_sum'] = round(float(obj['SKU_price_sum']), 2)  # 总进价
                    else:
                        obj['SKU_price_sum'] = 0

                    if obj['SKU_freight_sum']:
                        obj['SKU_freight_sum'] = round(float(obj['SKU_freight_sum']), 2)  # 总运费
                    else:
                        obj['SKU_freight_sum'] = 0

                    if obj['SKU_parts_price_sum']:
                        obj['SKU_parts_price_sum'] = round(float(obj['SKU_parts_price_sum']), 2)  # 总配件价
                    else:
                        obj['SKU_parts_price_sum'] = 0

                    if obj['SKU_parts_freight_sum']:
                        obj['SKU_parts_freight_sum'] = round(float(obj['SKU_parts_freight_sum']), 2)  # 总配件运费
                    else:
                        obj['SKU_parts_freight_sum'] = 0

                    if obj['SKU_buy_one_price_sum']:
                        obj['SKU_buy_one_price_sum'] = round(float(obj['SKU_buy_one_price_sum']), 2)  # 总买一得一进价
                    else:
                        obj['SKU_buy_one_price_sum'] = 0

                    if obj['SKU_buy_one_freight_sum']:
                        obj['SKU_buy_one_freight_sum'] = round(float(obj['SKU_buy_one_freight_sum']), 2)  # 总买一得一运费
                    else:
                        obj['SKU_buy_one_freight_sum'] = 0

                    if (obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum']):
                        if obj['upsells_amount2']:
                            obj['upsells_amount2'] = obj['upsells_amount2']
                        else:
                            obj['upsells_amount2'] = 0
                        obj['parts_prf'] = (float(obj['upsells_amount2']) * exchange_rate - (
                                obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum'])) / (
                                                   obj['SKU_parts_price_sum'] + obj['SKU_parts_freight_sum'])
                        obj['parts_prf'] = round(obj['parts_prf'] * 100, 2)
                    else:
                        obj['parts_prf'] = 0

                    obj['dabaochenben'] = 打包成本 * obj['paid_at']

                    obj['cost_of'] = round((obj['SKU_price_sum'] + obj['SKU_freight_sum'] + obj['SKU_parts_price_sum'] +
                                            obj['SKU_parts_freight_sum'] + obj['SKU_buy_one_price_sum'] + obj[
                                                'SKU_buy_one_freight_sum'] + obj['dabaochenben']), 2)  # 总成本

                    if obj['refunded_at_own']:
                        obj['cost_of'] = round((obj['cost_of'] - (obj['refunded_at_own'] * (float(obj['SKU_price'])))),2)  # 总成本
                    else:
                        obj['cost_of'] = obj['cost_of']

                    obj['Net_profit'] = round(((obj['disbursement_amount_Sum'] * exchange_rate) - obj['cost_of']),
                                              2)  # 毛利润(有自己主动退款)

                    if obj['paid_at']:
                        obj['Net_profit_avg'] = round((obj['Net_profit'] / obj['paid_at']), 2)  # 平均利润
                    else:
                        obj['Net_profit_avg'] = 0

                    if obj['cost_of']:
                        obj['profit_margin'] = round((obj['Net_profit'] / obj['cost_of']) * 100, 2)  # 利润率
                    else:
                        obj['profit_margin'] = 0

                    obj['dabaochenben'] = round(obj['dabaochenben'], 2) #打包成本

                    if obj['SKU_price'] and obj['HAI_SKU_freight']:
                        obj['suggest_buynows_price'] = round(((((float(obj['SKU_price']) + float(obj['HAI_SKU_freight'])) * 1.3  / exchange_rate) + 1.3) / 0.881) / 0.95, 2)  # 建议一口价



                    打包总成本 += obj['dabaochenben']
                    COSTF_OF += obj['cost_of']  # 店铺总成本
                    NET_PROFIT += obj['Net_profit']  # 店铺总利润
                    # obj['line_cost'] = round((float(obj['SKU_price']) + float(obj['SKU_freight'])), 2)  # 总成本
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

                    obj['profit_margin'] = '--'
                    obj['Net_profit_avg'] = '--'
                    obj['Net_profit'] = '--'
                    obj['cost_of'] = '--'
                    obj['dabaochenben'] = '--'
                    obj['suggest_buynows_price'] = '--'



                DIS_AMOUT1 += (obj['disbursement_amount1'] * obj['created_at'])  # 总成交价人命币
                DIS_AMOUT2 += (obj['disbursement_amount2'] * obj['created_at'])  # 总成交价 美元
                PAID_SUM += obj['paid_at']  # 店铺总订单

                REFUN_SUM_OWN += obj['refunded_at_own']  # 店铺总退货_自己
                REFUN_SUM_BUYER += obj['refunded_at_buyer']  # 店铺总退货_买家
                REFUN_SUM += obj['refunded_at']  # 店铺总退货

                if PAID_SUM:
                    PROFIT_REFUN_OWN = round(((REFUN_SUM_OWN / PAID_SUM) * 100), 2)  # 总退货率_自己
                else:
                    PROFIT_REFUN_OWN = 0

                if PAID_SUM:
                    PROFIT_REFUN_BUYER = round(((REFUN_SUM_BUYER / PAID_SUM) * 100), 2)  # 总退货率_买家
                else:
                    PROFIT_REFUN_BUYER = 0

                if PAID_SUM:
                    PROFIT_REFUN = round(((REFUN_SUM / PAID_SUM) * 100), 2)  # 总退货率
                else:
                    PROFIT_REFUN = 0


            打包总成本 = round(打包总成本, 2)  # 打包总成本
            COSTF_OF = round(COSTF_OF, 2)  # 店铺总成本
            NET_PROFIT = round(NET_PROFIT, 2)  # 店铺总利润

            if COSTF_OF:
                PROFIT_MARGIN = round((NET_PROFIT / COSTF_OF) * 100, 2)  # 利润率
            else:
                PROFIT_MARGIN = '0'

            EXCHANGE_RATE = exchange_rate

            context_all = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': [{
                # 统计数据
                'PAID_SUM': PAID_SUM,
                'REFUN_SUM_OWN': REFUN_SUM_OWN,
                'REFUN_SUM_BUYER': REFUN_SUM_BUYER,
                'REFUN_SUM': REFUN_SUM,
                'PROFIT_REFUN_OWN': PROFIT_REFUN_OWN,
                'PROFIT_REFUN_BUYER': PROFIT_REFUN_BUYER,
                'PROFIT_REFUN': PROFIT_REFUN,
                'COSTF_OF': COSTF_OF,
                'NET_PROFIT': NET_PROFIT,
                'PROFIT_MARGIN': PROFIT_MARGIN,

                '打包总成本': 打包总成本,
                'EXCHANGE_RATE': EXCHANGE_RATE,
                }]
            }
            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs1)
            }
            if table_number == 'table_number_sum':
                return HttpResponse(json.dumps(context_all, cls=CJsonEncoder))
            elif table_number == 'table_number_detail':
                return HttpResponse(json.dumps(context))
            return render(request, 'Tophatter/Buynow_orders_profitStatistics.html')
#一口价页面
def Buynow_page_orders(request):
    user_app.change_info(request, 'Buynow_page_orders')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            start_time = request.GET.get('start_time', '')  # 统计时间
            end_time = request.GET.get('end_time', '')  # 统计时间
            time_local = request.GET.get('time_local', '')  # 统计时间
            product_identifier = request.GET.get('product_identifier', '')  # 商品名称

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式
            table_number = request.GET.get('table_number', '')  # 表格序号

            if limit == '' and  page == '' and  table_number == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {'store_name_users':list(store_name_users)}
                return render(request, 'Tophatter/Buynow_page_orders.html',context0)

            if start_time == '':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
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

            start_time_combine = (datetime.datetime.now() - datetime.timedelta(hours=159)).date().strftime('%Y-%m-%d')
            end_time_combine = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')

            if store_name == '':
                store_name = 'all'

            if Sort_field == '':
                Sort_field = 'Impressions'

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
            objs1 = models_Tophatter.buynows_oders.objects.filter(USER_ID=USER_ID).filter(Q(time_hours_local_symbol=None) | Q(time_hours_local_symbol='yestoday')) \
                .filter(time_local__gte=start_time).filter(time_local__lte=end_time)
            if store_name != 'all':
                objs1 = objs1.filter(store_name=store_name)
            if product_identifier != '':
                objs1 = objs1.filter(identifier__contains=product_identifier)

            if table_number == 'table_number_detail':
                count_all = objs1.values('identifier').annotate(Impressions=Sum('Impressions')).count()
                objs1 = objs1.values('identifier').annotate(SKU=Max('identifier')
                                               , store_name=Max('store_name')
                                               , img_buynows=Max('img_buynows')
                                               , Impressions=Sum('Impressions')
                                               , Views=Sum('Views')
                                               , Orders=Sum('Orders')
                                               , Fees=Sum('Fees')
                                               , CPM=Sum('CPM')
                                               , save_time=Min('save_time')
                                               , Cost_per_Order=Sum('Cost_per_Order')).order_by(Sort_order+Sort_field)[page_star:page_end]
            elif  table_number == 'table_number_sum':
                objs1 = objs1.values('identifier').annotate(SKU=Max('identifier')
                                               , store_name=Max('store_name')
                                               , img_buynows=Max('img_buynows')
                                               , Impressions=Sum('Impressions')
                                               , Views=Sum('Views')
                                               , Orders=Sum('Orders')
                                               , Fees=Sum('Fees')
                                               , CPM=Sum('CPM')
                                               , save_time=Min('save_time')
                                               , Cost_per_Order=Sum('Cost_per_Order'))

            IMPRESSIONS = 0  # 总展示次数
            VIEWS = 0  # 总展示次数
            PAID_SUM_PAGE = 0  # 页面订单总数
            PAID_SUM = 0  # 订单总数
            FEES = 0  # 总广告费（$）
            FEES_2 = 0  # 总广告费(￥)
            CONVERSION_1 = 0  # 展示总转化率
            CONVERSION_2 = 0  # 展示总转化率
            EXCHANGE_RATE = 0  # 汇率
            SAVE_TIME = 0
            SAVE_TIME_UTC = 0

            for obj in objs1:
                SAVE_TIME = obj['save_time']
                SAVE_TIME_UTC = obj['save_time'] - datetime.timedelta(hours=15)

                objs2 = models_Tophatter.StoreSellData.objects.filter(product_identifier=obj['SKU']) \
                    .filter(canceled_at=None).filter(~Q(seller_fees_type_buy_nows=None)).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time)
                if store_name != 'all':
                    objs2 = objs2.filter(store_name=store_name)
                if product_identifier != '':
                    objs2 = objs2.filter(product_identifier=obj['SKU'])
                objs2 = objs2.values('product_internal_id').annotate(product_quantity=Sum('product_quantity'))

                if objs2:
                    obj['product_quantity'] = objs2[0]['product_quantity']
                else:
                    obj['product_quantity'] = 0

                oa = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=obj['SKU']).values('id').annotate(
                    primary_image=Max('primary_image', distinct=True),
                    standard_product_id=Max('standard_product_id', distinct=True))
                if oa:
                    obj['primary_image'] = oa[0]['primary_image']  # 主图
                    obj['standard_product_id'] = oa[0]['standard_product_id']  # 标准ID

                oc = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=obj['store_name']).values('seller_id')
                if oc:
                    obj['seller_id'] = oc[0]['seller_id']
                else:
                    obj['seller_id'] = ''

                IMPRESSIONS += float(obj['Impressions'])  # 总展示次数
                VIEWS += float(obj['Views'])  # 总展示次数
                FEES += float(obj['Fees'])  # 总广告费
                PAID_SUM_PAGE += float(obj['Orders'])  # 页面总订单
                PAID_SUM += float(obj['product_quantity'])  # 总订单

                if obj['Impressions']:
                    if float(obj['Impressions']) > 0:
                        obj['conversion_1'] = round(float(obj['product_quantity']) * 100 / float(obj['Impressions']), 2)
                    else:
                        obj['conversion_1'] = 0
                else:
                    obj['conversion_1'] = 0

                if obj['Views']:
                    if float(obj['Views']) > 0:
                        obj['conversion_2'] = round(float(obj['product_quantity']) * 100 / float(obj['Views']), 2)
                    else:
                        obj['conversion_2'] = 0
                else:
                    obj['conversion_2'] = 0

                obj['Impressions'] = round(float(obj['Impressions']))
                obj['Views'] = round(float(obj['Views']))
                obj['Orders'] = round(float(obj['Orders']))
                obj['product_quantity'] = round(float(obj['product_quantity']))
                obj['Fees'] = round(float(obj['Fees']),2)
                obj['CPM'] = round(float(obj['CPM']),2)
                obj['Cost_per_Order'] = round(float(obj['Cost_per_Order']),2)

            if IMPRESSIONS > 0:
                CONVERSION_1 = round(PAID_SUM * 100 / IMPRESSIONS, 2)  # 展示转化率
            else:
                CONVERSION_1 = 0
            if VIEWS > 0:
                CONVERSION_2 = round(PAID_SUM * 100 / VIEWS, 2)  # 浏览转化率
            else:
                CONVERSION_2 = 0
            IMPRESSIONS = int(IMPRESSIONS)  # 总展示次数
            VIEWS = int(VIEWS)  # 总展示次数
            PAID_SUM_PAGE = int(PAID_SUM_PAGE)  # 总展示次数
            PAID_SUM = int(PAID_SUM)  # 总展示次数
            FEES = round(FEES, 2)  # 总广告费
            FEES_2 = round(FEES*exchange_rate, 2)  # 总广告费
            EXCHANGE_RATE = exchange_rate

            context_all = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': [{
                    # 统计数据
                    'EXCHANGE_RATE': EXCHANGE_RATE,
                    'IMPRESSIONS': IMPRESSIONS,  # 总展示次数
                    'VIEWS': VIEWS,  # 总展示次数
                    'PAID_SUM_PAGE': PAID_SUM_PAGE,  # 页面总订单
                    'PAID_SUM': PAID_SUM,  # 总订单
                    'CONVERSION_1': CONVERSION_1,  # 展示转化率
                    'CONVERSION_2': CONVERSION_2,  # 浏览转化率
                    'SAVE_TIME': SAVE_TIME,  #
                    'SAVE_TIME_UTC': SAVE_TIME_UTC,  #
                    'FEES': FEES,  # 总广告费
                    'FEES_2': FEES_2,  # 总广告费
                }]
            }
            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs1)
            }
            if table_number == 'table_number_sum':
                return HttpResponse(json.dumps(context_all, cls=CJsonEncoder))
            elif table_number == 'table_number_detail':
                return HttpResponse(json.dumps(context, cls=CJsonEncoder))
            return render(request, 'Tophatter/Buynow_page_orders.html')
#批量退货
@csrf_exempt
def Refund_orders(request):
    user_app.change_info(request, 'Refund_orders')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET" or request.method == "POST":
        now = datetime.datetime.now()
        now_str = now.strftime('%Y%m%d_%H%M%S')
        if request.method == "GET":
            开始退货 = request.GET.get('开始退货', '')
            if 开始退货=='':
                return render(request, 'Tophatter/Refund_orders.html')

            if 开始退货 != '':
                filename_orders = request.GET.get('filename_orders', '')
                if 开始退货 == '开始退货':
                    try:
                        data_msg = {
                            'msg_1': '',
                            'msg_2': '',
                        }
                        a = 0
                        with open(filename_orders) as f:
                            reader = csv.reader(f)
                            for row in reader:
                                if row[0] != '店铺名':
                                    try:
                                        store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=row[0]).values_list('store_APIToken')[0][
                                            0]
                                        data_0 = {
                                            'access_token': store_APIToken,
                                            'order_id': int(row[1]),
                                            'type': 'full',
                                            'reason': str(row[2]),  # non_admin_buyer_address
                                        }
                                        subm = requests.post('https://tophatter.com/merchant_api/v1/orders/refund.json', data=data_0, timeout=30)
                                        print(subm.status_code)
                                        if subm.status_code == 200:
                                            a = a + 1
                                            data_msg['msg_1'] = str(a)
                                        else:
                                            data_msg['msg_2'] = data_msg['msg_2'] + row[0] + '-' + row[1] + '，'
                                    except Exception as e:
                                        print(e)
                                        data_msg['msg_2'] = data_msg['msg_2'] + row[0] + '-' + row[1] + '，'
                        return HttpResponse(json.dumps(data_msg))
                    except Exception as e:
                        data_msg_e = {'msg_e': str(e)}
                        return HttpResponse(json.dumps(data_msg_e))

        # 获取上传的文件，如果没有文件，则默认为None
        if request.method == "POST":
            File = request.FILES['file']
            if File is None :
                errmsg = '没有上传的文件！！！'
                context = {'status': 0,'msg': errmsg}
                return HttpResponse(json.dumps(context))
            else:
                from django.core.files.storage import FileSystemStorage
                try:
                    fs = FileSystemStorage()
                    filename_orders = fs.save('./static/user_files_directory/upload_file_refund_orders/'+ str(USER_ID) +'_'+ File.name[:-4] + now_str + File.name[-4:],File)
                    errmsg = '上传文件到服务器成功！！！'
                    context = {'status': 0,
                                'msg': errmsg,
                                'filename_orders':filename_orders}
                    return HttpResponse(json.dumps(context))
                except:
                    errmsg = '上传失败！！！'
                    context = {'status': 1,
                               'msg': errmsg}
                    return HttpResponse(json.dumps(context))
#订单详情
def orders_detail(request):
    user_app.change_info(request, 'All_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            start_time = request.GET.get('start_time', '')  # 统计时间
            end_time = request.GET.get('end_time', '')  # 统计时间
            订单ID = request.GET.get('订单ID', '')  # 订单ID
            time_local = request.GET.get('time_local', '')  # 时间段
            订单状态 = request.GET.get('订单状态', '')  # 订单状态
            product_identifier = request.GET.get('product_identifier', '')  # 商品名称
            product_type = request.GET.get('product_type', '')  # 订单类型
            related_order_ids = request.GET.get('related_order_ids', '') #关系订单
            service_type = request.GET.get('service_type', '') #服务类型
            input_order_type = request.GET.get('input_order_type', '') #已回款订单
            承运商 = request.GET.get('承运商', '')

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

            if start_time == '':
                start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
            if end_time == '':
                end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')

            if limit == '' and  page == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {
                            'store_name_users':list(store_name_users),
                            'time_local': time_local,  # 时间段
                            'start_time' : start_time,  # 统计时间
                            'end_time' : end_time,  # 统计时间
                            'product_identifier' : product_identifier,  # 商品名称
                            'product_type' : product_type,  # 订单类型
                            'related_order_ids' : related_order_ids,  # 关系订单
                            'service_type' : service_type,  # 服务类型
                            '承运商' : 承运商
                            }
                return render(request, 'Tophatter/orders_detail.html',context0)

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

            if 订单状态 == '':
                订单状态 = 'all'

            if service_type == '':
                service_type = '全部订单'
            if service_type == '全程追踪':
                service_type = 'full_tracking'
            if service_type == '部分追踪':
                service_type = 'partial_tracking'
            if service_type == '没有最后一英里追踪':
                service_type = 'no_last_mile_tracking'

            if input_order_type == '':
                input_order_type = '全部订单'

            if 承运商 == '':
                承运商 = '全部订单'


            if Sort_field == '':
                Sort_field = 'created_at'

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
                objs = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time)
                if store_name != 'all':
                    objs = objs.filter(store_name=store_name)
                if 订单ID != '':
                    objs = objs.filter(order_id=订单ID)
                if product_identifier != '':
                    objs = objs.filter(product_identifier__contains=product_identifier)
                if product_type == '一口价':
                    objs = objs.filter(~Q(seller_fees_type_buy_nows=None))
                if product_type == '竞拍价':
                    objs = objs.filter(seller_fees_type_buy_nows=None)
                if 订单状态 != 'all':
                    objs = objs.filter(status=订单状态)


                if related_order_ids == '非关系订单':
                    objs = objs.filter(Q(related_order_ids=None) & Q(related_order_ids='[]'))
                if related_order_ids == '关系订单':
                    objs = objs.filter(~Q(related_order_ids=None) & ~Q(related_order_ids='[]'))

                if service_type != '全部订单':
                    objs = objs.filter(service_type=service_type)

                if input_order_type == '有状态订单':
                    objs = objs.filter(~Q(ht_物流状态=None))
                elif input_order_type != '有状态订单' and input_order_type != '全部订单':
                    objs = objs.filter(ht_物流状态=input_order_type)

                if 承运商 == '有承运商订单':
                    objs = objs.filter(~Q(carrier=None))
                elif 承运商 == '无承运商订单':
                    objs = objs.filter(carrier=None)
                elif 承运商 != '全部订单' and 承运商 != '有承运商订单' and 承运商 != '无承运商订单':
                    objs = objs.filter(carrier=承运商)

                count_all = objs.values('order_id').count()
                objs = objs.values('order_id', 'store_name', 'status', 'carrier', 'tracking_number', 'product_name','created_at',
                                   'product_identifier', 'product_internal_id', 'customer_id', 'customer_name', 'country',
                                   'city', 'state', 'disbursement_amount', 'seller_fees_amount', 'seller_fees_amount_sfb',
                                   'upsells_type_description1',
                                   'upsells_amount1', 'upsells_description1', 'upsells_type_description2',
                                   'upsells_amount2', 'upsells_description2', 'product_quantity',
                                   'SKU_price', 'SKU_parts_price', 'SKU_freight', 'SKU_parts_freight',
                                   'seller_fees_type_buy_nows', 'related_order_ids', 'service_type', 'ht_物流状态',
                                   'refunded_at_own', 'refunded_at_buyer').order_by(Sort_order+Sort_field)[page_star:page_end]
                for obj in objs:
                    oa = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=obj['product_identifier']).values('id').annotate(
                        primary_image=Max('primary_image', distinct=True))
                    if oa:
                        obj['primary_image'] = oa[0]['primary_image']  # 主图

                    if obj['related_order_ids'] == None or obj['related_order_ids'] == '[]':  # 关系订单
                        obj['related_order_ids'] = ''
                    else:
                        obj['related_order_ids'] = obj['related_order_ids'][1:-1].split(',')

                    if obj['seller_fees_type_buy_nows'] == None:
                        obj['seller_fees_type_buy_nows'] = ''
                    if obj['seller_fees_amount_sfb'] == None:
                        obj['seller_fees_amount_sfb'] = ''

                    if obj['upsells_type_description1'] == None:
                        obj['upsells_type_description1'] = ''
                    elif obj['upsells_type_description1'] != None:
                        obj['upsells_type_description1'] = '买送一'
                    if obj['upsells_amount1'] == None:
                        obj['upsells_amount1'] = ''
                    if obj['upsells_type_description2'] == None:
                        obj['upsells_type_description2'] = ''
                    elif obj['upsells_type_description2'] != None:
                        obj['upsells_type_description2'] = '配件'
                    if obj['upsells_amount2'] == None:
                        obj['upsells_amount2'] = ''

                    if obj['refunded_at_own']:
                        obj['profit'] = round((float(obj['disbursement_amount']) * exchange_rate), 2)
                    else:
                        obj['profit'] = round((float(obj['disbursement_amount']) * exchange_rate - (
                                float(obj['SKU_price']) + float(obj['SKU_freight']) + float(obj['SKU_parts_price']) + float(
                            obj['SKU_parts_freight']))), 2)

                    ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['product_identifier']).values('id').annotate(
                        SKU_price_or=Max('SKU_price', distinct=True)
                        , SKU_parts_price_or=Max('SKU_parts_price', distinct=True)

                        , SKU_weight_or=Max('SKU_weight', distinct=True)  # -------
                        , SKU_parts_weight_or=Max('SKU_parts_weight', distinct=True)  # -------
                        , SKU_variety_or=Max('SKU_variety', distinct=True)
                        , HAI_SKU_freight_or=Max('HAI_SKU_freight', distinct=True))  # -------
                    if ob:
                        obj['SKU_price_or'] = ob[0]['SKU_price_or']  # 单价
                        obj['SKU_parts_price_or'] = ob[0]['SKU_parts_price_or']  # 配件价
                        obj['SKU_weight_or'] = ob[0]['SKU_weight_or']  # 单重量
                        obj['SKU_parts_weight_or'] = ob[0]['SKU_parts_weight_or']  # 单配件重量
                        obj['SKU_variety_or'] = ob[0]['SKU_variety_or']  # 单种类
                        obj['HAI_SKU_freight_or'] = ob[0]['HAI_SKU_freight_or']  #

                        if obj['SKU_price_or']:
                            obj['SKU_price_or'] = obj['SKU_price_or']
                        else:
                            obj['SKU_price_or'] = 0

                        if obj['SKU_parts_price_or']:
                            obj['SKU_parts_price_or'] = obj['SKU_parts_price_or']
                        else:
                            obj['SKU_parts_price_or'] = 0

                        if obj['SKU_weight_or']:
                            obj['SKU_weight_or'] = obj['SKU_weight_or']
                        else:
                            obj['SKU_weight_or'] = 0

                        if obj['SKU_parts_weight_or']:
                            obj['SKU_parts_weight_or'] = obj['SKU_parts_weight_or']
                        else:
                            obj['SKU_parts_weight_or'] = 0

                        if obj['SKU_variety_or']:
                            obj['SKU_variety'] = obj['SKU_variety_or']
                        else:
                            obj['SKU_variety_or'] = ''

                        if obj['HAI_SKU_freight_or']:
                            obj['HAI_SKU_freight_or'] = obj['HAI_SKU_freight_or']
                        else:
                            obj['HAI_SKU_freight_or'] = 0
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

                        obj['profit_margin'] = '--'
                        obj['Net_profit_avg'] = '--'
                        obj['Net_profit'] = '--'
                        obj['cost_of'] = '--'

            except Exception as e:
                print(e)

            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs),
            }
            return HttpResponse(json.dumps(context, cls=CJsonEncoder))
        return render(request, 'Tophatter/orders_detail.html')
# 订单展示
def orders_to_show(request):
    user_app.change_info(request, 'All_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            tubiao_type = request.GET.get('tubiao_type', '')  # 图表类型
            if tubiao_type == 'fenshi' or tubiao_type == 'fenshi-sum' or tubiao_type == 'riqi' or tubiao_type == 'riqi-sum' or tubiao_type == 'dianpu':
                store_name = request.GET.get('store_name', '')  # 店铺名
                start_time = request.GET.get('start_time', '')  # 统计时间
                end_time = request.GET.get('end_time', '')  # 统计时间
                time_local = request.GET.get('time_local', '')  # 统计时间
                product_identifier = request.GET.get('product_identifier', '')  # 商品名称
                product_type = request.GET.get('product_type', '')  # 订单类型


                if start_time == '':
                    start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
                if end_time == '':
                    end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')

                if product_type=='':
                    product_type='全部订单'
                if store_name == '':
                    store_name = 'all'

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
                    start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
                    end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                if time_local == 'last_30_days':
                    start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=30)).date().strftime('%Y-%m-%d')
                    end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                if time_local == 'last_60_days':
                    start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=60)).date().strftime('%Y-%m-%d')
                    end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                if time_local == 'last_90_days':
                    start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=90)).date().strftime('%Y-%m-%d')
                    end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                if time_local == 'all_time':
                    start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(days=600)).date().strftime('%Y-%m-%d')
                    end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')

                if tubiao_type == 'riqi' or tubiao_type == 'riqi-sum':
                    #总图表日期数据
                    if tubiao_type == 'riqi':
                        objs_charts = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time)
                        objs_chart_SFBs = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None).filter(~Q(seller_fees_amount_sfb=None)).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time)
                    else:
                        objs_charts = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None)
                        objs_chart_SFBs = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None).filter(~Q(seller_fees_amount_sfb=None))

                    if store_name != 'all':
                        objs_charts = objs_charts.filter(store_name=store_name)
                        objs_chart_SFBs = objs_chart_SFBs.filter(store_name=store_name)

                    if product_identifier != '':
                        objs_charts = objs_charts.filter(product_identifier__contains=product_identifier)
                        objs_chart_SFBs = objs_chart_SFBs.filter(product_identifier__contains=product_identifier)

                    if product_type == '一口价':
                        objs_charts = objs_charts.filter(~Q(seller_fees_type_buy_nows=None))
                        objs_chart_SFBs = objs_chart_SFBs.filter(~Q(seller_fees_type_buy_nows=None))

                    if product_type == '竞拍价':
                        objs_charts = objs_charts.filter(seller_fees_type_buy_nows=None)
                        objs_chart_SFBs = objs_chart_SFBs.filter(seller_fees_type_buy_nows=None)

                    objs_charts = objs_charts.values('data_time_created_at').annotate(amount=Count('order_id', distinct=True)
                                                          ,status_refunded=Count('status_refunded')
                                                          ,disbursement_amount=Avg('disbursement_amount')).order_by('data_time_created_at')
                    objs_chart_SFBs = objs_chart_SFBs.values('data_time_created_at').annotate(SFB_AVG=Avg('seller_fees_amount_sfb')) \
                                                     .order_by('data_time_created_at')



                    index_amount_0 = [0,0]
                    index_refunded_0 = [0,0]
                    index_SFB_0 = [0, 0]
                    index_profit_0 = [0, 0]
                    index_amount = []
                    index_refunded = []
                    index_SFB = []
                    index_profit = []
                    for objs_chart in objs_charts:
                        objs_chart['index_amount_0']=[0,0]
                        objs_chart['index_refunded_0']=[0,0]
                        objs_chart['index_profit_0'] = [0, 0]
                        this_date = datetime.datetime.strptime(str(objs_chart['data_time_created_at']), '%Y-%m-%d')
                        this_date = time.mktime(this_date.timetuple())

                        index_amount_0[0] = this_date * 1000
                        index_amount_0[1] = objs_chart['amount']
                        objs_chart['index_amount_0'][0] = index_amount_0[0]
                        objs_chart['index_amount_0'][1] = index_amount_0[1]
                        index_amount.append(objs_chart['index_amount_0'])

                        index_refunded_0[0] = this_date * 1000
                        index_refunded_0[1] = objs_chart['status_refunded']
                        objs_chart['index_refunded_0'][0] = index_refunded_0[0]
                        objs_chart['index_refunded_0'][1] = index_refunded_0[1]
                        index_refunded.append(objs_chart['index_refunded_0'])

                        index_profit_0[0] = this_date * 1000
                        index_profit_0[1] = objs_chart['disbursement_amount']
                        objs_chart['index_profit_0'][0] = index_profit_0[0]
                        objs_chart['index_profit_0'][1] = round(index_profit_0[1],2)
                        index_profit.append(objs_chart['index_profit_0'])
                    for objs_chart_SFB in objs_chart_SFBs:
                        objs_chart_SFB['index_SFB_0'] = [0, 0]
                        this_date = datetime.datetime.strptime(str(objs_chart_SFB['data_time_created_at']), '%Y-%m-%d')
                        this_date = time.mktime(this_date.timetuple())

                        index_SFB_0[0] = this_date * 1000
                        index_SFB_0[1] = objs_chart_SFB['SFB_AVG']
                        objs_chart_SFB['index_SFB_0'][0] = index_SFB_0[0]
                        objs_chart_SFB['index_SFB_0'][1] = round(index_SFB_0[1],2)
                        index_SFB.append(objs_chart_SFB['index_SFB_0'])
                    context1 = {
                        # 日期图表
                        'index_amount': index_amount,
                        'index_refunded': index_refunded,
                        'index_SFB': index_SFB,
                        'index_profit': index_profit,
                    }
                    return HttpResponse(json.dumps(context1))

                if tubiao_type == 'fenshi' or tubiao_type == 'fenshi-sum':
                    # 图表分时数据
                    times_charts = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time)
                    times_chart_SFBs = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None).filter(~Q(seller_fees_amount_sfb=None)).filter(data_time_created_at__gte=start_time).filter(data_time_created_at__lte=end_time)
                    if store_name != 'all':
                        times_charts = times_charts.filter(store_name=store_name)
                        times_chart_SFBs = times_chart_SFBs.filter(store_name=store_name)
                    if product_identifier != '':
                        times_charts = times_charts.filter(product_identifier__contains=product_identifier)
                        times_chart_SFBs = times_chart_SFBs.filter(product_identifier__contains=product_identifier)
                    if product_type == '一口价':
                        times_charts = times_charts.filter(~Q(seller_fees_type_buy_nows=None))
                        times_chart_SFBs = times_chart_SFBs.filter(~Q(seller_fees_type_buy_nows=None))
                    if product_type == '竞拍价':
                        times_charts = times_charts.filter(seller_fees_type_buy_nows=None)
                        times_chart_SFBs = times_chart_SFBs.filter(seller_fees_type_buy_nows=None)
                    times_charts = times_charts.values('hours_time_created_at').annotate(amount=Count('order_id', distinct=True)\
                                                                      , status_refunded=Count('status_refunded', distinct=True)\
                                                                      , disbursement_amount=Avg('disbursement_amount',distinct=True)).order_by('hours_time_created_at')
                    times_chart_SFBs = times_chart_SFBs.values('hours_time_created_at').annotate(SFB_AVG=Avg('seller_fees_amount_sfb', distinct=True)) \
                            .order_by('hours_time_created_at')

                    times_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
                    times_refunded= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
                    times_profit= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
                    times_SFB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
                    # times_profit_margin = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

                    times_amount_A = [0, 0, 0, 0, 0, 0, 0, 0]
                    times_refunded_A = [0, 0, 0, 0, 0, 0, 0, 0]
                    times_profit_A = [0, 0, 0, 0, 0, 0, 0, 0]
                    times_SFB_A = [0, 0, 0, 0, 0, 0, 0, 0]
                    # times_profit_margin_A = [0, 0, 0, 0, 0, 0, 0, 0]
                    for times_chart in times_charts:
                        x = round(float(times_chart['hours_time_created_at']))
                        times_amount[x] = times_chart['amount']
                        times_refunded[x] = times_chart['status_refunded']
                        times_profit[x] = round(times_chart['disbursement_amount'], 2)
                    for times_chart_SFB in times_chart_SFBs:
                        x = round(float(times_chart_SFB['hours_time_created_at']))
                        times_SFB[x] = round(times_chart_SFB['SFB_AVG'], 2)
                    for n in range(0,8):
                        n = int(n)
                        times_amount_A[n] = times_amount[3 * n] + times_amount[(3 * n) + 1] + times_amount[(3 * n) + 2]
                        times_refunded_A[n] = times_refunded[3 * n] + times_refunded[(3 * n) + 1] + times_refunded[(3 * n) + 2]
                        times_profit_A[n] = round(
                            (times_profit[3 * n] + times_profit[(3 * n) + 1] + times_profit[(3 * n) + 2]) / 3, 2)
                        times_SFB_A[n] = round((times_SFB[3 * n] + times_SFB[(3 * n) + 1] + times_SFB[(3 * n) + 2]) / 3, 2)
                        # times_profit_margin_A[n] = times_amount[3 * n] + times_amount[(3 * n) + 1] + times_amount[(3 * n) + 2]
                    context2 = {
                        # 分时图表
                        'times_amount_A': times_amount_A,
                        'times_refunded_A': times_refunded_A,
                        'times_profit_A': times_profit_A,
                        'times_SFB_A': times_SFB_A,
                    }
                    return HttpResponse(json.dumps(context2))

                if tubiao_type == 'dianpu':
                    # 一口价 统计店铺
                    objs_charts = models_Tophatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(canceled_at=None).filter(data_time_created_at__gte=start_time).filter(
                        data_time_created_at__lte=end_time)
                    if product_type == '一口价':
                        objs_charts = objs_charts.filter(~Q(seller_fees_type_buy_nows=None))
                    objs_charts = objs_charts.values('store_name').annotate( amount=Count('order_id', distinct=True)
                                                                             , status_refunded=Count('status_refunded')
                                                                             , disbursement_amount=Avg('disbursement_amount')).order_by('store_name')

                    index_amount = []
                    index_refunded = []
                    index_SFB = []
                    index_profit = []
                    store_name_all = []
                    for objs_chart in objs_charts:
                        index_amount.append(objs_chart['amount'])
                        index_refunded.append(objs_chart['status_refunded'])
                        objs_chart['disbursement_amount'] = round(objs_chart['disbursement_amount'], 2)
                        index_profit.append(objs_chart['disbursement_amount'])
                        store_name_all.append(objs_chart['store_name'])

                    context1 = {
                        # 日期图表
                        'store_name':store_name_all,
                        'index_amount': index_amount,
                        'index_refunded': index_refunded,
                        'index_profit': index_profit,
                    }
                    return HttpResponse(json.dumps(context1))

            if tubiao_type == 'paimai-fenshi-sum' or tubiao_type == 'paimai-fenshi':
                time_today = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d')
                time_yestoday = (datetime.datetime.now() - datetime.timedelta(hours=39)).date().strftime('%Y-%m-%d')
                store_name = request.GET.get('store_name', '')  # 店铺名
                product_identifier = request.GET.get('product_identifier', '')  # 商品名称   .filter(identifier=obj['SKU'])

                if store_name=='':
                    store_name='all'

                obj_ALL = {'SKU': 'AAA'}
                objs6s = models_Tophatter.Performance_hours_time.objects.filter(USER_ID=USER_ID).filter(time_local=time_today)
                objs7s = models_Tophatter.Performance_hours_time.objects.filter(USER_ID=USER_ID).filter(time_local=time_yestoday)
                if store_name != 'all':
                    objs6s = objs6s.filter(store_name=store_name)
                    objs7s = objs7s.filter(store_name=store_name)

                if product_identifier != '':
                    objs6s = objs6s.filter(identifier=product_identifier)
                    objs7s = objs7s.filter(identifier=product_identifier)

                objs6s = objs6s.filter(~Q(time_hours_local=None)) \
                    .values('time_hours_local_symbol').annotate(schedules=Sum('schedules', distinct=True)
                                                                , orders=Sum('orders', distinct=True)
                                                                , revenue=Sum('revenue', distinct=True)
                                                                , fees=Sum('fees', distinct=True)
                                                                , scheduling_fees=Sum('scheduling_fees',distinct=True)).order_by( 'time_hours_local_symbol')
                objs7s = objs7s.filter(~Q(time_hours_local=None)) \
                    .values('time_hours_local_symbol').annotate(schedules=Sum('schedules', distinct=True)
                                                                , orders=Sum('orders', distinct=True)
                                                                , revenue=Sum('revenue', distinct=True)
                                                                , fees=Sum('fees', distinct=True)
                                                                , scheduling_fees=Sum('scheduling_fees',distinct=True)).order_by('time_hours_local_symbol')
                obj_ALL['line_cost'] = 0  # 图表

                obj_ALL['today_03_orders'] = 0
                obj_ALL['today_03_revenue'] = 0
                obj_ALL['today_03_CloseRate'] = 0
                obj_ALL['today_03_SFB'] = 0
                obj_ALL['today_03_profit'] = 0

                obj_ALL['today_06_orders'] = 0
                obj_ALL['today_06_revenue'] = 0
                obj_ALL['today_06_CloseRate'] = 0
                obj_ALL['today_06_SFB'] = 0
                obj_ALL['today_06_profit'] = 0

                obj_ALL['today_09_orders'] = 0
                obj_ALL['today_09_revenue'] = 0
                obj_ALL['today_09_CloseRate'] = 0
                obj_ALL['today_09_SFB'] = 0
                obj_ALL['today_09_profit'] = 0

                obj_ALL['today_12_orders'] = 0
                obj_ALL['today_12_revenue'] = 0
                obj_ALL['today_12_CloseRate'] = 0
                obj_ALL['today_12_SFB'] = 0
                obj_ALL['today_12_profit'] = 0

                obj_ALL['today_15_orders'] = 0
                obj_ALL['today_15_revenue'] = 0
                obj_ALL['today_15_CloseRate'] = 0
                obj_ALL['today_15_SFB'] = 0
                obj_ALL['today_15_profit'] = 0

                obj_ALL['today_18_orders'] = 0
                obj_ALL['today_18_revenue'] = 0
                obj_ALL['today_18_CloseRate'] = 0
                obj_ALL['today_18_SFB'] = 0
                obj_ALL['today_18_profit'] = 0

                obj_ALL['today_21_orders'] = 0
                obj_ALL['today_21_revenue'] = 0
                obj_ALL['today_21_CloseRate'] = 0
                obj_ALL['today_21_SFB'] = 0
                obj_ALL['today_21_profit'] = 0

                obj_ALL['today_23_orders'] = 0
                obj_ALL['today_23_revenue'] = 0
                obj_ALL['today_23_CloseRate'] = 0
                obj_ALL['today_23_SFB'] = 0
                obj_ALL['today_23_profit'] = 0
                aa4 = 0
                aa44 = 0
                cc4 = 0
                dd4 = 0
                ee4 = 0
                ee44 = 0

                if objs6s:
                    for objs6 in objs6s:
                        a = objs6['time_hours_local_symbol']

                        aa44 = objs6['orders']  # a 单量
                        obj_ALL['today_' + a + '_orders'] = round((aa44 - aa4), 2)
                        aa4 = aa44

                        objs6['schedules_index'] = objs6['schedules'] - cc4
                        objs6['scheduling_fees_index'] = objs6['scheduling_fees'] - dd4
                        if objs6['schedules_index']:
                            obj_ALL['today_' + a + '_CloseRate'] = round(
                                ((float(obj_ALL['today_' + a + '_orders']) / float(objs6['schedules_index'])) * 100),2)  # c 成交率
                            obj_ALL['today_' + a + '_SFB'] = round(
                                (float(objs6['scheduling_fees_index']) / float(objs6['schedules_index'])), 2)  # d 均SFB
                        cc4 = objs6['schedules']
                        dd4 = objs6['scheduling_fees']

                        objs6['line_cost_sum'] = (obj_ALL['today_' + a + '_orders'] * obj_ALL[
                            'line_cost']) / exchange_rate  # 总花费
                        objs6['revenue_index'] = objs6['revenue'] - ee4
                        objs6['fees_index'] = objs6['fees'] - ee44
                        if objs6['line_cost_sum']:  # e 利润率
                            obj_ALL['today_' + a + '_profit'] = round((((float(objs6['revenue_index']) - float(
                                objs6['fees_index'])) - float(objs6['line_cost_sum'])) / float(objs6['line_cost_sum'])) * 100, 2)
                        if obj_ALL['today_' + a + '_orders']:  # b 均到手价
                            obj_ALL['today_' + a + '_revenue'] = round(((float(objs6['revenue_index']) - float(
                                objs6['fees_index'])) / float(obj_ALL['today_' + a + '_orders'])), 2)
                        ee4 = objs6['revenue']
                        ee44 = objs6['fees']

                obj_ALL['yestoday_03_orders'] = 0
                obj_ALL['yestoday_03_revenue'] = 0
                obj_ALL['yestoday_03_CloseRate'] = 0
                obj_ALL['yestoday_03_SFB'] = 0
                obj_ALL['yestoday_03_profit'] = 0

                obj_ALL['yestoday_06_orders'] = 0
                obj_ALL['yestoday_06_revenue'] = 0
                obj_ALL['yestoday_06_CloseRate'] = 0
                obj_ALL['yestoday_06_SFB'] = 0
                obj_ALL['yestoday_06_profit'] = 0

                obj_ALL['yestoday_09_orders'] = 0
                obj_ALL['yestoday_09_revenue'] = 0
                obj_ALL['yestoday_09_CloseRate'] = 0
                obj_ALL['yestoday_09_SFB'] = 0
                obj_ALL['yestoday_09_profit'] = 0

                obj_ALL['yestoday_12_orders'] = 0
                obj_ALL['yestoday_12_revenue'] = 0
                obj_ALL['yestoday_12_CloseRate'] = 0
                obj_ALL['yestoday_12_SFB'] = 0
                obj_ALL['yestoday_12_profit'] = 0

                obj_ALL['yestoday_15_orders'] = 0
                obj_ALL['yestoday_15_revenue'] = 0
                obj_ALL['yestoday_15_CloseRate'] = 0
                obj_ALL['yestoday_15_SFB'] = 0
                obj_ALL['yestoday_15_profit'] = 0

                obj_ALL['yestoday_18_orders'] = 0
                obj_ALL['yestoday_18_revenue'] = 0
                obj_ALL['yestoday_18_CloseRate'] = 0
                obj_ALL['yestoday_18_SFB'] = 0
                obj_ALL['yestoday_18_profit'] = 0

                obj_ALL['yestoday_21_orders'] = 0
                obj_ALL['yestoday_21_revenue'] = 0
                obj_ALL['yestoday_21_CloseRate'] = 0
                obj_ALL['yestoday_21_SFB'] = 0
                obj_ALL['yestoday_21_profit'] = 0

                obj_ALL['yestoday_23_orders'] = 0
                obj_ALL['yestoday_23_revenue'] = 0
                obj_ALL['yestoday_23_CloseRate'] = 0
                obj_ALL['yestoday_23_SFB'] = 0
                obj_ALL['yestoday_23_profit'] = 0
                aa5 = 0
                aa55 = 0
                cc5 = 0
                dd5 = 0
                ee5 = 0
                ee55 = 0

                if objs7s:
                    for objs7 in objs7s:
                        a = objs7['time_hours_local_symbol']

                        aa55 = objs7['orders']  # a 单量
                        obj_ALL['yestoday_' + a + '_orders'] = round((aa55 - aa5), 2)
                        aa5 = aa55

                        objs7['schedules_index'] = objs7['schedules'] - cc5
                        objs7['scheduling_fees_index'] = objs7['scheduling_fees'] - dd5
                        if objs7['schedules_index']:
                            obj_ALL['yestoday_' + a + '_CloseRate'] = round(
                                ((float(obj_ALL['yestoday_' + a + '_orders']) / float(objs7['schedules_index'])) * 100),2)  # c 成交率
                            obj_ALL['yestoday_' + a + '_SFB'] = round(
                                (float(objs7['scheduling_fees_index']) / float(objs7['schedules_index'])), 2)  # d 均SFB
                        cc5 = objs7['schedules']
                        dd5 = objs7['scheduling_fees']

                        objs7['line_cost_sum'] = (obj_ALL['yestoday_' + a + '_orders'] * obj_ALL[
                            'line_cost']) / exchange_rate  # 总花费
                        objs7['revenue_index'] = objs7['revenue'] - ee5
                        objs7['fees_index'] = objs7['fees'] - ee55
                        if objs7['line_cost_sum']:  # e 利润率
                            obj_ALL['yestoday_' + a + '_profit'] = round((((float(objs7['revenue_index']) - float(
                                objs7['fees_index'])) - float(objs7['line_cost_sum'])) / float(
                                objs7['line_cost_sum'])) * 100, 2)
                        if obj_ALL['yestoday_' + a + '_orders']:  # b 均到手价
                            obj_ALL['yestoday_' + a + '_revenue'] = round(((float(objs7['revenue_index']) - float(
                                objs7['fees_index'])) / float(obj_ALL['yestoday_' + a + '_orders'])), 2)
                        ee5 = objs7['revenue']
                        ee55 = objs7['fees']
                context3 = {
                    # 分时图表
                    'obj_ALL': obj_ALL,}
                return HttpResponse(json.dumps(context3))


#Top 所有商品
def Top_all_products(request):
    user_app.change_info(request, 'All_orders_profitStatistics')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            FIG = request.GET.get('FIG', '')
            if FIG == 'FIG_CPM':
                CPM = request.GET.get('CPM', '')
                checkStatus = request.GET.get('checkStatus', '')
                checkStatus = literal_eval(checkStatus)
                if checkStatus == '':
                    data_msg_e = {'msg_e': '请选择要上传的产品'}
                    return HttpResponse(json.dumps(data_msg_e))
                if CPM == '' :
                    data_msg_e = {'msg_e': '请选择CPM参数'}
                    return HttpResponse(json.dumps(data_msg_e))
                # 上传数据到店铺
                try:
                    errmsg_1 = ''
                    errmsg_2 = ''
                    data_msg = {'msg_1': '无', 'msg_2': '无', }
                    for internal_id in checkStatus:
                        if FIG == 'FIG_CPM':
                            store_name = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(internal_id=int(internal_id)).values_list('store_name')[0][0]
                            store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]
                            # print(store_name, store_APIToken)
                            # 店铺模板
                            internal_id = int(internal_id)  # Product Unique ID
                            campaign_name = CPM  # campaign_name
                            data = {
                                'access_token': store_APIToken,  # '2f9a6837ddb548932118fb57b625f3b3',  # 实验账号
                                'internal_id': internal_id,
                                'campaign_name': campaign_name
                            }
                            try:
                                subm = requests.post('https://tophatter.com/merchant_api/v1/products/update.json',data=data, timeout=30)
                                print("status code:", subm.status_code, store_name)
                                if subm.status_code == 200:
                                    # 获取更新完的产品信息
                                    errmsg_1 = errmsg_1 + str(internal_id) + '，'
                                    try:
                                        models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(internal_id=internal_id).update(campaign_name=campaign_name, updated_at=datetime.datetime.now())
                                        # print(store_name + '商品数据保存 success')
                                    except Exception as e:
                                        print(e)
                                        print('商品数据替换  faile')
                                else:
                                    errmsg_2 = errmsg_2 + str(internal_id) + '，'
                            except Exception as e:
                                print(e)
                                errmsg_2 = errmsg_2 + str(internal_id) + '，'
                        else:
                            data_msg_e = {'msg_e': '没有需要上传的产品'}
                            return HttpResponse(json.dumps(data_msg_e))
                    data_msg['msg_1'] = errmsg_1
                    data_msg['msg_2'] = errmsg_2
                    return HttpResponse(json.dumps(data_msg))
                except Exception as e:
                    data_msg_e = {'msg_e': str(e)}
                    return HttpResponse(json.dumps(data_msg_e))



            store_name = request.GET.get('store_name', '')  # 店铺名
            colect_pruduct = request.GET.get('colect_pruduct', '')  # 是否收藏
            status_pruduct = request.GET.get('status_pruduct', '')  # 订单状态
            product_identifier = request.GET.get('product_identifier', '')  # SKU  1
            CPM_SELECT = request.GET.get('CPM_SELECT', '')  # CPM选择   1

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

            if limit == '' and  page == '':
                campaign_listes = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(Q(status='Active')|Q(status='active')).values('name').distinct().order_by('name')
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {
                            'store_name_users':list(store_name_users),
                            'campaign_listes': list(campaign_listes),
                            }
                return render(request, 'Tophatter/Top_all_products.html',context0)

            if store_name == '':
                store_name = 'all'
            if colect_pruduct == '':
                colect_pruduct = '所有商品'
            if status_pruduct == '':
                status_pruduct = 'all'
            if CPM_SELECT == '':
                CPM_SELECT = '---请选择---'

            if Sort_field == '':
                Sort_field = 'internal_id'

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
                objs = models_Tophatter.Products.objects.filter(USER_ID=USER_ID)
                if store_name != 'all':
                    objs = objs.filter(store_name=store_name)
                if colect_pruduct == '未收藏商品':
                    objs = objs.filter(user_collect=None)
                elif colect_pruduct == '收藏商品':
                    objs = objs.filter(user_collect='是')

                if status_pruduct != 'all':
                    objs = objs.filter(status=status_pruduct)

                if CPM_SELECT != '---请选择---':
                    objs = objs.filter(campaign_name=CPM_SELECT)

                if product_identifier != '':
                    objs = objs.filter(identifier__contains=product_identifier)
                count_all = objs.values('identifier').count()
                objs = objs.values('identifier', 'status', 'store_name', 'primary_image', 'scheduling_fee_bid', 'retail_price','minimum_bid_amount',\
                                   'reserve_price', 'shipping_price', 'cost_basis', 'ratings_average', 'ratings_count', \
                                   'user_collect', 'category', 'title', 'description', 'condition', 'all_images', \
                                   'created_at', 'updated_at', 'internal_id', 'standard_product_id', 'campaign_name', 'buy_now_price').order_by(Sort_order+Sort_field)[page_star:page_end]

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
                    if str(obj['campaign_name']) == 'None':
                        obj['campaign_name'] = ''

                    obj['SKU_freight'] = 0
                    obj['imgs'] = []
                    ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['identifier']).values('id').annotate(
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

                        obj['profit_margin'] = '--'
                        obj['Net_profit_avg'] = '--'
                        obj['Net_profit'] = '--'
                        obj['cost_of'] = '--'

                    for img in literal_eval(obj['all_images']):
                        obj['imgs'].append(img['original'])

            except Exception as e:
                print(e)

            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs),
            }
            return HttpResponse(json.dumps(context, cls=CJsonEncoder))
        return render(request, 'Tophatter/Top_all_products.html')
#更新商品信息
def Top_products_update(request):
    user_app.change_info(request, 'uploading_one')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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

                campaign_listes = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(Q(status='Active')|Q(status='active')).values('name').distinct().order_by('name')
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
                    'campaign_listes': list(campaign_listes),
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
#TOP店铺信息
def TOP_campaign_list(request):
    user_app.change_info(request, 'TOP_seller')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID','PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
        return render(request, '../../user_app/templates/404.html')
    try:
        exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
    except:
        exchange_rate = 6.3000

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            caozuo_status = request.GET.get('caozuo_status', '')
            if caozuo_status:
                #增加新数据
                if caozuo_status == 'add':
                    ADDcampaign_name = request.GET.get('ADDcampaign_name', '')
                    ADDcampaign_type = request.GET.get('ADDcampaign_type', '')
                    ADDcampaign_bid_amount = request.GET.get('ADDcampaign_bid_amount', '')
                    if ADDcampaign_bid_amount:
                        ADDcampaign_bid_amount = float(ADDcampaign_bid_amount)
                    else:
                        ADDcampaign_bid_amount=0
                    ADDcampaign_daily_budget = request.GET.get('ADDcampaign_daily_budget', '')
                    if ADDcampaign_daily_budget:
                        ADDcampaign_daily_budget = float(ADDcampaign_daily_budget)
                    else:
                        ADDcampaign_daily_budget=10000
                    ADDcampaign_daily_budget_per_product = request.GET.get('ADDcampaign_daily_budget_per_product', '')
                    if ADDcampaign_daily_budget_per_product:
                        ADDcampaign_daily_budget_per_product = float(ADDcampaign_daily_budget_per_product)
                    else:
                        ADDcampaign_daily_budget_per_product=1000
                    ADDcampaign_lifetime_budget = request.GET.get('ADDcampaign_lifetime_budget', '')
                    if ADDcampaign_lifetime_budget:
                        ADDcampaign_lifetime_budget = float(ADDcampaign_lifetime_budget)
                    else:
                        ADDcampaign_lifetime_budget=100000
                    ADDcampaign_lifetime_budget_per_product = request.GET.get('ADDcampaign_lifetime_budget_per_product', '')
                    if ADDcampaign_lifetime_budget_per_product:
                        ADDcampaign_lifetime_budget_per_product = float(ADDcampaign_lifetime_budget_per_product)
                    else:
                        ADDcampaign_lifetime_budget_per_product=10000
                    store_name_add_valss = request.GET.get('store_name_add_valss', '')
                    store_name_add_es = store_name_add_valss.split(',')
                    del store_name_add_es[-1]
                    errmsg_1=''
                    errmsg_2=''
                    if store_name_add_es:
                        for store_name_add in store_name_add_es:
                            try:
                                store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_add).values_list('store_APIToken')[0][0]
                                data_0 = {'name': ADDcampaign_name,
                                          'type': ADDcampaign_type,
                                          'bid_amount':ADDcampaign_bid_amount,
                                          'daily_budget':ADDcampaign_daily_budget,
                                          'daily_budget_per_product':ADDcampaign_daily_budget_per_product,
                                          'lifetime_budget':ADDcampaign_lifetime_budget,
                                          'lifetime_budget_per_product':ADDcampaign_lifetime_budget_per_product
                                          }
                                subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                if subm.status_code == 200:
                                    errmsg_1 = errmsg_1 + store_name_add  + ','
                                    try:
                                        models_Tophatter.campaign_list.objects.create(USER_ID=USER_ID,
                                                                                      store_name=store_name_add,
                                                                                      name=ADDcampaign_name,
                                                                                      type=ADDcampaign_type,
                                                                                      bid_amount=ADDcampaign_bid_amount,
                                                                                      daily_budget=ADDcampaign_daily_budget,
                                                                                      daily_budget_per_product=ADDcampaign_daily_budget_per_product,
                                                                                      lifetime_budget=ADDcampaign_lifetime_budget,
                                                                                      lifetime_budget_per_product=ADDcampaign_lifetime_budget_per_product,
                                                                                      update_time=datetime.datetime.now(),
                                                                                      save_time=datetime.datetime.now()).save()
                                    except:
                                        print('保存错误')
                                else:
                                    errmsg_2 = errmsg_2 + store_name_add  + ','
                            except Exception as e:
                                errmsg_2 = errmsg_2 + store_name_add  + ','
                        data_msg = {'msg_1': errmsg_1,
                                    'msg_2': errmsg_2
                                    }
                        return HttpResponse(json.dumps(data_msg))
                    else:
                        data_msg_e = {'msg_e': '请选择账号和类型'}
                        return HttpResponse(json.dumps(data_msg_e))
                #编辑已有数据
                if caozuo_status== 'edit':
                    store_name_edit = request.GET.get('store_name_edit', '')
                    name_edit = request.GET.get('name_edit', '')
                    name_type = request.GET.get('name_type', '')
                    field_edit = request.GET.get('field_edit', '')
                    value_edit = request.GET.get('value_edit', '')
                    all_refuse = request.GET.get('all_refuse', '')
                    if value_edit:
                        try:
                            if field_edit == 'status':
                                if value_edit == 'Active' or value_edit == 'active':
                                    if all_refuse == '是':
                                        for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                            try:
                                                store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                                type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                                store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                                models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(type=type). \
                                                    update(status=value_edit, update_time=datetime.datetime.now())
                                                data_0 = {'name': name_edit }
                                                subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/resume.json?access_token=' + store_APIToken, data=data_0,timeout=100)
                                            except:
                                                print('替换错误')
                                    else:
                                        models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(
                                            type=name_type). \
                                            update(status=value_edit, update_time=datetime.datetime.now())
                                        store_APIToken = \
                                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                        data_0 = {'name': name_edit}
                                        subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/resume.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        print(1234)
                                elif value_edit == 'Paused' or value_edit == 'paused':
                                    if all_refuse == '是':
                                        for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                            try:
                                                store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                                type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                                store_APIToken = \
                                                models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                                models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(
                                                    type=type). \
                                                    update(status=value_edit, update_time=datetime.datetime.now())
                                                data_0 = {'name': name_edit}
                                                subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/pause.json?access_token=' + store_APIToken, data=data_0,
                                                                     timeout=100)
                                            except:
                                                print('替换错误')
                                    else:
                                        models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(
                                            type=name_type). \
                                            update(status=value_edit, update_time=datetime.datetime.now())
                                        store_APIToken = \
                                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                        data_0 = {'name': name_edit}
                                        subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/pause.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        print(1234)
                                else :
                                    data_msg_e = {'msg_e': '请填写：active，paused'}
                                    return HttpResponse(json.dumps(data_msg_e))

                            if field_edit == 'daily_budget':
                                if all_refuse == '是':
                                    for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                        try:
                                            store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                            type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                            store_APIToken = \
                                            models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                            models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(type=type). \
                                                update(daily_budget=value_edit, update_time=datetime.datetime.now())
                                            data_0 = {'name': name_edit, 'type': type, 'daily_budget': value_edit, }
                                            subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        except:
                                            print('替换错误')
                                else:
                                    models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(type=name_type). \
                                        update(daily_budget=value_edit, update_time=datetime.datetime.now())
                                    store_APIToken = \
                                    models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                    data_0 = {'name': name_edit, 'type': name_type, 'daily_budget': value_edit, }
                                    subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                            if field_edit == 'bid_amount':
                                if all_refuse == '是':
                                    for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                        try:
                                            store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                            type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                            store_APIToken = \
                                            models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                            models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(type=type). \
                                                update(bid_amount=value_edit, update_time=datetime.datetime.now())
                                            data_0 = {'name': name_edit, 'type': type, 'bid_amount': value_edit, }
                                            subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        except:
                                            print('替换错误')
                                else:
                                    models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(type=name_type). \
                                        update(status=value_edit, update_time=datetime.datetime.now())
                                    store_APIToken = \
                                    models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                    data_0 = {'name': name_edit, 'type': name_type, 'bid_amount': value_edit, }
                                    subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                    aa = subm.text
                                    reponse_dicts = json.loads(aa)
                                    print(123)
                            if field_edit == 'daily_budget_per_product':
                                if all_refuse == '是':
                                    for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                        try:
                                            store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                            type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                            store_APIToken = \
                                            models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                            models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(type=type). \
                                                update(daily_budget_per_product=value_edit, update_time=datetime.datetime.now())
                                            data_0 = {'name': name_edit, 'type': type, 'daily_budget_per_product': value_edit, }
                                            subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        except:
                                            print('替换错误')
                                else:
                                    models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(type=name_type). \
                                        update(daily_budget_per_product=value_edit, update_time=datetime.datetime.now())
                                    store_APIToken = \
                                    models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                    data_0 = {'name': name_edit, 'type': name_type, 'daily_budget_per_product': value_edit, }
                                    subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                            if field_edit == 'lifetime_budget':
                                if all_refuse == '是':
                                    for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                        try:
                                            store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                            type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                            store_APIToken = \
                                            models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                            models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(type=type). \
                                                update(lifetime_budget=value_edit, update_time=datetime.datetime.now())
                                            data_0 = {'name': name_edit, 'type': type, 'lifetime_budget': value_edit, }
                                            subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        except:
                                            print('替换错误')
                                else:
                                    models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(type=name_type). \
                                        update(lifetime_budget=value_edit, update_time=datetime.datetime.now())
                                    store_APIToken = \
                                    models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                    data_0 = {'name': name_edit, 'type': name_type, 'lifetime_budget': value_edit, }
                                    subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                            if field_edit == 'lifetime_budget_per_product':
                                if all_refuse == '是':
                                    for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                        try:
                                            store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                            type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                            store_APIToken = \
                                            models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                            models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(type=type). \
                                                update(lifetime_budget_per_product=value_edit, update_time=datetime.datetime.now())
                                            data_0 = {'name': name_edit, 'type': type, 'lifetime_budget_per_product': value_edit, }
                                            subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        except:
                                            print('替换错误')
                                else:
                                    models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(type=name_type). \
                                        update(lifetime_budget_per_product=value_edit, update_time=datetime.datetime.now())
                                    store_APIToken = \
                                    models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                    data_0 = {'name': name_edit, 'type': name_type, 'lifetime_budget_per_product': value_edit, }
                                    subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                            if field_edit == 'hourly_schedule':
                                if all_refuse == '是':
                                    for i in models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(name=name_edit).values_list('id', flat=True):
                                        try:
                                            store_name = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                            type = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('type')[0][0]
                                            store_APIToken = \
                                            models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]

                                            models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(name=name_edit).filter(type=type). \
                                                update(hourly_schedule=value_edit, update_time=datetime.datetime.now())
                                            data_0 = {'name': name_edit, 'type': type, 'hourly_schedule': value_edit, }
                                            subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)
                                        except:
                                            print('替换错误')
                                else:
                                    models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).filter(name=name_edit).filter(type=name_type). \
                                        update(hourly_schedule=value_edit, update_time=datetime.datetime.now())
                                    store_APIToken = \
                                    models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).values_list('store_APIToken')[0][0]
                                    data_0 = {'name': name_edit, 'type': name_type, 'hourly_schedule': value_edit, }
                                    subm = requests.post('https://tophatter.com/merchant_api/v1/campaigns/update.json?access_token=' + store_APIToken, data=data_0, timeout=100)

                            if subm.status_code == 200:
                                data_msg_e = {'msg_e': '替换成功'}
                                return HttpResponse(json.dumps(data_msg_e))
                            else:
                                data_msg_e = {'msg_e': '替换失败'}
                                return HttpResponse(json.dumps(data_msg_e))
                        except:
                            data_msg_e = {'msg_e': '替换失败'}
                            return HttpResponse(json.dumps(data_msg_e))
                    else:
                        data_msg_e = {'msg_e': '请输入值'}
                        return HttpResponse(json.dumps(data_msg_e))
                # 刷新数据
                if caozuo_status == 'refuse':
                    store_name_refuse = request.GET.get('store_name_refuse', '')
                    if store_name_refuse == 'all' or store_name_refuse=='':
                        try:
                            for i in models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values_list('id', flat=True):
                                try:
                                    store_name = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_name')[0][0]
                                    store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(id=i).values_list('store_APIToken')[0][0]
                                    models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).delete()
                                    try:
                                        subm = requests.get('https://tophatter.com/merchant_api/v1/campaigns.json?access_token=' + store_APIToken + '&per_page=1000', timeout=100)
                                        aa = subm.text
                                        reponse_dicts = json.loads(aa)
                                        # 2 保存到数据库
                                        for reponse_dict in reponse_dicts:
                                            name = reponse_dict.get('name')
                                            type = reponse_dict.get('type')
                                            status = reponse_dict.get('status')
                                            daily_budget = reponse_dict.get('daily_budget')
                                            bid_amount = reponse_dict.get('bid_amount')
                                            daily_budget_per_product = reponse_dict.get('daily_budget_per_product')
                                            lifetime_budget = reponse_dict.get('lifetime_budget')
                                            lifetime_budget_per_product = reponse_dict.get('lifetime_budget_per_product')
                                            hourly_schedule = reponse_dict.get('hourly_schedule')
                                            try:
                                                twz = models_Tophatter.campaign_list.objects.create(
                                                    USER_ID=USER_ID,
                                                    store_name=store_name,
                                                    name=name,
                                                    save_time=datetime.datetime.now(),
                                                    type=type,
                                                    status=status,
                                                    daily_budget=daily_budget,
                                                    bid_amount=bid_amount,
                                                    daily_budget_per_product=daily_budget_per_product,
                                                    lifetime_budget=lifetime_budget,
                                                    lifetime_budget_per_product=lifetime_budget_per_product,
                                                    hourly_schedule=hourly_schedule,
                                                    update_time=datetime.datetime.now(),
                                                )
                                                twz.save()
                                                print(store_name + 'CPM保存 success')
                                            except Exception as e:
                                                print('CPM保存  faile')
                                    except Exception as e:
                                        print('not this CPM 数据')
                                except Exception as e:
                                    print(e)
                                    print('1')
                            data_msg_e = {'msg_e': '刷新成功'}
                            return HttpResponse(json.dumps(data_msg_e))
                        except Exception as e:
                            data_msg_e = {'msg_e': '失败'}
                            return HttpResponse(json.dumps(data_msg_e))
                    else:
                        try:
                            store_name = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_refuse).values_list('store_name')[0][0]
                            store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_refuse).values_list('store_APIToken')[0][0]
                            models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).delete()
                            try:
                                subm = requests.get('https://tophatter.com/merchant_api/v1/campaigns.json?access_token=' + store_APIToken + '&per_page=1000', timeout=100)
                                aa = subm.text
                                reponse_dicts = json.loads(aa)
                                # 2 保存到数据库
                                for reponse_dict in reponse_dicts:
                                    name = reponse_dict.get('name')
                                    type = reponse_dict.get('type')
                                    status = reponse_dict.get('status')
                                    daily_budget = reponse_dict.get('daily_budget')
                                    bid_amount = reponse_dict.get('bid_amount')
                                    daily_budget_per_product = reponse_dict.get('daily_budget_per_product')
                                    lifetime_budget = reponse_dict.get('lifetime_budget')
                                    lifetime_budget_per_product = reponse_dict.get('lifetime_budget_per_product')
                                    hourly_schedule = reponse_dict.get('hourly_schedule')
                                    try:
                                        twz = models_Tophatter.campaign_list.objects.create(
                                            USER_ID=USER_ID,
                                            store_name=store_name,
                                            name=name,
                                            save_time=datetime.datetime.now(),
                                            type=type,
                                            status=status,
                                            daily_budget=daily_budget,
                                            bid_amount=bid_amount,
                                            daily_budget_per_product=daily_budget_per_product,
                                            lifetime_budget=lifetime_budget,
                                            lifetime_budget_per_product=lifetime_budget_per_product,
                                            hourly_schedule=hourly_schedule,
                                            update_time=datetime.datetime.now(),
                                        )
                                        twz.save()
                                    except Exception as e:
                                        print('CPM保存  faile')
                            except Exception as e:
                                print('not this CPM 数据')
                            data_msg_e = {'msg_e': '刷新成功'}
                            return HttpResponse(json.dumps(data_msg_e))
                        except Exception as e:
                            data_msg_e = {'msg_e': '失败'}
                            return HttpResponse(json.dumps(data_msg_e))

            store_name = request.GET.get('store_name', '')
            campaign_name = request.GET.get('campaign_name', '')
            campaign_type = request.GET.get('campaign_type', '')
            campaign_status = request.GET.get('campaign_status', '')
            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式
            if store_name == '':
                store_name='all'
            if campaign_type == '':
                campaign_type = '全部订单'
            if campaign_status == '':
                campaign_status = '全部订单'

            if Sort_field == '':
                Sort_field = 'store_name'

            if Sort_order == 'desc' :
                Sort_order = '-'
            elif Sort_order == 'asc'or Sort_order == '':
                Sort_order = ''
            else:
                Sort_order = ''

            if limit == '' and page == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {'store_name_users': list(store_name_users)}
                return render(request, 'Tophatter/TOP_campaign_list.html', context0)
            try:
                page_star = int(limit) * (int(page) - 1)
                page_end = page_star + int(limit)

                objs = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID)
                if store_name != 'all':
                    objs = objs.filter(store_name=store_name)
                if campaign_name != '':
                    objs = objs.filter(name__contains=campaign_name)
                if campaign_type != '全部订单':
                    objs = objs.filter(type=campaign_type)
                if campaign_status != '全部订单':
                    objs = objs.filter(status=campaign_status)
                count_all = objs.values().count()
                objs = objs.values().order_by(Sort_order+Sort_field)[page_star:page_end]  # 已备注的卖家

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
            return render(request, 'Tophatter/TOP_campaign_list.html')
# 上传CSV文件产品
@csrf_exempt
def uploading_csv(request):
    user_app.change_info(request, 'uploading_csv')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
            context0 = {'store_name_users': list(store_name_users)}
            return render(request, 'Tophatter/uploading_csv.html', context0)

            开始上传 = request.GET.get('开始上传', '')
            if 开始上传:
                try:
                    # 获取需要上传的目标店铺，以列表的形式
                    filename = request.GET.get('filename_orders', '')
                    store_value = request.GET.get('valss', '')
                    store_list = store_value.split(',')
                    del store_list[-1]
                    if store_list:
                        errmsg_1 = ''
                        errmsg_2 = ''
                        errmsg_3 = ''
                        for store in store_list:
                            store_APIToken =  models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store).values_list('store_APIToken')[0][0]
                            data_all = []
                            i = 0
                            data_variations = {}
                            data_msg = {
                                'msg_1': '无',
                                'msg_2': '无',
                            }
                            subm_index_1 = 0
                            subm_index_2 = 0
                            identifier_index = '开始'
                            with open(filename) as f:
                                reader = csv.reader(f)
                                for row in reader:
                                    i = i + 1
                                    if i == 1:
                                        xyz = row[16]  # 如果第16列是 SFB价格 表格模板就是店铺后台模板。如果不是那就是 财来了 模板
                                    if i > 1:
                                        if   xyz == 'Scheduling Fee Bid':  # 店铺模板
                                            identifier = store + '-' + row[0] + '-' + now_str_data  # Product Unique ID
                                            category = row[1]  # Product Category
                                            title = row[2]  # Product Title
                                            description = row[3]  # Product Description
                                            condition = row[4]  # Product Condition
                                            brand = row[5]  # Product Brand
                                            material = row[6]  # Product Material
                                            variations_identifier = store + '-' + row[7] + '-' + now_str_data  # Variation Unique ID
                                            variations_size = row[8]  # Variation Size
                                            variations_color = row[9]  # Variation Color
                                            if row[10] and row[10] != '0':
                                                variations_quantity = int(row[10])  # Variation Quantity
                                            else:
                                                variations_quantity = None

                                            if row[11] and row[11] != '0':
                                                cost_basis = int(row[11])  # Target Price
                                            else:
                                                cost_basis = None

                                            if row[12] and row[12] != '0':
                                                buy_now_price = int(row[12])  # Buy Now Price
                                            else:
                                                buy_now_price = None

                                            if row[13] and row[13] != '0':
                                                retail_price = int(row[13])  # Retail Price
                                            else:
                                                retail_price = None

                                            if row[14] and row[14] != '0':
                                                minimum_bid_amount = int(row[14])  # Starting Bid
                                            else:
                                                minimum_bid_amount = None

                                            if row[15] and row[15] != '0':
                                                reserve_price = int(row[15])  # Reserve Price
                                            else:
                                                reserve_price = None

                                            if row[16] and row[16] != '0':
                                                scheduling_fee_bid = float(row[16])  # Scheduling Fee Bid
                                            else:
                                                scheduling_fee_bid = None

                                            if row[17] and row[17] != '0':
                                                max_daily_schedules = int(row[17])  # Max Daily Schedules
                                            else:
                                                max_daily_schedules = None

                                            if row[18] and row[18] != '0':
                                                shipping_price = int(row[18])  # Shipping Price
                                            else:
                                                shipping_price = None
                                            shipping_origin = row[19]  # Ships From Country
                                            # fulfillment_partner = row[0] #
                                            if row[20] and row[20] != '0':
                                                weight = int(row[20])  # Shipping Weight In Ounces
                                            else:
                                                weight = None

                                            if row[21] and row[21] != '0':
                                                days_to_fulfill = int(row[21])  # Days To Process Orde
                                            else:
                                                days_to_fulfill = None

                                            if row[22] and row[22] != '0':
                                                expedited_shipping_price = int(row[22])  # Expedited Shipping Price
                                            else:
                                                expedited_shipping_price = None

                                            if row[23] and row[23] != '0':
                                                expedited_days_to_deliver = int(row[23])  # Expedited Delivery Time
                                            else:
                                                expedited_days_to_deliver = None

                                            buy_one_get_one_available = row[24]  # Buy One Get One Available

                                            if row[25] and row[25] != '0':
                                                accessory_price = int(row[25])  # Accessory Price
                                            else:
                                                accessory_price = None
                                            accessory_description = row[26]  # Accessory Description

                                            primary_image = row[28]  # Primary Image URL
                                            extra_images = row[29]  # Extra Image URL 1 | Extra Image URL 2
                                            if row[30]:
                                                extra_images = extra_images + '|' + row[30]
                                            if row[31]:
                                                extra_images = extra_images + '|' + row[31]
                                            if row[32]:
                                                extra_images = extra_images + '|' + row[32]
                                            # campaign_name = row[34]  # Campaign Name
                                        elif xyz == 'Ships From Country':  # 财来了模板
                                            identifier = store + '-' + row[0] + '-' + now_str_data  # Product Unique ID
                                            category = row[1]  # Product Category
                                            title = row[2]  # Product Title
                                            description = row[3]  # Product Description
                                            condition = row[4]  # Product Condition
                                            brand = row[5]  # Product Brand
                                            material = row[6]  # Product Material
                                            variations_identifier = store + '-' + row[7] + '-' + now_str_data  # Variation Unique ID
                                            variations_size = row[8]  # Variation Size
                                            variations_color = row[9]  # Variation Color
                                            if row[10] and row[10] != '0':
                                                variations_quantity = int(row[10])  # Variation Quantity
                                            else:
                                                variations_quantity = None

                                            if row[14] and row[14] != '0':
                                                cost_basis = int(row[14])  # Target Price
                                            else:
                                                cost_basis = None

                                            if row[12] and row[12] != '0':
                                                buy_now_price = int(row[12])  # Buy Now Price
                                            else:
                                                buy_now_price = None

                                            if row[13] and row[13] != '0':
                                                retail_price = int(row[13])  # Retail Price
                                            else:
                                                retail_price = None

                                            if row[11] and row[11] != '0':
                                                minimum_bid_amount = int(row[11])  # Starting Bid
                                            else:
                                                minimum_bid_amount = None

                                            reserve_price = None  # Reserve Price

                                            if row[25] and row[25] != '0':
                                                scheduling_fee_bid = float(row[25])  # Scheduling Fee Bid
                                            else:
                                                scheduling_fee_bid = None

                                            max_daily_schedules = None  # Max Daily Schedules

                                            if row[15] and row[15] != '0':
                                                shipping_price = int(row[15])  # Shipping Price
                                            else:
                                                shipping_price = None

                                            shipping_origin = row[16]  # Ships From Country

                                            if row[17] and row[17] != '0':
                                                weight = int(row[17])  # Shipping Weight In Ounces
                                            else:
                                                weight = None

                                            if row[18] and row[18] != '0':
                                                days_to_fulfill = int(row[18])  # Days To Process Orde
                                            else:
                                                days_to_fulfill = None

                                            if row[20] and row[20] != '0':
                                                expedited_shipping_price = int(row[20])  # Expedited Shipping Price
                                            else:
                                                expedited_shipping_price = None

                                            if row[21] and row[21] != '0':
                                                expedited_days_to_deliver = int(row[21])  # Expedited Delivery Time
                                            else:
                                                expedited_days_to_deliver = None

                                            buy_one_get_one_available = row[22]  # Buy One Get One Available

                                            if row[23] and row[23] != '0':
                                                accessory_price = int(row[23])  # Accessory Price
                                            else:
                                                accessory_price = None

                                            accessory_description = row[24]  # Accessory Description

                                            primary_image = row[26]  # Primary Image URL
                                            extra_images = row[27]  # Extra Image URL 1 | Extra Image URL 2
                                            if row[28]:
                                                extra_images = extra_images + '|' + row[28]
                                            if row[29]:
                                                extra_images = extra_images + '|' + row[29]
                                            if row[30]:
                                                extra_images = extra_images + '|' + row[30]
                                        elif xyz == '来源url':  # 店小秘模板
                                            identifier = store + '-' + row[0] + '-' + now_str_data  # ParentSKU
                                            category = row[2]  # 产品分类
                                            title = row[3]  # 产品标题
                                            description = row[4]  # 产品描述
                                            condition = row[5]  # 物品状况
                                            brand = row[6]  # 产品品牌
                                            material = row[7]  # 产品材质
                                            variations_identifier = store + '-' + row[1] + '-' + now_str_data  # SKU
                                            variations_size = row[8]  # 尺寸
                                            variations_color = row[9]  # 颜色
                                            if row[10] and row[10] != '0':
                                                variations_quantity = int(row[10])  # 库存
                                            else:
                                                variations_quantity = None

                                            if row[12] and row[12] != '0':
                                                cost_basis = int(row[12])  # 目标价
                                            else:
                                                cost_basis = None

                                            if row[13] and row[13] != '0':
                                                buy_now_price = int(row[13])  # 一口价
                                            else:
                                                buy_now_price = None

                                            if row[11] and row[11] != '0':
                                                retail_price = int(row[11])  # 零售价
                                            else:
                                                retail_price = None

                                            if row[15] and row[15] != '0':
                                                minimum_bid_amount = int(row[15])  # 起拍价
                                            else:
                                                minimum_bid_amount = None

                                            reserve_price = None  # Reserve Price

                                            if row[14] and row[14] != '0':
                                                scheduling_fee_bid = float(row[14])  # 拍卖安排费出价
                                            else:
                                                scheduling_fee_bid = None

                                            if row[24] and row[24] != '0':
                                                max_daily_schedules = int(row[24])  # 最大日销售量
                                            else:
                                                max_daily_schedules = None

                                            if row[17] and row[17] != '0':
                                                shipping_price = int(row[17])  # 运费
                                            else:
                                                shipping_price = None

                                            shipping_origin = row[18]  # 发货地

                                            if row[20] and row[20] != '0':
                                                weight = int(row[20])  # 运输重量
                                            else:
                                                weight = None

                                            if row[19] and row[19] != '0':
                                                days_to_fulfill = int(row[19])  # 处理时间
                                            else:
                                                days_to_fulfill = None

                                            if row[21] and row[21] != '0':
                                                expedited_shipping_price = int(row[21])  # 快速运输运费
                                            else:
                                                expedited_shipping_price = None

                                            if row[22] and row[22] != '0':
                                                expedited_days_to_deliver = int(row[22])  # 快速运输时间
                                            else:
                                                expedited_days_to_deliver = None

                                            buy_one_get_one_available = ''  # row[22]  # Buy One Get One Available

                                            if row[25] and row[25] != '0':
                                                accessory_price = int(row[25])  # 配件价格
                                            else:
                                                accessory_price = None

                                            accessory_description = row[26]  # 配件描述

                                            primary_image = row[27]  # 主图（url）地址
                                            extra_images = row[28]  # 附图（URL）地址
                                            if row[29]:
                                                extra_images = extra_images + '|' + row[29]
                                            if row[30]:
                                                extra_images = extra_images + '|' + row[30]
                                            if row[31]:
                                                extra_images = extra_images + '|' + row[31]
                                        else:
                                            data_msg_e = {'msg_e': '模板错误'}
                                            return HttpResponse(json.dumps(data_msg_e))

                                        if identifier_index != identifier and i > 2:
                                            data.update(data_variations_end)
                                            data_all.append(data)
                                            data_variations = {}
                                        if variations_identifier:
                                            data_variations_0 = {
                                                'variations[' + variations_identifier + '][identifier]': variations_identifier,
                                                'variations[' + variations_identifier + '][size]': variations_size,
                                                'variations[' + variations_identifier + '][color]': variations_color,
                                                'variations[' + variations_identifier + '][quantity]': variations_quantity
                                            }
                                            data_variations.update(data_variations_0)
                                        if identifier_index != identifier or identifier_index == '开始':
                                            data_0 = {
                                                'access_token': store_APIToken,  # '2f9a6837ddb548932118fb57b625f3b3',  # 实验账号
                                                'identifier': identifier,
                                                'category': category,
                                                'title': title,
                                                'description': description,
                                                'condition': condition,
                                                'brand': brand,
                                                'material': material,
                                                'cost_basis': cost_basis,
                                                'buy_now_price': buy_now_price,

                                                'retail_price': retail_price,
                                                'minimum_bid_amount': minimum_bid_amount,
                                                'reserve_price': reserve_price,
                                                'scheduling_fee_bid': scheduling_fee_bid,
                                                'max_daily_schedules': max_daily_schedules,
                                                'shipping_price': shipping_price,
                                                'shipping_origin': shipping_origin,
                                                'weight': weight,
                                                'days_to_fulfill': days_to_fulfill,
                                                'expedited_shipping_price': expedited_shipping_price,
                                                'expedited_days_to_deliver': expedited_days_to_deliver,
                                                'buy_one_get_one_available': buy_one_get_one_available,
                                                'accessory_price': accessory_price,
                                                'accessory_description': accessory_description,

                                                'primary_image': primary_image,
                                                'extra_images': extra_images,
                                                # 'campaign_id': '0.01'
                                            }
                                            data = data_0
                                            data_variations_end = data_variations
                                        # print(identifier, identifier_index)
                                        identifier_index = identifier
                                data.update(data_variations_end)
                                data_all.append(data)

                                for data in data_all:
                                    # print('开始上传')
                                    try:
                                        subm = requests.post('https://tophatter.com/merchant_api/v1/products.json', data=data, timeout=15)
                                        print("status code:", subm.status_code, store)
                                        if subm.status_code == 200:
                                            subm_index_1 = subm_index_1 + 1
                                        else:
                                            subm_index_2 = subm_index_2 + 1
                                    except Exception as e:
                                        print(e)
                                        subm_index_2 = subm_index_2 + 1
                            try:
                                errmsg_1 = errmsg_1 + store + '(' + str(subm_index_1) + ')' + ','
                                data_msg['msg_1'] = errmsg_1
                                subm_index_1 = 0

                                errmsg_2 = errmsg_2 + store + '(' + str(subm_index_2) + ')' + ','
                                data_msg['msg_2'] = errmsg_2
                                subm_index_2 = 0
                            except:
                                errmsg_2 = errmsg_2 + store + '(' + str(subm_index_2) + ')' + ','
                                data_msg['msg_2'] = errmsg_2
                                subm_index_2 = 0
                        return HttpResponse(json.dumps(data_msg))
                except Exception as e:
                    data_msg_e = {'msg_e': str(e)}
                    print(data_msg_e)
                    return HttpResponse(json.dumps(data_msg_e))
                return render(request, 'Tophatter/uploading_csv.html')

        if request.method == "POST":
            now = datetime.datetime.now()
            now_str = now.strftime('%Y%m%d_%H%M%S')
            File = request.FILES['file']
            if File is None:
                errmsg = '没有上传的文件！！！'
                context = {'status': 0, 'msg': errmsg}
                return HttpResponse(json.dumps(context))
            else:
                from django.core.files.storage import FileSystemStorage
                try:
                    fs = FileSystemStorage()
                    filename_orders = fs.save('./static/user_files_directory/upload_file_products/' + str(USER_ID) + '_' + File.name[:-4] + now_str + File.name[-4:], File)
                    errmsg = '上传文件到服务器成功！！！'
                    context = {'status': 0,
                               'msg': errmsg,
                               'filename_orders': filename_orders}
                    return HttpResponse(json.dumps(context))
                except:
                    errmsg = '上传失败！！！'
                    context = {'status': 1,
                               'msg': errmsg}
                    return HttpResponse(json.dumps(context))


# TOP店铺资金
def Top_founds(request):
    user_app.change_info(request, 'uploading_one')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {
                            'store_name_users':list(store_name_users),
                            'exchange_rate':exchange_rate,
                            }
                return render(request, 'Tophatter/Top_founds.html',context0)
            if cols == 'cols':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                i = 0
                for store_name_user in store_name_users:
                    i = i+1
                    store_name_user['field'] = str(i)

                context1 = { 'store_name_users':list(store_name_users), }
                return HttpResponse(json.dumps(context1))

            count_all = 0
            objs = models_Tophatter.Founds.objects.filter(USER_ID=USER_ID).values('Time_Date').annotate(store_name_count=Count('store_name')).order_by('-Time_Date')
            count_all = objs.count()
            store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
            for obj in objs:
                i = 0
                obj['UP']=0
                obj['PE'] = 0
                obj['SUM_UP_PE'] = 0
                obj['SUM_UP_PE_REN'] = 0
                obj['SUM_UP_PE_92'] = 0
                for store_name_user in store_name_users:
                    i = i + 1
                    Upcoming =  0
                    Pending  =  0
                    sum_up_pe = 0
                    oa = models_Tophatter.Founds.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_user['store_name']).filter(Time_Date=obj['Time_Date'])\
                         .values('store_name','Upcoming','Pending','Time_Date','save_time')
                    if oa:
                        if oa[0]['Upcoming'] and  oa[0]['Pending']:
                            Upcoming = float(oa[0]['Upcoming'])
                            Pending = float(oa[0]['Pending'])
                            sum_up_pe = round(Upcoming + Pending,2)
                            obj[str(i)] = oa[0]['Upcoming'] + ' / ' +  oa[0]['Pending']  +' / '+ str(sum_up_pe)
                        else:
                            obj[str(i)] = '未获取'
                    else:
                        obj[str(i)] = '未获取'
                    obj['UP'] += Upcoming
                    obj['PE'] += Pending
                    obj['SUM_UP_PE'] += sum_up_pe
                obj['SUM_UP_PE_REN'] = obj['SUM_UP_PE'] * exchange_rate
                obj['SUM_UP_PE_92'] = (obj['UP'] + obj['PE']*0.92)*exchange_rate
                obj['UP'] = round(obj['UP'],2)
                obj['PE'] = round(obj['PE'],2)
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
#TOP店铺信息
def TOP_store_msg(request):
    user_app.change_info(request, 'TOP_seller')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID','PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_edit).update(store_APIToken=value_edit,updated_time = datetime.datetime.now())
                    elif field_edit == 'seller_id':
                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(seller_id=value_edit,updated_time = datetime.datetime.now())
                    elif field_edit == 'IP_address':
                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(IP_address=value_edit,updated_time = datetime.datetime.now())
                    elif field_edit == 'store_cookie':
                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(store_cookie=value_edit,updated_time = datetime.datetime.now())
                    elif field_edit == 'beizhu':
                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter( store_name=store_name_edit).update(beizhu=value_edit,updated_time = datetime.datetime.now())
                    data_msg_e = {'msg_e': '替换成功'}
                    return HttpResponse(json.dumps(data_msg_e))
                except:
                    data_msg_e = {'msg_e': '替换失败'}
                    return HttpResponse(json.dumps(data_msg_e))
            #增加新数据
            if caozuo_status == 'add':
                try:
                    if store_name_add :
                        index = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_add)
                        if index:
                            data_msg_e = {'msg_e': '该账号名已存在'}
                            return HttpResponse(json.dumps(data_msg_e))
                        else:
                            models_Tophatter.APIAccessToken.objects.create(USER_ID=USER_ID,store_name=store_name_add,created_time=datetime.datetime.now(),updated_time = datetime.datetime.now()).save()
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
                        models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_del).delete()
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
                return render(request, 'Tophatter/TOP_store_msg.html')
            try:
                page_star = int(limit) * (int(page) - 1)
                page_end = page_star + int(limit)

                objs = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values()
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
            return render(request, 'Tophatter/TOP_store_msg.html')
# TOP文件下载
def Top_download(request):
    user_app.change_info(request, 'uploading_one')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
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
            start_time = request.GET.get('start_time', '')  # 统计时间
            end_time = request.GET.get('end_time', '')  # 统计时间
            订单ID = request.GET.get('订单ID', '')  # 订单ID
            time_local = request.GET.get('time_local', '')  # 时间段
            订单状态 = request.GET.get('订单状态', '')  # 订单状态
            product_identifier = request.GET.get('product_identifier', '')  # 商品名称
            product_type = request.GET.get('product_type', '')  # 订单类型
            related_order_ids = request.GET.get('related_order_ids', '')  # 关系订单
            service_type = request.GET.get('service_type', '')  # 服务类型
            input_order_type = request.GET.get('input_order_type', '')  # 已回款订单
            承运商 = request.GET.get('承运商', '')

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

            if limit == '' and page == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {
                    'store_name_users': list(store_name_users),
                }
                return render(request, 'Tophatter/Top_download.html', context0)
#日期转换成JOSN的解码函数
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


