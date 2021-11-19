from django.shortcuts import render
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
#Top 所有商品
def Products_All_Own(request):
    user_app.change_info(request, 'Products_All_Own')
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
        if request.method == "GET" :
            导出类型 = request.GET.get('导出类型', '')
            checked_value = request.GET.get('checkStatus', '')
            FIG = request.GET.get('FIG', '')
            store_name = request.GET.get('store_name', '')
            store_name_5M = request.GET.get('store_name_5M', '')

            caozuo_status = request.GET.get('caozuo_status', '')
            id_edit = request.GET.get('id_edit', '')
            field_edit = request.GET.get('field_edit', '')
            value_edit = request.GET.get('value_edit', '')

            #编辑已有数据
            if caozuo_status== 'edit':
                try:
                    if field_edit == 'user_collect':
                        models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=id_edit).update(user_collect=value_edit,updated_at = datetime.datetime.now())
                        data_msg_e = {'msg_e': '替换成功'}
                        return HttpResponse(json.dumps(data_msg_e))
                    else:
                        data_msg_e = {'msg_e': '字段错误'}
                        return HttpResponse(json.dumps(data_msg_e))
                except:
                    data_msg_e = {'msg_e': '替换失败'}
                    return HttpResponse(json.dumps(data_msg_e))
            # 导出数据
            if 导出类型:
                products_list = literal_eval(checked_value)
                user_app.change_info(request, '导出商品库-TOP')
                if 导出类型 == '导出选择商品':
                    with open("C:\\shengkongshuju\\static\\user_files_directory\\导出平台数据\\商品详情_商品库.csv", 'w', encoding='utf-8', newline='') as fp:
                    # with open("F:\\E_commerce\\static\\导出平台商品\\商品详情.csv", 'w', encoding='utf-8', newline='') as fp:
                        headers = ('ParentSKU(必填)', 'SKU（必填）', '产品分类', '产品标题（必填）', '产品描述（必填）',  # 5
                                   '物品状况（必填）', '产品品牌', '产品材质', '尺寸', '颜色', '库存(必填)', '零售价', '目标价(必填)',  # 13
                                   '一口价(必填)', '拍卖安排费出价', '起拍价', '来源url', '运费(必填)', '发货地(必填)', '处理时间(必填)',  # 20
                                   '运输重量', '快速运输运费（美国）', '快速运输时间', '附加项目价格', '最大日销售量', '配件价格', '配件描述',  # 27
                                   '主图（URL）地址(必填)', '附图1（URL）地址', '附图2（URL）地址', '附图3（URL）地址', '附图4（URL）地址',  # 32
                                   '附图5（URL）地址', '附图6（URL）地址', '附图7（URL）地址', '商品编号')  # 35
                        writer = csv.writer(fp, dialect='excel')
                        writer.writerow(headers)  # 写入一行
                        for products_id in products_list:
                            try:
                                objs_load_orders = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=products_id).values_list(
                                    'product_name', 'category', 'title', 'description', 'retail_price', 'buy_now_price',
                                    'minimum_bid_amount', 'shipping_price')
                                products = list(objs_load_orders[0])
                                products_s = products

                                load_orders_facets = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=products_id).values(
                                    'material', 'condition', 'size', 'color', 'accessory_price', 'accessory_description', 'primary_image',
                                    'all_images', 'standard_product_id', 'lots_id')  # 获取详细参数信息

                                facet_Material = load_orders_facets[0]['material']
                                facet_Condition = load_orders_facets[0]['condition']
                                facet_Available_Sizes = load_orders_facets[0]['size']
                                facet_Available_Colors = load_orders_facets[0]['color']

                                lot_upsells_description = load_orders_facets[0]['accessory_description']
                                lot_upsells_amount = load_orders_facets[0]['accessory_price']

                                facet_Available_images = load_orders_facets[0]['all_images']
                                all_images = facet_Available_images.split('|')
                                image_urls_0 = ''
                                image_urls_1 = ''
                                image_urls_2 = ''
                                image_urls_3 = ''
                                image_urls_4 = ''
                                image_urls_5 = ''
                                ii = 0
                                try:
                                    for image in all_images:
                                        if ii == 0:
                                            image_urls_0 = image
                                        if ii == 1:
                                            image_urls_1 = image
                                        if ii == 2:
                                            image_urls_2 = image
                                        if ii == 3:
                                            image_urls_3 = image
                                        if ii == 4:
                                            image_urls_4 = image
                                        if ii == 5:
                                            image_urls_5 = image
                                        ii = ii + 1
                                except:
                                    image_urls_0 = ''
                                    image_urls_1 = ''
                                    image_urls_2 = ''
                                    image_urls_3 = ''
                                    image_urls_4 = ''
                                    image_urls_5 = ''

                                products_s.insert(4, facet_Condition)  # 物品状况（必填）
                                products_s.insert(5, '')  # 产品品牌
                                products_s.insert(6, facet_Material)  # 产品材质

                                products_s.insert(7, 1000)  # 库存
                                products_s.insert(9, '')  # 目标价
                                products_s.insert(11, '')  # 拍卖安排费出价
                                products_s.insert(13, '')  # 来源url
                                products_s.insert(15, 'China')  # 发货地
                                products_s.insert(16, 5)  # 处理时间
                                products_s.insert(17, '')  # 运输重量
                                products_s.insert(18, '')  # 快速运输运费
                                products_s.insert(19, '')  # 快速运输时间
                                products_s.insert(20, '')  # 附加项目价格
                                products_s.insert(21, '')  # 最大日销售量
                                products_s.insert(22, lot_upsells_amount)  # 配件价格
                                products_s.insert(23, lot_upsells_description)  # 配件描述
                                products_s.insert(24, load_orders_facets[0]['primary_image'])  # 主图
                                products_s.insert(25, image_urls_1)  # 图1
                                products_s.insert(26, image_urls_2)  # 图2
                                products_s.insert(27, image_urls_3)  # 图3
                                products_s.insert(28, image_urls_4)  # 图4
                                products_s.insert(29, image_urls_5)  # 图5
                                products_s.insert(30, '')  # 图6
                                products_s.insert(31, '')  # 图7
                                products_s.insert(32, load_orders_facets[0]['lots_id'])  # 商品编号

                                facet_Available_Sizes = re.sub('[ ]', '', facet_Available_Sizes)
                                facet_Available_Colors = re.sub('[ ]', '', facet_Available_Colors)
                                facet_Available_Size = facet_Available_Sizes.split(',')
                                facet_Available_Color = facet_Available_Colors.split(',')
                                if facet_Available_Size != ['']:
                                    if facet_Available_Color != ['']:
                                        for facet_Size in facet_Available_Size:
                                            for facet_Color in facet_Available_Color:
                                                products_s0 = []
                                                products_s0 += products_s
                                                products_s0.insert(1, products_s[0] + '-' + facet_Size + '-' + facet_Color)
                                                products_s0.insert(8, facet_Size)  # 尺寸
                                                products_s0.insert(9, facet_Color)  # 颜色

                                                products_s0 = tuple(products_s0)
                                                products_s1 = []
                                                products_s1.insert(0, products_s0)
                                                writer.writerows(products_s1)  # 写入多行
                                    else:
                                        for facet_Size in facet_Available_Size:
                                            products_s0 = []
                                            products_s0 += products_s
                                            products_s0.insert(1, products_s[0] + '-' + facet_Size)
                                            products_s0.insert(8, facet_Size)  # 尺寸
                                            products_s0.insert(9, '')  # 颜色

                                            products_s01 = tuple(products_s0)
                                            products_s1 = []
                                            products_s1.insert(0, products_s01)
                                            writer.writerows(products_s1)  # 写入多行
                                else:
                                    if facet_Available_Color != ['']:
                                        for facet_Color in facet_Available_Color:
                                            products_s0 = []
                                            products_s0 += products_s
                                            products_s0.insert(1, products_s[0] + '-' + facet_Color)
                                            products_s0.insert(8, '')  # 尺寸
                                            products_s0.insert(9, facet_Color)  # 颜色

                                            products_s0 = tuple(products_s0)
                                            products_s1 = []
                                            products_s1.insert(0, products_s0)
                                            writer.writerows(products_s1)  # 写入多行
                                    else:
                                        products_s0 = []
                                        products_s0 += products_s
                                        products_s0.insert(1, products_s[0])
                                        products_s0.insert(8, '')  # 尺寸
                                        products_s0.insert(9, '')  # 颜色

                                        products_s0 = tuple(products_s0)
                                        products_s1 = []
                                        products_s1.insert(0, products_s0)
                                        writer.writerows(products_s1)  # 写入多行
                            except Exception as e:
                                print(e)
                    Detailed_orders = {'Detailed_orders': '1'}
                    return HttpResponse(json.dumps(Detailed_orders))
                else:
                    Detailed_orders = {'Detailed_orders': '0'}
                    return HttpResponse(json.dumps(Detailed_orders))
            # 上传选中商品库产品到TOP
            if FIG == 'FIG1':
                if checked_value == '':
                    data_msg_e = {'msg_e': '请选择要上传的产品'}
                    return HttpResponse(json.dumps(data_msg_e))
                if store_name == '':
                    data_msg_e = {'msg_e': '请选择要上传的TOP店铺'}
                    return HttpResponse(json.dumps(data_msg_e))

                now = datetime.datetime.now()
                now_str = now.strftime('%Y%m%d_%H%M%S')
                now_str_data = now.strftime('%Y%m%d')[2:]
                errmsg_1 = ''
                errmsg_2 = ''
                products_list = literal_eval(checked_value)
                for product_id in products_list:
                    # 获取自己店铺产品
                    try:
                        Product = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=product_id).values_list()
                        摇钱数ID = Product[0][0]
                        产品SKU = Product[0][1]
                        产品分类 = Product[0][3]
                        产品标题 = Product[0][4]
                        产品材质 = Product[0][8]
                        物品状况 = Product[0][6]
                        产品描述 = Product[0][5]
                        产品尺寸 = Product[0][11]
                        产品颜色 = Product[0][10]
                        产品尺寸 = 产品尺寸.split(',')
                        产品颜色 = 产品颜色.split(',')
                        库存数量 = Product[0][9]

                        一口价 = Product[0][33]
                        目标价 = Product[0][13]
                        底价 = Product[0][17]
                        # 底价 = re.sub('None', '', 底价)
                        零售价 = Product[0][12]
                        SFB = Product[0][16]
                        起拍价 = Product[0][14]

                        运输费用 = Product[0][18]
                        运输重量 = Product[0][21]
                        发货地 = 'China'
                        是否买一得一 = 'No'
                        处理时间 = Product[0][23]
                        处理时间 = re.sub('None', '', str(处理时间))
                        最大日销售数量 = Product[0][15]
                        CAMPAIGN = Product[0][34]
                        配件价格 = Product[0][27]
                        配件描述 = Product[0][28]

                        主图序号 = Product[0][46]
                        产品图片all = Product[0][30]
                        产品图片all = 产品图片all.split('|')
                        try:
                            产品图片1 = 产品图片all[0]
                        except:
                            产品图片1 = ''

                        try:
                            产品图片2 = 产品图片all[1]
                        except:
                            产品图片2 = ''

                        try:
                            产品图片3 = 产品图片all[2]
                        except:
                            产品图片3 = ''

                        try:
                            产品图片4 = 产品图片all[3]
                        except:
                            产品图片4 = ''

                        try:
                            产品图片5 = 产品图片all[4]
                        except:
                            产品图片5 = ''

                        try:
                            产品图片6 = 产品图片all[5]
                        except:
                            产品图片6 = ''

                        try:
                            产品图片7 = 产品图片all[6]
                        except:
                            产品图片7 = ''

                        try:
                            产品图片8 = 产品图片all[7]
                        except:
                            产品图片8 = ''

                    except Exception as e:
                        print(e)
                    # 获取自己店铺产品的价格信息
                    try:
                        ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=产品SKU).values('id').annotate(
                              SKU_price=Max('SKU_price', distinct=True)
                            , SKU_parts_price=Max('SKU_parts_price', distinct=True)
                            , SKU_weight=Max('SKU_weight', distinct=True)  # -------
                            , SKU_parts_weight=Max('SKU_parts_weight', distinct=True)  # -------
                            , SKU_variety=Max('SKU_variety', distinct=True)
                            , HAI_SKU_freight=Max('HAI_SKU_freight', distinct=True))  # -------
                        if ob:
                            SKU_price = ob[0]['SKU_price']  # 单价
                            SKU_parts_price = ob[0]['SKU_parts_price']  # 配件价
                            SKU_weight = ob[0]['SKU_weight']  # 单重量
                            SKU_parts_weight = ob[0]['SKU_parts_weight']  # 单配件重量
                            SKU_variety = ob[0]['SKU_variety']  # 单种类
                            HAI_SKU_freight = ob[0]['HAI_SKU_freight']  # 海运费用
                            if SKU_price == None:
                                SKU_price = ''
                            if SKU_parts_price == None:
                                SKU_parts_price = ''
                            if SKU_weight == None:
                                SKU_weight = ''
                            if SKU_parts_weight == None:
                                SKU_parts_weight = ''
                            if SKU_variety == None:
                                SKU_variety = ''
                            if HAI_SKU_freight == None:
                                HAI_SKU_freight = ''
                    except Exception as e:
                        print(e)
                    # 获取自己店铺产品的价格信息
                    try:
                        # 获取需要上传的目标店铺，以列表的形式
                        store_APIToken = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).values_list('store_APIToken')[0][0]
                        data_variations = {}
                        data_msg = {
                            'msg_1': '无',
                            'msg_2': '无',
                        }

                        if 产品SKU != '' and 产品标题 != '' and 产品描述 != '' and 产品分类 != '' and \
                                物品状况 != '' and 一口价 != '' and 运输费用 != '' and \
                                处理时间 != '' and 发货地 != '':
                            # 店铺模板
                            identifier = store_name + '-' + 产品SKU + '-' + now_str_data  # Product Unique ID
                            category = 产品分类  # Product Category
                            title = 产品标题  # Product Title
                            description = 产品描述  # Product Description
                            condition = 物品状况  # Product Condition
                            brand = ''  # Product Brand
                            material = 产品材质  # Product Material
                            # variations_size = 尺寸  # Variation Size
                            # variations_color = 颜色  # Variation Color
                            if 库存数量 and 库存数量 != '0':
                                库存数量1 = float(库存数量)
                                variations_quantity = int(库存数量1)  # Variation Quantity
                            else:
                                variations_quantity = None

                            if 运输费用 and 运输费用 != '0':
                                运输费用1 = float(运输费用)
                                shipping_price = int(运输费用1)  # Shipping Price
                            else:
                                shipping_price = None

                            if 一口价 and 一口价 != '0':
                                一口价1 = float(一口价)
                                buy_now_price = int(一口价1)  # Buy Now Price
                            else:
                                buy_now_price = None

                            if 目标价 and 目标价 != '0':
                                cost_basis = 目标价  # Target Price
                            else:
                                if shipping_price != None:
                                    cost_basis = buy_now_price + shipping_price  # Target Price
                                else:
                                    cost_basis = buy_now_price  # Target Price

                            if 零售价 and 零售价 != '0':
                                零售价1 = float(零售价)
                                retail_price = int(零售价1)  # Retail Price
                            else:
                                if shipping_price != None:
                                    retail_price = buy_now_price + shipping_price + 5  # Retail Price
                                else:
                                    retail_price = buy_now_price + 5  # Retail Price

                            if 起拍价 and 起拍价 != '0':
                                起拍价1 = float(起拍价)
                                minimum_bid_amount = int(起拍价1)  # Starting Bid
                            else:
                                minimum_bid_amount = None

                            if 底价 and 底价 != '0':
                                底价1 = float(底价)
                                reserve_price = int(底价1)  # Reserve Price
                            else:
                                reserve_price = None

                            if SFB and SFB != '0':
                                scheduling_fee_bid = float(SFB)  # Scheduling Fee Bid
                            else:
                                scheduling_fee_bid = None

                            if 最大日销售数量 and 最大日销售数量 != '0':
                                最大日销售数量1 = float(最大日销售数量)
                                max_daily_schedules = int(最大日销售数量1)  # Max Daily Schedules
                            else:
                                max_daily_schedules = None

                            if 运输费用 and 运输费用 != '0':
                                运输费用1 = float(运输费用)  # Shipping Price
                                shipping_price = int(运输费用1)  # Shipping Price
                            else:
                                shipping_price = None

                            shipping_origin = 发货地  # Ships From Country

                            # fulfillment_partner = row[0] #

                            if 运输重量 and 运输重量 != '0':
                                weight = int(运输重量)  # Shipping Weight In Ounces
                            else:
                                weight = None

                            if 处理时间 and 处理时间 != '0':
                                days_to_fulfill = int(处理时间)  # Days To Process Orde
                            else:
                                days_to_fulfill = None

                            expedited_shipping_price = None
                            expedited_days_to_deliver = None

                            buy_one_get_one_available = 是否买一得一  # Buy One Get One Available

                            if 配件价格 and 配件价格 != '0':
                                配件价格1 = float(配件价格)
                                accessory_price = int(配件价格1)  # Accessory Price

                            else:
                                accessory_price = None
                            accessory_description = 配件描述  # Accessory Description
                            campaign_name = CAMPAIGN  # campaign_name

                            if 主图序号 == '2':
                                primary_image = 产品图片2  # Primary Image URL
                            elif 主图序号 == '3':
                                primary_image = 产品图片3  # Primary Image URL
                            elif 主图序号 == '4':
                                primary_image = 产品图片4  # Primary Image URL
                            elif 主图序号 == '5':
                                primary_image = 产品图片5  # Primary Image URL
                            elif 主图序号 == '6':
                                primary_image = 产品图片6  # Primary Image URL
                            elif 主图序号 == '7':
                                primary_image = 产品图片7  # Primary Image URL
                            elif 主图序号 == '8':
                                primary_image = 产品图片8  # Primary Image URL
                            else:
                                primary_image = 产品图片1  # Primary Image URL

                            if 产品图片1 and 主图序号 != '1':
                                extra_images = 产品图片1
                            if 产品图片2 and 主图序号 != '2':
                                if 主图序号 == '1':
                                    extra_images = 产品图片2
                                else:
                                    extra_images = extra_images + '|' + 产品图片2
                            if 产品图片3 and 主图序号 != '3':
                                extra_images = extra_images + '|' + 产品图片3
                            if 产品图片4 and 主图序号 != '4':
                                extra_images = extra_images + '|' + 产品图片4
                            if 产品图片5 and 主图序号 != '5':
                                extra_images = extra_images + '|' + 产品图片5
                            if 产品图片6 and 主图序号 != '6':
                                extra_images = extra_images + '|' + 产品图片6
                            if 产品图片7 and 主图序号 != '7':
                                extra_images = extra_images + '|' + 产品图片7
                            if 产品图片8 and 主图序号 != '8':
                                extra_images = extra_images + '|' + 产品图片8

                            data_variations = {}
                            if 产品尺寸 != ['']:
                                if 产品颜色 != ['']:
                                    for 尺寸_0 in 产品尺寸:
                                        for 颜色_0 in 产品颜色:
                                            data_variations_0 = {
                                                'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + 颜色_0 + '-' + now_str_data + '][identifier]': store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + 颜色_0 + '-' + now_str_data,
                                                'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + 颜色_0 + '-' + now_str_data + '][size]': 尺寸_0,
                                                'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + 颜色_0 + '-' + now_str_data + '][color]': 颜色_0,
                                                'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + 颜色_0 + '-' + now_str_data + '][quantity]': 库存数量
                                            }
                                            data_variations.update(data_variations_0)
                                else:
                                    for 尺寸_0 in 产品尺寸:
                                        data_variations_0 = {
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + now_str_data + '][identifier]': store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + now_str_data,
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + now_str_data + '][size]': 尺寸_0,
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + now_str_data + '][color]': '',
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 尺寸_0 + '-' + now_str_data + '][quantity]': 库存数量
                                        }
                                        data_variations.update(data_variations_0)
                            else:
                                if 产品颜色 != ['']:
                                    for 颜色_0 in 产品颜色:
                                        data_variations_0 = {
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 颜色_0 + '-' + now_str_data + '][identifier]': store_name + '-' + 产品SKU + '-' + 颜色_0 + '-' + now_str_data,
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 颜色_0 + '-' + now_str_data + '][size]': '',
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 颜色_0 + '-' + now_str_data + '][color]': 颜色_0,
                                            'variations[' + store_name + '-' + 产品SKU + '-' + 颜色_0 + '-' + now_str_data + '][quantity]': 库存数量
                                        }
                                        data_variations.update(data_variations_0)
                                else:
                                    data_variations_0 = {
                                        'variations[' + store_name + '-' + 产品SKU + '-' + now_str_data + '][identifier]': store_name + '-' + 产品SKU + '-' + now_str_data,
                                        'variations[' + store_name + '-' + 产品SKU + '-' + now_str_data + '][size]': '',
                                        'variations[' + store_name + '-' + 产品SKU + '-' + now_str_data + '][color]': '',
                                        'variations[' + store_name + '-' + 产品SKU + '-' + now_str_data + '][quantity]': 库存数量
                                    }
                                    data_variations.update(data_variations_0)
                            # print(data_variations)

                            data = {
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
                                # 'reserve_price': reserve_price, #需要默认关闭，所以暂时屏蔽
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
                                'campaign_name': campaign_name
                            }
                            data.update(data_variations)

                            try:
                                subm = requests.post('https://tophatter.com/merchant_api/v1/products.json',data=data, timeout=30)
                                # print("status code:", subm.status_code, store_name)
                                if subm.status_code == 200:
                                    # 保存对应的商品信息
                                    try:
                                        index = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(identifier))
                                        if index:
                                            if SKU_price != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(identifier)).update(
                                                    SKU_price=SKU_price)
                                            if SKU_weight != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(identifier)).update(
                                                    SKU_weight=SKU_weight)
                                            if SKU_parts_price != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(identifier)).update(
                                                    SKU_parts_price=SKU_parts_price)
                                            if SKU_parts_weight != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(identifier)).update(
                                                    SKU_parts_weight=SKU_parts_weight)
                                            if SKU_variety != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(identifier)).update(
                                                    SKU_variety=SKU_variety)
                                            if HAI_SKU_freight != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(identifier)).update(
                                                    HAI_SKU_freight=HAI_SKU_freight)
                                        else:
                                            if identifier:
                                                twz = models_Tophatter.Price_Freight.objects.create(
                                                                                          USER_ID=USER_ID,
                                                                                          identifier=identifier,
                                                                                          SKU_price=SKU_price,
                                                                                          SKU_weight=SKU_weight,
                                                                                          SKU_parts_price=SKU_parts_price,
                                                                                          SKU_parts_weight=SKU_parts_weight,
                                                                                          SKU_variety=SKU_variety,
                                                                                          HAI_SKU_freight=HAI_SKU_freight,
                                                                                          )
                                                twz.save()
                                    except Exception as e:
                                        print(e)
                                    errmsg_1 = errmsg_1 + 产品SKU + '；'
                                else:
                                    errmsg_2 = errmsg_2 + 产品SKU + '(重复上传/参数错误)' + '；'
                            except Exception as e:
                                print(e)
                                errmsg_2 = errmsg_2 + 产品SKU + '(请求错误)' + '；'
                        else:
                            errmsg_2 = errmsg_2 + 产品SKU + '(必须参数没填)' + '；'
                    except Exception as e:
                        data_msg_e = {'msg_e': str(e)}
                        return HttpResponse(json.dumps(data_msg_e))
                data_msg['msg_1'] = errmsg_1
                data_msg['msg_2'] = errmsg_2
                return HttpResponse(json.dumps(data_msg))
            # 上传选中商品库产品到5M
            if FIG == 'FIG2':
                if checked_value == '':
                    data_msg_e = {'msg_e': '请选择要上传的产品'}
                    return HttpResponse(json.dumps(data_msg_e))
                if store_name_5M == '':
                    data_msg_e = {'msg_e': '请选择要上传的5M店铺'}
                    return HttpResponse(json.dumps(data_msg_e))

                now = datetime.datetime.now()
                now_str = now.strftime('%Y%m%d_%H%M%S')
                now_str_data = now.strftime('%Y%m%d')[2:]
                errmsg_1 = ''
                errmsg_2 = ''
                products_list = literal_eval(checked_value)
                for product_id in products_list:
                    # 获取自己店铺产品
                    try:
                        Product = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=product_id).values_list()
                        商品编号 = Product[0][1]
                        商品名称 = Product[0][4]
                        产品材质 = Product[0][8]
                        产品条件 = Product[0][6]
                        产品描述 = Product[0][5]
                        产品尺寸 = Product[0][11]
                        产品颜色 = Product[0][10]

                        产品尺寸 = re.sub(' ', '', 产品尺寸)
                        产品颜色 = re.sub(' ', '', 产品颜色)
                        商品编号 = re.sub(' ', '', 商品编号)

                        尺寸 = 产品尺寸.split(',')
                        颜色 = 产品颜色.split(',')
                        库存 = '10000'

                        一口价 = Product[0][33]
                        运费 = Product[0][18]
                        if 运费 == '':
                            运费 = '0'
                        运费 = re.sub('\.0', '', 运费)
                        产品分类 = Product[0][45]

                        主图序号 = Product[0][46]
                        产品图片all = Product[0][30]
                        产品图片all = 产品图片all.split('|')
                        try:
                            产品图片5m1 = 产品图片all[0]
                        except:
                            产品图片5m1 = ''

                        try:
                            产品图片5m2 = 产品图片all[1]
                        except:
                            产品图片5m2 = ''

                        try:
                            产品图片5m3 = 产品图片all[2]
                        except:
                            产品图片5m3 = ''

                        try:
                            产品图片5m4 = 产品图片all[3]
                        except:
                            产品图片5m4 = ''

                        try:
                            产品图片5m5 = 产品图片all[4]
                        except:
                            产品图片5m5 = ''

                        try:
                            产品图片5m6 = 产品图片all[5]
                        except:
                            产品图片5m6 = ''

                        try:
                            产品图片5m7 = 产品图片all[6]
                        except:
                            产品图片5m7 = ''

                        try:
                            产品图片5m8 = 产品图片all[7]
                        except:
                            产品图片5m8 = ''

                    except Exception as e:
                        print(e)
                    # 获取自己店铺产品的价格信息

                    try:
                        ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品编号).values('id').annotate(
                            SKU_price=Max('SKU_price', distinct=True)
                            , SKU_parts_price=Max('SKU_parts_price', distinct=True)
                            , SKU_weight=Max('SKU_weight', distinct=True)  # -------
                            , SKU_parts_weight=Max('SKU_parts_weight', distinct=True)  # -------
                            , SKU_variety=Max('SKU_variety', distinct=True)
                            , HAI_SKU_freight=Max('HAI_SKU_freight', distinct=True))  # -------
                        if ob:
                            SKU_price = ob[0]['SKU_price']  # 单价
                            SKU_parts_price = ob[0]['SKU_parts_price']  # 配件价
                            SKU_weight = ob[0]['SKU_weight']  # 单重量
                            SKU_parts_weight = ob[0]['SKU_parts_weight']  # 单配件重量
                            SKU_variety = ob[0]['SKU_variety']  # 单种类
                            HAI_SKU_freight = ob[0]['HAI_SKU_freight']  # 海运费用
                            if SKU_price == None:
                                SKU_price = ''
                            if SKU_parts_price == None:
                                SKU_parts_price = ''
                            if SKU_weight == None:
                                SKU_weight = ''
                            if SKU_parts_weight == None:
                                SKU_parts_weight = ''
                            if SKU_variety == None:
                                SKU_variety = ''
                            if HAI_SKU_freight == None:
                                HAI_SKU_freight = ''
                    except Exception as e:
                        print(e)
                    # 获取自己店铺产品的价格信息
                    try:
                        store_APIToken = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).filter(store_name=store_name_5M).values_list('store_APIToken')[0][0]
                        data_variations = {}
                        data_msg = {
                            'msg_1': '无',
                            'msg_2': '无',
                        }
                        if 商品编号 != '' and 商品名称 != '' and 产品分类 != '' and 产品描述 != '' and 一口价 != '' and 运费 != '':
                            goods_no = store_name_5M + '-' + 商品编号 + '-' + now_str_data  # 商品编码 *
                            name = 商品名称  # 商品名称 *
                            cat_name = 产品分类  # 产品分类 *z
                            description = 产品描述  # 产品描述

                            if 一口价 and 一口价 != '0':
                                一口价2 = float(一口价)
                                purchase_price = int(一口价2)  # 一口价 * number
                                original_sale_price = (int(一口价2) + int(运费)) * 1.5  # 原价
                                reserve_price = int(一口价2) - 1  # "保留价
                            else:
                                purchase_price = None
                                original_sale_price = None
                                reserve_price = None

                            if 运费 and 运费 != '0':
                                shipping_fee = int(运费)  # 运费
                            else:
                                shipping_fee = None

                            min_delivery_days = 7  # 预计运输天数1
                            max_delivery_days = 50  # 预计运输天数2
                            delivery_address = 'CN'  # 发货地
                            weight = ''
                            cost_price = None

                            if 主图序号 == '2':
                                main_image_url = 产品图片5m2  # Primary Image URL
                            elif 主图序号 == '3':
                                main_image_url = 产品图片5m3  # Primary Image URL
                            elif 主图序号 == '4':
                                main_image_url = 产品图片5m4  # Primary Image URL
                            elif 主图序号 == '5':
                                main_image_url = 产品图片5m5  # Primary Image URL
                            elif 主图序号 == '6':
                                main_image_url = 产品图片5m6  # Primary Image URL
                            elif 主图序号 == '7':
                                main_image_url = 产品图片5m7  # Primary Image URL
                            elif 主图序号 == '8':
                                main_image_url = 产品图片5m8  # Primary Image URL
                            else:
                                main_image_url = 产品图片5m1  # Primary Image URL

                            image_set = []
                            if 产品图片5m1 != '' and 主图序号 != '1':
                                image_set_xy = {'image_url': 产品图片5m1}
                                image_set.append(image_set_xy)
                            if 产品图片5m2 != '' and 主图序号 != '2':
                                image_set_xy = {'image_url': 产品图片5m2}
                                image_set.append(image_set_xy)
                            if 产品图片5m3 != '' and 主图序号 != '3':
                                image_set_xy = {'image_url': 产品图片5m3}
                                image_set.append(image_set_xy)
                            if 产品图片5m4 != '' and 主图序号 != '4':
                                image_set_xy = {'image_url': 产品图片5m4}
                                image_set.append(image_set_xy)
                            if 产品图片5m5 != '' and 主图序号 != '5':
                                image_set_xy = {'image_url': 产品图片5m5}
                                image_set.append(image_set_xy)
                            if 产品图片5m6 != '' and 主图序号 != '6':
                                image_set_xy = {'image_url': 产品图片5m6}
                                image_set.append(image_set_xy)
                            if 产品图片5m7 != '' and 主图序号 != '7':
                                image_set_xy = {'image_url': 产品图片5m7}
                                image_set.append(image_set_xy)
                            if 产品图片5m8 != '' and 主图序号 != '8':
                                image_set_xy = {'image_url': 产品图片5m8}
                                image_set.append(image_set_xy)
                        else:
                            data_msg_e = {'msg_e': '没有需要上传的产品 或者 没有填必填项目 '}
                            return HttpResponse(json.dumps(data_msg_e))

                        # 库存 = int(库存)
                        if 商品编号 != '' and 商品名称 != '' and 产品分类 != '' and 产品描述 != '' and 一口价 != '' and 运费 != '':
                            sku_set = []
                            if 尺寸 != ['']:
                                if 颜色 != ['']:
                                    for 尺寸_0 in 尺寸:
                                        for 颜色_0 in 颜色:
                                            data_variations_0 = {
                                                'sku_no': store_name_5M + '-' + 商品编号 + '-' + 尺寸_0 + '-' + 颜色_0 + '-' + now_str_data,
                                                'total_stock': 库存,
                                                'color': 颜色_0,
                                                'size': 尺寸_0
                                            }
                                            sku_set.append(data_variations_0)
                                else:
                                    for 尺寸_0 in 尺寸:
                                        data_variations_0 = {
                                            'sku_no': store_name_5M + '-' + 商品编号 + '-' + 尺寸_0 + '-' + now_str_data,
                                            'total_stock': 库存,
                                            'color': None,
                                            'size': 尺寸_0
                                        }
                                        sku_set.append(data_variations_0)
                            else:
                                if 颜色 != ['']:
                                    for 颜色_0 in 颜色:
                                        data_variations_0 = {
                                            'sku_no': store_name_5M + '-' + 商品编号 + '-' + 颜色_0 + '-' + now_str_data,
                                            'total_stock': 库存,
                                            'color': 颜色_0,
                                            'size': None
                                        }
                                        sku_set.append(data_variations_0)
                                else:
                                    data_variations_0 = {
                                        'sku_no': store_name_5M + '-' + 商品编号 + '-' + now_str_data,
                                        'total_stock': 库存,
                                        'color': None,
                                        'size': None
                                    }
                                    sku_set.append(data_variations_0)
                            # print(data_variations)

                            headers = {
                                'X-Api-Key': store_APIToken
                            }
                            data = {
                                'goods_no': goods_no,
                                'name': name,
                                'main_image_url': main_image_url,
                                'cat_name': cat_name,
                                'description': description,
                                'purchase_price': purchase_price,
                                'original_sale_price': original_sale_price,
                                'reserve_price': reserve_price,
                                'shipping_fee': shipping_fee,

                                'min_delivery_days': min_delivery_days,
                                'max_delivery_days': max_delivery_days,
                                'delivery_address': delivery_address,
                                'weight': None,
                                'image_set': image_set,
                                'sku_set': sku_set,
                                'detail_image_set': image_set,
                                'cost_price': cost_price,
                            }
                            data.update(data_variations)
                            # print(str(sku_set))  #data
                            # print(data)
                            try:
                                data = json.dumps(data)
                                subm = requests.post('https://hibiscus.5miles.com/api/v1/products.json', data=data, headers=headers, timeout=20)
                                print("status code:", subm.status_code, store_name_5M)
                                # aa = subm.text
                                # reponse_dicts = json.loads(aa)
                                # print(reponse_dicts)

                                if subm.status_code == 200:
                                    # 保存对应的商品信息
                                    try:
                                        index = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(goods_no))
                                        if index:
                                            if SKU_price != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(goods_no)).update(
                                                    SKU_price=SKU_price)
                                            if SKU_weight != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(goods_no)).update(
                                                    SKU_weight=SKU_weight)
                                            if SKU_parts_price != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(goods_no)).update(
                                                    SKU_parts_price=SKU_parts_price)
                                            if SKU_parts_weight != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(goods_no)).update(
                                                    SKU_parts_weight=SKU_parts_weight)
                                            if SKU_variety != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(goods_no)).update(
                                                    SKU_variety=SKU_variety)
                                            if HAI_SKU_freight != '':
                                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(goods_no)).update(
                                                    HAI_SKU_freight=HAI_SKU_freight)
                                        else:
                                            if goods_no:
                                                twz = models_Tophatter.Price_Freight.objects.create(
                                                    USER_ID=USER_ID,
                                                    identifier=goods_no,
                                                    SKU_price=SKU_price,
                                                    SKU_weight=SKU_weight,
                                                    SKU_parts_price=SKU_parts_price,
                                                    SKU_parts_weight=SKU_parts_weight,
                                                    SKU_variety=SKU_variety,
                                                    HAI_SKU_freight=HAI_SKU_freight,
                                                )
                                                twz.save()
                                    except Exception as e:
                                        print(e)

                                    errmsg_1 = errmsg_1 + store_name_5M
                                else:
                                    errmsg_2 = errmsg_2 + store_name_5M + '(参数不对)，'
                            except Exception as e:
                                # print(e)
                                errmsg_2 = errmsg_2 + store_name_5M + '(' + str(e) + '),'
                        else:
                            data_msg_e = {'msg_e': '没有需要上传的产品'}
                            return HttpResponse(json.dumps(data_msg_e))
                    except Exception as e:
                        data_msg_e = {'msg_e': str(e)}
                        print(data_msg_e)
                        return HttpResponse(json.dumps(data_msg_e))
                data_msg['msg_1'] = errmsg_1
                data_msg['msg_2'] = errmsg_2
                return HttpResponse(json.dumps(data_msg))
            # 删除商品库产品
            if FIG == 'FIG3':
                products_list = literal_eval(checked_value)
                for product_id in products_list:
                    models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=int(product_id)).delete()
                data_msg_e = {'msg_e': '删除成功: ' + checked_value}
                return HttpResponse(json.dumps(data_msg_e))

            # 搜索显示
            本站ID = request.GET.get('本站ID', '')  # 本站ID
            标准ID = request.GET.get('标准ID', '')  # 标准ID
            SKU = request.GET.get('SKU', '')  # SKU
            特征搜索 = request.GET.get('特征搜索', '')  # 特征搜索

            limit = request.GET.get('limit', '')  # 查询的每页数量   1
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

            if limit == '' and  page == '':
                store_name_users = models_Tophatter.APIAccessToken.objects.filter(USER_ID=USER_ID).values('store_name')
                store_name_users_5M  = models_five_miles.APIAccessToken_5miles.objects.filter(USER_ID=USER_ID).values('store_name')
                context0 = {
                            'store_name_users':list(store_name_users),
                            'store_name_users_5M': list(store_name_users_5M),
                            }
                return render(request, 'PruAndLog/Products_All_Own.html',context0)

            if Sort_field == '':
                Sort_field = 'updated_at'

            if Sort_order == 'desc' or Sort_order == '':
                Sort_order = '-'
            elif Sort_order == 'asc':
                Sort_order = ''
            else:
                Sort_order = '-'

            if 特征搜索 == '':
                特征搜索 = '所有商品'

            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            try:
                objs = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID)
                if 本站ID != '':
                    objs = objs.filter(id=int(本站ID))
                if 标准ID != '':
                    objs = objs.filter(standard_product_id=int(标准ID))
                if 特征搜索 != '所有商品':
                    objs = objs.filter(user_collect__contains=特征搜索)
                if SKU != '':
                    objs = objs.filter(product_name__contains=SKU)
                count_all = objs.values('product_name').count()
                objs = objs.values('id', 'product_name', 'category', 'title', 'description', 'condition', 'material',
                                   'available_quantity', 'color', 'size',
                                   'retail_price', 'cost_basis', 'minimum_bid_amount', 'scheduling_fee_bid', 'reserve_price',
                                   'shipping_price', 'shipping_origin', 'weight', 'days_to_deliver',
                                   'buy_one_get_one_available', 'all_images', 'primary_image', 'accessory_price',
                                   'accessory_description', 'buy_now_price', 'campaign_name',
                                   'user_collect', 'created_at', 'updated_at','standard_product_id').order_by(Sort_order+Sort_field)[page_star:page_end]

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
                    ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=obj['product_name']).values('id').annotate(
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
                            obj['suggest_buynows_price'] = round(((((float(obj['SKU_price']) + float(obj['SKU_freight'])) * 1.3 / exchange_rate) + 1.3) / 0.88) / 0.98, 2)  # 建议一口价
                            obj['suggest_buynows_price_5M'] = round(((((float(obj['SKU_price']) + float(obj['SKU_freight'])) * 1.35 / exchange_rate) + 1.3) / 0.82) / 0.98,2)  # 建议一口价5M
                        else:
                            obj['suggest_buynows_price'] = ''
                            obj['suggest_buynows_price_5M'] = ''
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
                        obj['suggest_buynows_price_5M'] = ''


                    obj['imgs'] = obj['all_images'].split('|')

            except Exception as e:
                print(e)

            context = {
                'code': 0,
                'msg': 'asdfgh',
                'count': count_all,
                'data': list(objs),
            }
            return HttpResponse(json.dumps(context, cls=CJsonEncoder))
        return render(request, 'PruAndLog/Products_All_Own.html')

#更新商品库信息
def owm_products_update(request):
    user_app.change_info(request, 'owm_products_updates')
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
            now = datetime.datetime.now()
            now_str = now.strftime('%Y%m%d_%H%M%S')
            now_str_data = now.strftime('%Y%m%d')[2:]

            lots_id = request.GET.get('lots_id', '')
            Top主SKU = request.GET.get('Top主SKU', '')
            商品名 = request.GET.get('商品名', '')
            SKU_5M = request.GET.get('SKU_5M', '')
            来源 = request.GET.get('来源', '')
            FIG = request.GET.get('FIG', '0')

            if FIG == '0':
                标准ID = ''

                摇钱数ID = ''
                商品名称 = ''
                产品标题 = ''
                产品材质 = ''
                产品条件 = ''
                产品尺寸 = ''
                产品颜色 = ''
                产品描述 = ''
                产品分类TOP = ''
                产品分类5M = ''

                一口价 = ''
                目标价 = '20'
                底价 = '20'
                零售价 = '20'
                SFB = '0'
                起拍价 = '1'

                发货地 = 'China'
                运输费用 = '0'
                运输重量 = ''
                处理时间 = ''
                最大日销售数量 = ''
                CAMPAIGN = ''
                配件价格 = ''
                配件描述 = ''

                产品图片1 = ''
                产品图片2 = ''
                产品图片3 = ''
                产品图片4 = ''
                产品图片5 = ''
                产品图片6 = ''
                产品图片7 = ''
                产品图片8 = ''
                主图序号 = '1'

                SKU_price = ''
                SKU_weight = ''
                SKU_parts_price = ''
                SKU_parts_weight = ''
                SKU_variety = ''
                HAI_SKU_freight = ''
                if lots_id  != ''   and 来源 ==  'TOP所有':
                    # 获取平台分析产品
                    try:
                        Product = models_common_functions.Data_TopData.objects.filter(lots_id=lots_id).values_list()
                        产品分类TOP = Product[0][8] + '|' + Product[0][9]
                        产品标题 = Product[0][7]
                        产品描述 = Product[0][13]
                        标准ID = Product[0][3]
                        if 标准ID==None:
                            标准ID=''

                        商品名称 = Product[0][2]

                        详细参数 = literal_eval(Product[0][12])
                        if 详细参数:
                            for 参数 in 详细参数:
                                if 参数[0] == 'Material':
                                    产品材质 = 参数[1]
                                if 参数[0] == 'Condition':
                                    产品条件 = 参数[1]
                                if 参数[0] == 'Available Sizes':
                                    产品尺寸 = 参数[1]
                                    产品尺寸 = re.sub('None', '', 产品尺寸)
                                if 参数[0] == 'Available Colors':
                                    产品颜色 = 参数[1]
                                    产品颜色 = re.sub('None', '', 产品颜色)

                        # 一口价 = Product[0][20]
                        # 目标价 = Product[0][13]
                        # 底价 = Product[0][17]
                        # # 底价 = re.sub('None', '', 底价)
                        # 零售价 = Product[0][21]
                        # SFB = Product[0][16]
                        起拍价 = Product[0][22]

                        # 运输费用 = Product[0][24]
                        # 运输重量 = Product[0][21]
                        # 处理时间 = Product[0][23]
                        # 处理时间 = re.sub('None', '', str(处理时间))
                        # 最大日销售数量 = Product[0][15]
                        # CAMPAIGN = Product[0][34]

                        try:
                            详细配件 = literal_eval(Product[0][29])
                            if 详细配件:
                                for 配件 in 详细配件:
                                    if 配件['description'] != None:
                                        配件价格 = 配件['amount']
                                        配件价格 = re.sub('\.0', '', 配件价格)
                                        配件描述 = 配件['description']
                        except:
                            配件价格 = ''
                            配件描述 = ''

                        产品图片1 = Product[0][14]
                        产品图片2 = Product[0][15]
                        产品图片3 = Product[0][16]
                        产品图片4 = Product[0][17]
                        产品图片5 = Product[0][18]
                        产品图片6 = Product[0][19]
                    except Exception as e:
                        print(e)
                if Top主SKU != ''   and 来源 ==  'TOP后台':
                    # 获取自己店铺产品的价格信息
                    try:
                        ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=Top主SKU).values('id').annotate(
                              SKU_price=Max('SKU_price', distinct=True)
                            , SKU_parts_price=Max('SKU_parts_price', distinct=True)
                            , SKU_weight=Max('SKU_weight', distinct=True)  # -------
                            , SKU_parts_weight=Max('SKU_parts_weight', distinct=True)  # -------
                            , SKU_variety=Max('SKU_variety', distinct=True)
                            , HAI_SKU_freight=Max('HAI_SKU_freight', distinct=True))  # -------
                        if ob:
                            SKU_price = ob[0]['SKU_price']  # 单价
                            SKU_parts_price = ob[0]['SKU_parts_price']  # 配件价
                            SKU_weight = ob[0]['SKU_weight']  # 单重量
                            SKU_parts_weight = ob[0]['SKU_parts_weight']  # 单配件重量
                            SKU_variety = ob[0]['SKU_variety']  # 单种类
                            HAI_SKU_freight = ob[0]['HAI_SKU_freight']  # 海运费用
                            if SKU_price == None:
                                SKU_price = ''
                            if SKU_parts_price == None:
                                SKU_parts_price = ''
                            if SKU_weight == None:
                                SKU_weight = ''
                            if SKU_parts_weight == None:
                                SKU_parts_weight = ''
                            if SKU_variety == None:
                                SKU_variety = ''
                            if HAI_SKU_freight == None:
                                HAI_SKU_freight = ''
                    except Exception as e:
                        print(e)
                    # 获取自己店铺产品
                    try:
                        Product = models_Tophatter.Products.objects.filter(USER_ID=USER_ID).filter(identifier=Top主SKU).values_list()
                        产品分类TOP = Product[0][6]
                        产品分类TOP = str(产品分类TOP)
                        if 产品分类TOP == '':
                            产品分类TOP = '|'

                        标准ID = Product[0][5]
                        if 标准ID == None:
                            标准ID = ''

                        底价 = Product[0][19]
                        # 底价 = re.sub('None', '', 底价)
                        目标价 = Product[0][15]
                        # 目标价 = re.sub('\.0', '', str(目标价))
                        # 发货地 = Product[0][21]
                        CAMPAIGN = Product[0][36]
                        一口价 = Product[0][35]
                        一口价 = re.sub('\.0', '', str(一口价))
                        加售 = literal_eval(Product[0][29])
                        if len(加售) == 1:
                            配件价格 = str(加售[0]['amount'])
                            配件价格 = re.sub('\.0', '', 配件价格)
                            配件描述 = 加售[0]['description']
                        elif len(加售) == 2:
                            配件价格 = str(加售[1]['amount'])
                            配件价格 = re.sub('\.0', '', 配件价格)
                            配件描述 = 加售[1]['description']

                        产品标题 = Product[0][7]
                        产品材质 = Product[0][11]
                        if 产品材质 == None:
                            产品材质 = ''
                        产品条件 = Product[0][9]
                        if 产品条件 == None:
                            产品条件 = ''
                        产品描述 = Product[0][8]
                        产品尺寸 = ''
                        产品颜色 = ''
                        尺寸1 = ''
                        颜色1 = ''
                        for 尺寸0 in literal_eval(Product[0][13]):
                            if 尺寸0['size'] != 尺寸1:
                                产品尺寸 = 产品尺寸 + str(尺寸0['size']) + ','
                            尺寸1 = 尺寸0['size']
                        for 颜色0 in literal_eval(Product[0][13]):
                            if 颜色0['color'] != 颜色1:
                                产品颜色 = 产品颜色 + str(颜色0['color']) + ','
                            颜色1 = 颜色0['color']
                        产品尺寸 = re.sub('None,', '', 产品尺寸)
                        产品颜色 = re.sub('None,', '', 产品颜色)
                        if 产品尺寸 != '':
                            产品尺寸 = 产品尺寸[:-1]
                        if 产品颜色 != '':
                            产品颜色 = 产品颜色[:-1]

                        产品图片1 = Product[0][30]
                        产品图片all = Product[0][31]
                        产品图片all = 产品图片all.split('|')
                        try:
                            产品图片2 = 产品图片all[0]
                        except:
                            产品图片2 = ''

                        try:
                            产品图片3 = 产品图片all[1]
                        except:
                            产品图片3 = ''

                        try:
                            产品图片4 = 产品图片all[2]
                        except:
                            产品图片4 = ''

                        try:
                            产品图片5 = 产品图片all[3]
                        except:
                            产品图片5 = ''

                        try:
                            产品图片6 = 产品图片all[4]
                        except:
                            产品图片6 = ''

                        try:
                            产品图片7 = 产品图片all[5]
                        except:
                            产品图片7 = ''

                        try:
                            产品图片8 = 产品图片all[6]
                        except:
                            产品图片8 = ''
                    except Exception as e:
                        print(e)
                if 商品名   != ''   and 来源 ==  '商品库':
                    # 获取自己店铺产品的价格信息
                    try:
                        ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=str(商品名)).values('id').annotate(
                            SKU_price=Max('SKU_price', distinct=True)
                            , SKU_parts_price=Max('SKU_parts_price', distinct=True)
                            , SKU_weight=Max('SKU_weight', distinct=True)  # -------
                            , SKU_parts_weight=Max('SKU_parts_weight', distinct=True)  # -------
                            , SKU_variety=Max('SKU_variety', distinct=True)
                            , HAI_SKU_freight=Max('HAI_SKU_freight', distinct=True))  # -------
                        if ob:
                            SKU_price = ob[0]['SKU_price']  # 单价
                            SKU_parts_price = ob[0]['SKU_parts_price']  # 配件价
                            SKU_weight = ob[0]['SKU_weight']  # 单重量
                            SKU_parts_weight = ob[0]['SKU_parts_weight']  # 单配件重量
                            SKU_variety = ob[0]['SKU_variety']  # 单种类
                            HAI_SKU_freight = ob[0]['HAI_SKU_freight']  # 海运费用
                            if SKU_price == None:
                                SKU_price = ''
                            if SKU_parts_price == None:
                                SKU_parts_price = ''
                            if SKU_weight == None:
                                SKU_weight = ''
                            if SKU_parts_weight == None:
                                SKU_parts_weight = ''
                            if SKU_variety == None:
                                SKU_variety = ''
                            if HAI_SKU_freight == None:
                                HAI_SKU_freight = ''
                    except Exception as e:
                        print(e)
                    # 获取自己商品库产品
                    try:
                        Product = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(product_name=str(商品名)).values_list()
                        标准ID = Product[0][42]
                        if 标准ID == None:
                            标准ID = ''

                        摇钱数ID = Product[0][0]
                        商品名称 = Product[0][1]
                        产品分类TOP = Product[0][3]
                        产品分类5M = Product[0][45]
                        if 产品分类5M :
                            产品分类5M = 产品分类5M
                        else:
                            产品分类5M=''
                        产品标题 = Product[0][4]
                        产品材质 = Product[0][8]
                        产品条件 = Product[0][6]
                        产品描述 = Product[0][5]
                        产品尺寸 = Product[0][11]
                        产品颜色 = Product[0][10]

                        一口价 = Product[0][33]
                        一口价 = re.sub('\.0', '', str(一口价))
                        目标价 = Product[0][13]
                        底价 = Product[0][17]
                        # 底价 = re.sub('None', '', 底价)
                        零售价 = Product[0][12]
                        SFB = Product[0][16]
                        起拍价 = Product[0][14]

                        运输费用 = Product[0][18]
                        运输重量 = Product[0][21]
                        处理时间 = Product[0][23]
                        处理时间 = re.sub('None', '', str(处理时间))
                        最大日销售数量 = Product[0][15]
                        CAMPAIGN = Product[0][34]
                        配件价格 = Product[0][27]
                        配件描述 = Product[0][28]

                        主图序号 = Product[0][46]
                        if 主图序号 == None or 主图序号 == '':
                            主图序号 = '1'
                        产品图片all = Product[0][30]
                        产品图片all = 产品图片all.split('|')
                        try:
                            产品图片1 = 产品图片all[0]
                        except:
                            产品图片1 = ''

                        try:
                            产品图片2 = 产品图片all[1]
                        except:
                            产品图片2 = ''

                        try:
                            产品图片3 = 产品图片all[2]
                        except:
                            产品图片3 = ''

                        try:
                            产品图片4 = 产品图片all[3]
                        except:
                            产品图片4 = ''

                        try:
                            产品图片5 = 产品图片all[4]
                        except:
                            产品图片5 = ''

                        try:
                            产品图片6 = 产品图片all[5]
                        except:
                            产品图片6 = ''

                        try:
                            产品图片7 = 产品图片all[6]
                        except:
                            产品图片7 = ''

                        try:
                            产品图片8 = 产品图片all[7]
                        except:
                            产品图片8 = ''
                    except Exception as e:
                        print(e)
                if SKU_5M   != ''   and 来源 ==  '5miles':
                    # 获取自己店铺产品的价格信息
                    try:
                        ob = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=SKU_5M).values('id').annotate(
                            SKU_price=Max('SKU_price', distinct=True)
                            , SKU_parts_price=Max('SKU_parts_price', distinct=True)
                            , SKU_weight=Max('SKU_weight', distinct=True)  # -------
                            , SKU_parts_weight=Max('SKU_parts_weight', distinct=True)  # -------
                            , SKU_variety=Max('SKU_variety', distinct=True)
                            , HAI_SKU_freight=Max('HAI_SKU_freight', distinct=True))  # -------
                        if ob:
                            SKU_price = ob[0]['SKU_price']  # 单价
                            SKU_parts_price = ob[0]['SKU_parts_price']  # 配件价
                            SKU_weight = ob[0]['SKU_weight']  # 单重量
                            SKU_parts_weight = ob[0]['SKU_parts_weight']  # 单配件重量
                            SKU_variety = ob[0]['SKU_variety']  # 单种类
                            HAI_SKU_freight = ob[0]['HAI_SKU_freight']  # 海运费用
                            if SKU_price == None:
                                SKU_price = ''
                            if SKU_parts_price == None:
                                SKU_parts_price = ''
                            if SKU_weight == None:
                                SKU_weight = ''
                            if SKU_parts_weight == None:
                                SKU_parts_weight = ''
                            if SKU_variety == None:
                                SKU_variety = ''
                            if HAI_SKU_freight == None:
                                HAI_SKU_freight = ''
                    except Exception as e:
                        print(e)
                    # 获取自己5M店铺产品
                    try:
                        Product = models_five_miles.Products_5miles.objects.filter(USER_ID=USER_ID).filter(goods_no=SKU_5M).values_list()

                        产品标题 = Product[0][12]
                        产品描述 = Product[0][13]
                        产品分类5M = Product[0][5]
                        一口价 = str(Product[0][8])
                        一口价 = re.sub('\.0', '', 一口价)

                        产品尺寸 = ''
                        产品颜色 = ''
                        尺寸1 = ''
                        颜色1 = ''
                        for 尺寸0 in literal_eval(Product[0][20]):
                            if 尺寸0['size'] != 尺寸1:
                                产品尺寸 = 产品尺寸 + str(尺寸0['size']) + ','
                            尺寸1 = 尺寸0['size']
                        for 颜色0 in literal_eval(Product[0][20]):
                            if 颜色0['color'] != 颜色1:
                                产品颜色 = 产品颜色 + str(颜色0['color']) + ','
                            颜色1 = 颜色0['color']

                        产品尺寸 = re.sub('None,', '', 产品尺寸)
                        产品颜色 = re.sub('None,', '', 产品颜色)
                        if 产品尺寸 != '':
                            产品尺寸 = 产品尺寸[:-1]
                        if 产品颜色 != '':
                            产品颜色 = 产品颜色[:-1]

                        产品图片1 = Product[0][14]
                        产品图片all = []
                        for img in literal_eval(Product[0][19]):
                            产品图片all.append(img['image_url'])
                        try:
                            产品图片2 = 产品图片all[0]
                        except:
                            产品图片2 = ''

                        try:
                            产品图片3 = 产品图片all[1]
                        except:
                            产品图片3 = ''

                        try:
                            产品图片4 = 产品图片all[2]
                        except:
                            产品图片4 = ''

                        try:
                            产品图片5 = 产品图片all[3]
                        except:
                            产品图片5 = ''

                        try:
                            产品图片6 = 产品图片all[4]
                        except:
                            产品图片6 = ''

                        try:
                            产品图片7 = 产品图片all[5]
                        except:
                            产品图片7 = ''

                        try:
                            产品图片8 = 产品图片all[6]
                        except:
                            产品图片8 = ''
                    except Exception as e:
                        print(e)
                campaign_listes = models_Tophatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(Q(status='Active')|Q(status='active')).values('name').distinct().order_by('name')
                context = {
                    'EXCHANGE_RATE': exchange_rate,
                    'lots_id': lots_id,
                    'Top主SKU': Top主SKU,
                    '商品名': 商品名,
                    'SKU_5M': SKU_5M,

                    '标准ID':标准ID,
                    '摇钱数ID': 摇钱数ID,
                    '商品名称': 商品名称,
                    '产品标题': 产品标题,
                    '产品材质': 产品材质,
                    '产品条件': 产品条件,
                    '产品尺寸': 产品尺寸,
                    '产品颜色': 产品颜色,
                    '产品描述': 产品描述,
                    '产品分类TOP': 产品分类TOP,
                    '产品分类5M': 产品分类5M,

                    '一口价': 一口价,
                    '目标价': 目标价,
                    '底价': 底价,
                    '零售价': 零售价,
                    'SFB': SFB,
                    '起拍价': 起拍价,

                    '运输费用': 运输费用,
                    '运输重量': 运输重量,
                    '处理时间': 处理时间,
                    '最大日销售数量': 最大日销售数量,
                    'CAMPAIGN': CAMPAIGN,
                    '配件价格': 配件价格,
                    '配件描述': 配件描述,

                    '产品图片1': 产品图片1,
                    '产品图片2': 产品图片2,
                    '产品图片3': 产品图片3,
                    '产品图片4': 产品图片4,
                    '产品图片5': 产品图片5,
                    '产品图片6': 产品图片6,
                    '产品图片7': 产品图片7,
                    '产品图片8': 产品图片8,
                    '主图序号':主图序号,

                    'SKU_price': SKU_price,
                    'SKU_weight': SKU_weight,
                    'SKU_parts_price': SKU_parts_price,
                    'SKU_parts_weight': SKU_parts_weight,
                    'SKU_variety': SKU_variety,
                    'HAI_SKU_freight': HAI_SKU_freight,

                    'campaign_listes': list(campaign_listes),
                }
                return render(request, 'PruAndLog/own_products_update.html', context)
            if FIG == 'FIG':
                标准ID = request.GET.get('标准ID', '')
                if 标准ID == '':
                    标准ID = None
                else:
                    标准ID = int(标准ID)

                主图序号 = request.GET.get('主图序号', '')
                产品图片1 = request.GET.get('产品图片1', '')
                产品图片2 = request.GET.get('产品图片2', '')
                产品图片3 = request.GET.get('产品图片3', '')
                产品图片4 = request.GET.get('产品图片4', '')
                产品图片5 = request.GET.get('产品图片5', '')
                产品图片6 = request.GET.get('产品图片6', '')
                产品图片7 = request.GET.get('产品图片7', '')
                产品图片8 = request.GET.get('产品图片8', '')
                if 主图序号 == '1':
                    产品主图 = 产品图片1
                elif 主图序号 == '2':
                    产品主图 = 产品图片2
                elif 主图序号 == '3':
                    产品主图 = 产品图片3
                elif 主图序号 == '4':
                    产品主图 = 产品图片4
                elif 主图序号 == '5':
                    产品主图 = 产品图片5
                elif 主图序号 == '6':
                    产品主图 = 产品图片6
                elif 主图序号 == '7':
                    产品主图 = 产品图片7
                elif 主图序号 == '8':
                    产品主图 = 产品图片8
                else:
                    产品主图 = 产品图片1

                一口价 = request.GET.get('一口价', '')
                目标价 = request.GET.get('目标价', '')
                零售价 = request.GET.get('零售价', '')
                底价 = '20'
                起拍价 = request.GET.get('起拍价', '')
                SFB = request.GET.get('SFB', '')
                运输费用 = request.GET.get('运输费用', '')

                商品名称 = request.GET.get('商品名称', '')
                产品分类TOP = request.GET.get('产品分类TOP', '')
                产品分类5M = request.GET.get('产品分类5M', '')

                SKU_price = request.GET.get('SKU_price', '')
                SKU_weight = request.GET.get('SKU_weight', '')
                SKU_parts_price = request.GET.get('SKU_parts_price', '')
                SKU_parts_weight = request.GET.get('SKU_parts_weight', '')
                SKU_variety = request.GET.get('SKU_variety', '')
                HAI_SKU_freight = request.GET.get('HAI_SKU_freight', '')

                摇钱数ID = request.GET.get('摇钱数ID', '')
                if 摇钱数ID == '':
                    摇钱数ID = '0'


                产品条件 = request.GET.get('产品条件', '')
                产品材质 = request.GET.get('产品材质', '')
                CAMPAIGN = request.GET.get('CAMPAIGN', '')
                产品尺寸 = request.GET.get('产品尺寸', '')
                产品颜色 = request.GET.get('产品颜色', '')
                配件价格 = request.GET.get('配件价格', '')
                配件描述 = request.GET.get('配件描述', '')
                产品标题 = request.GET.get('产品标题', '')
                产品描述 = request.GET.get('产品描述', '')

                库存数量 =  '10000'
                运输重量 = '0'
                处理时间 = '5'
                发货地 =  'China'
                最大日销售数量 = '1000'
                是否买一得一 = ''
                if 一口价 == '' or 起拍价=='' or SFB==''or 运输费用==''or 商品名称=='' or 产品条件=='' or 产品标题==''or 产品描述=='':
                    data_msg_e = {'msg_e': '失败，请填写必要信息 '}
                    return HttpResponse(json.dumps(data_msg_e))

                idenx = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=int(摇钱数ID))
                if idenx:
                    try:
                        if 产品分类TOP != '|' and 产品分类TOP != '':
                            OLD_商品特征 = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=int(摇钱数ID)).values('user_collect')
                            OLD_商品特征 = OLD_商品特征[0]['user_collect']
                            OLD_商品特征 = re.sub('None', '', str(OLD_商品特征))
                            OLD_商品特征 = re.sub(',TOP', '', str(OLD_商品特征))
                            NEW_商品特征 = OLD_商品特征 + ',' + 'TOP'
                            models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=int(摇钱数ID)).update(user_collect=NEW_商品特征)
                        if 产品分类5M != '':
                            OLD_商品特征 = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=int(摇钱数ID)).values('user_collect')
                            OLD_商品特征 = OLD_商品特征[0]['user_collect']
                            OLD_商品特征 = re.sub('None', '', str(OLD_商品特征))
                            OLD_商品特征 = re.sub(',5M', '', str(OLD_商品特征))
                            NEW_商品特征 = OLD_商品特征 + ',' + '5M'
                            models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=int(摇钱数ID)).update(user_collect=NEW_商品特征)

                        models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID).filter(id=int(摇钱数ID)) \
                            .update(product_name=商品名称,
                                    internal_id=None,
                                    category=产品分类TOP,
                                    cat_name=产品分类5M,
                                    title=产品标题,
                                    description=产品描述,
                                    condition=产品条件,
                                    # brand='',
                                    material=产品材质,
                                    available_quantity=库存数量,
                                    color=产品颜色,
                                    size=产品尺寸,

                                    retail_price=零售价,
                                    cost_basis=目标价,
                                    minimum_bid_amount=起拍价,
                                    max_daily_schedules=最大日销售数量,
                                    scheduling_fee_bid=SFB,
                                    reserve_price=底价,
                                    shipping_price=运输费用,
                                    shipping_origin=发货地,
                                    # fulfillment_partner='',
                                    weight=运输重量,
                                    days_to_deliver=处理时间,
                                    # days_to_fulfill='',

                                    # expedited_shipping_price=expedited_shipping_price,
                                    # expedited_days_to_deliver=expedited_days_to_deliver,
                                    buy_one_get_one_available=是否买一得一,
                                    # upsells=upsells,
                                    accessory_price=配件价格,
                                    accessory_description=配件描述,

                                    主图序号=主图序号,
                                    primary_image=产品主图,
                                    all_images=产品图片1 + '|' + 产品图片2 + '|' + 产品图片3 + '|' + 产品图片4 + '|' + 产品图片5 + '|' + 产品图片6 + '|' + 产品图片7 + '|' + 产品图片8,
                                    # ratings_count='',
                                    # ratings_average='',
                                    campaign_name=CAMPAIGN,
                                    buy_now_price=一口价,

                                    # created_at=created_at,
                                    updated_at=now,
                                    # disabled_at=disabled_at

                                    standard_product_id = 标准ID,
                                    )
                        # 保存对应的商品信息
                        index = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称)
                        if index:
                            if SKU_price != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_price=SKU_price)
                            if SKU_weight != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_weight=SKU_weight)
                            if SKU_parts_price != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_parts_price=SKU_parts_price)
                            if SKU_parts_weight != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_parts_weight=SKU_parts_weight)
                            if SKU_variety != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_variety=SKU_variety)

                            if HAI_SKU_freight != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    HAI_SKU_freight=HAI_SKU_freight)
                        else:
                            if 商品名称:
                                twz = models_Tophatter.Price_Freight.objects.create(
                                                                          USER_ID=USER_ID,
                                                                          identifier=商品名称,
                                                                          SKU_price=SKU_price,
                                                                          SKU_weight=SKU_weight,
                                                                          SKU_parts_price=SKU_parts_price,
                                                                          SKU_parts_weight=SKU_parts_weight,
                                                                          SKU_variety=SKU_variety,

                                                                          HAI_SKU_freight=HAI_SKU_freight,
                                                                          )
                                twz.save()
                        data_msg_e = {'msg_e': '替换成功 '}
                        return HttpResponse(json.dumps(data_msg_e))
                    except Exception as e:
                        print(e)
                        data_msg_e = {'msg_e': '替换失败: ' + str(e)}
                        return HttpResponse(json.dumps(data_msg_e))
                else:
                    NEW_商品特征 = ''
                    if 产品分类TOP != '|' and 产品分类TOP != '':
                        NEW_商品特征 =  ',TOP'
                    if 产品分类5M != '':
                        NEW_商品特征 = NEW_商品特征 + ',' + '5M'
                    try:
                        twz = models_PruAndLog.Products_All_Own.objects.create(
                            USER_ID=USER_ID,
                            product_name=商品名称,
                            internal_id=None,
                            category=产品分类TOP,
                            cat_name=产品分类5M,
                            title=产品标题,
                            description=产品描述,
                            condition=产品条件,
                            # brand='',
                            material=产品材质,
                            available_quantity=库存数量,
                            color=产品颜色,
                            size=产品尺寸,

                            retail_price=零售价,
                            cost_basis=目标价,
                            minimum_bid_amount=起拍价,
                            max_daily_schedules=最大日销售数量,
                            scheduling_fee_bid=SFB,
                            reserve_price=底价,
                            shipping_price=运输费用,
                            shipping_origin=发货地,
                            # fulfillment_partner='',
                            weight=运输重量,
                            days_to_deliver=处理时间,
                            # days_to_fulfill='',

                            # expedited_shipping_price=expedited_shipping_price,
                            # expedited_days_to_deliver=expedited_days_to_deliver,
                            buy_one_get_one_available=是否买一得一,
                            # upsells=upsells,
                            accessory_price=配件价格,
                            accessory_description=配件描述,

                            主图序号=主图序号,
                            primary_image=产品主图,
                            all_images=产品图片1 + '|' + 产品图片2 + '|' + 产品图片3 + '|' + 产品图片4 + '|' + 产品图片5 + '|' + 产品图片6 + '|' + 产品图片7 + '|' + 产品图片8,
                            # ratings_count='',
                            # ratings_average='',
                            campaign_name=CAMPAIGN,
                            buy_now_price=一口价,

                            created_at=now,
                            updated_at=now,
                            # disabled_at=disabled_at

                            standard_product_id=标准ID,
                            user_collect=NEW_商品特征,
                        )
                        twz.save()
                        # 保存对应的商品信息
                        index = models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称)
                        if index:
                            if SKU_price != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_price=SKU_price)
                            if SKU_weight != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_weight=SKU_weight)
                            if SKU_parts_price != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_parts_price=SKU_parts_price)
                            if SKU_parts_weight != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_parts_weight=SKU_parts_weight)
                            if SKU_variety != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    SKU_variety=SKU_variety)

                            if HAI_SKU_freight != '':
                                models_Tophatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(identifier=商品名称).update(
                                    HAI_SKU_freight=HAI_SKU_freight)
                        else:
                            if 商品名称:
                                twz = models_Tophatter.Price_Freight.objects.create(
                                    USER_ID=USER_ID,
                                    identifier=商品名称,
                                    SKU_price=SKU_price,
                                    SKU_weight=SKU_weight,
                                    SKU_parts_price=SKU_parts_price,
                                    SKU_parts_weight=SKU_parts_weight,
                                    SKU_variety=SKU_variety,

                                    HAI_SKU_freight=HAI_SKU_freight,
                                )
                                twz.save()
                        data_msg_e = {'msg_e': '创建成功 '}
                        return HttpResponse(json.dumps(data_msg_e))
                    except Exception as e:
                        print(e)
                        data_msg_e = {'msg_e': '创建失败: ' + str(e)}
                        return HttpResponse(json.dumps(data_msg_e))

#基本参数
def key_parameter(request):
    user_app.change_info(request, 'owm_products_updates')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
        return render(request, '../../user_app/templates/404.html')
    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
                设置参数 = request.GET.get('设置参数', '')
                if 设置参数 == '设置参数':
                    打包成本设置 = request.GET.get('打包成本设置', '')
                    ind = models_PruAndLog.key_parameter.objects.filter(USER_ID=USER_ID).values('打包成本').first()['打包成本']
                    try :
                        if ind:
                            models_PruAndLog.key_parameter.objects.filter(USER_ID=USER_ID).update(打包成本=打包成本设置,save_time=datetime.datetime.now())
                            data_msg_e = {'Detailed_orders':'0','msg_e': '替换成功'}
                            return HttpResponse(json.dumps(data_msg_e))
                        else:
                            models_PruAndLog.key_parameter.objects.create(USER_ID=USER_ID,打包成本=打包成本设置,save_time=datetime.datetime.now()).save()
                            data_msg_e = {'Detailed_orders':'1','msg_e': '保存成功'}
                            return HttpResponse(json.dumps(data_msg_e))
                    except:
                        data_msg_e = {'Detailed_orders': '2', 'msg_e': '失败'}
                        return HttpResponse(json.dumps(data_msg_e))

                try:
                    打包成本 = models_PruAndLog.key_parameter.objects.filter(USER_ID=USER_ID).values('打包成本').first()['打包成本']
                except:
                    打包成本 = 1.8
                context = {
                    '打包成本': 打包成本,
                }
                return render(request, 'PruAndLog/key_parameter.html', context)

#物流信息
def logistics_statistic(request):
    user_app.change_info(request, 'TOP_seller')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID','PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            caozuo_status = request.GET.get('caozuo_status', '')

            #编辑已有数据
            if caozuo_status== '保存':
                美国_每克_普货 = request.GET.get('美国_每克_普货', '')
                美国_每克_带电 = request.GET.get('美国_每克_带电', '')
                美国_每克_特货 = request.GET.get('美国_每克_特货', '')
                美国_挂号_普货 = request.GET.get('美国_挂号_普货', '')
                美国_挂号_带电 = request.GET.get('美国_挂号_带电', '')
                美国_挂号_特货 = request.GET.get('美国_挂号_特货', '')
                美国_销售比 = request.GET.get('美国_销售比', '')
                美国_折扣_普货 = request.GET.get('美国_折扣_普货', '')
                美国_折扣_带电 = request.GET.get('美国_折扣_带电', '')
                美国_折扣_特货 = request.GET.get('美国_折扣_特货', '')

                英国_每克_普货 = request.GET.get('英国_每克_普货', '')
                英国_每克_带电 = request.GET.get('英国_每克_带电', '')
                英国_每克_特货 = request.GET.get('英国_每克_特货', '')
                英国_挂号_普货 = request.GET.get('英国_挂号_普货', '')
                英国_挂号_带电 = request.GET.get('英国_挂号_带电', '')
                英国_挂号_特货 = request.GET.get('英国_挂号_特货', '')
                英国_销售比 = request.GET.get('英国_销售比', '')
                英国_折扣_普货 = request.GET.get('英国_折扣_普货', '')
                英国_折扣_带电 = request.GET.get('英国_折扣_带电', '')
                英国_折扣_特货 = request.GET.get('英国_折扣_特货', '')

                加拿_每克_普货 = request.GET.get('加拿_每克_普货', '')
                加拿_每克_带电 = request.GET.get('加拿_每克_带电', '')
                加拿_每克_特货 = request.GET.get('加拿_每克_特货', '')
                加拿_挂号_普货 = request.GET.get('加拿_挂号_普货', '')
                加拿_挂号_带电 = request.GET.get('加拿_挂号_带电', '')
                加拿_挂号_特货 = request.GET.get('加拿_挂号_特货', '')
                加拿_销售比 = request.GET.get('加拿_销售比', '')
                加拿_折扣_普货 = request.GET.get('加拿_折扣_普货', '')
                加拿_折扣_带电 = request.GET.get('加拿_折扣_带电', '')
                加拿_折扣_特货 = request.GET.get('加拿_折扣_特货', '')

                澳大_每克_普货 = request.GET.get('澳大_每克_普货', '')
                澳大_每克_带电 = request.GET.get('澳大_每克_带电', '')
                澳大_每克_特货 = request.GET.get('澳大_每克_特货', '')
                澳大_挂号_普货 = request.GET.get('澳大_挂号_普货', '')
                澳大_挂号_带电 = request.GET.get('澳大_挂号_带电', '')
                澳大_挂号_特货 = request.GET.get('澳大_挂号_特货', '')
                澳大_销售比 = request.GET.get('澳大_销售比', '')
                澳大_折扣_普货 = request.GET.get('澳大_折扣_普货', '')
                澳大_折扣_带电 = request.GET.get('澳大_折扣_带电', '')
                澳大_折扣_特货 = request.GET.get('澳大_折扣_特货', '')

                TIME = request.GET.get('TIME', '')
                if TIME == '':
                    TIME = datetime.datetime.now().date().strftime('%Y-%m-%d')
                if 美国_每克_普货 != '' and 美国_每克_带电 != '' and 美国_每克_特货 != '':
                    try:
                        twzz = models_Tophatter.logistics_statistic.objects.create(
                            USER_ID=USER_ID,
                            STAR_DATE=datetime.datetime.now().date(),
                            END_DATE=datetime.datetime.now().date(),
                            美国_每克_普货=美国_每克_普货,
                            美国_每克_带电=美国_每克_带电,
                            美国_每克_特货=美国_每克_特货,
                            美国_挂号_普货=美国_挂号_普货,
                            美国_挂号_带电=美国_挂号_带电,
                            美国_挂号_特货=美国_挂号_特货,
                            美国_销售比=美国_销售比,
                            美国_折扣_普货=美国_折扣_普货,
                            美国_折扣_带电=美国_折扣_带电,
                            美国_折扣_特货=美国_折扣_特货,

                            英国_每克_普货=英国_每克_普货,
                            英国_每克_带电=英国_每克_带电,
                            英国_每克_特货=英国_每克_特货,
                            英国_挂号_普货=英国_挂号_普货,
                            英国_挂号_带电=英国_挂号_带电,
                            英国_挂号_特货=英国_挂号_特货,
                            英国_销售比=英国_销售比,
                            英国_折扣_普货=英国_折扣_普货,
                            英国_折扣_带电=英国_折扣_带电,
                            英国_折扣_特货=英国_折扣_特货,

                            加拿_每克_普货=加拿_每克_普货,
                            加拿_每克_带电=加拿_每克_带电,
                            加拿_每克_特货=加拿_每克_特货,
                            加拿_挂号_普货=加拿_挂号_普货,
                            加拿_挂号_带电=加拿_挂号_带电,
                            加拿_挂号_特货=加拿_挂号_特货,
                            加拿_销售比=加拿_销售比,
                            加拿_折扣_普货=加拿_折扣_普货,
                            加拿_折扣_带电=加拿_折扣_带电,
                            加拿_折扣_特货=加拿_折扣_特货,

                            澳大_每克_普货=澳大_每克_普货,
                            澳大_每克_带电=澳大_每克_带电,
                            澳大_每克_特货=澳大_每克_特货,
                            澳大_挂号_普货=澳大_挂号_普货,
                            澳大_挂号_带电=澳大_挂号_带电,
                            澳大_挂号_特货=澳大_挂号_特货,
                            澳大_销售比=澳大_销售比,
                            澳大_折扣_普货=澳大_折扣_普货,
                            澳大_折扣_带电=澳大_折扣_带电,
                            澳大_折扣_特货=澳大_折扣_特货,
                        )
                        twzz.save()
                        data_msg_e = {'Detailed_orders': '1', 'msg_e': '保存成功'}
                        return HttpResponse(json.dumps(data_msg_e))
                    except Exception as e:
                        print(e)
                        models_Tophatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(STAR_DATE=TIME).update(
                            END_DATE=datetime.datetime.now().date(),
                            美国_每克_普货=美国_每克_普货,
                            美国_每克_带电=美国_每克_带电,
                            美国_每克_特货=美国_每克_特货,
                            美国_挂号_普货=美国_挂号_普货,
                            美国_挂号_带电=美国_挂号_带电,
                            美国_挂号_特货=美国_挂号_特货,
                            美国_销售比=美国_销售比,
                            美国_折扣_普货=美国_折扣_普货,
                            美国_折扣_带电=美国_折扣_带电,
                            美国_折扣_特货=美国_折扣_特货,

                            英国_每克_普货=英国_每克_普货,
                            英国_每克_带电=英国_每克_带电,
                            英国_每克_特货=英国_每克_特货,
                            英国_挂号_普货=英国_挂号_普货,
                            英国_挂号_带电=英国_挂号_带电,
                            英国_挂号_特货=英国_挂号_特货,
                            英国_销售比=英国_销售比,
                            英国_折扣_普货=英国_折扣_普货,
                            英国_折扣_带电=英国_折扣_带电,
                            英国_折扣_特货=英国_折扣_特货,

                            加拿_每克_普货=加拿_每克_普货,
                            加拿_每克_带电=加拿_每克_带电,
                            加拿_每克_特货=加拿_每克_特货,
                            加拿_挂号_普货=加拿_挂号_普货,
                            加拿_挂号_带电=加拿_挂号_带电,
                            加拿_挂号_特货=加拿_挂号_特货,
                            加拿_销售比=加拿_销售比,
                            加拿_折扣_普货=加拿_折扣_普货,
                            加拿_折扣_带电=加拿_折扣_带电,
                            加拿_折扣_特货=加拿_折扣_特货,

                            澳大_每克_普货=澳大_每克_普货,
                            澳大_每克_带电=澳大_每克_带电,
                            澳大_每克_特货=澳大_每克_特货,
                            澳大_挂号_普货=澳大_挂号_普货,
                            澳大_挂号_带电=澳大_挂号_带电,
                            澳大_挂号_特货=澳大_挂号_特货,
                            澳大_销售比=澳大_销售比,
                            澳大_折扣_普货=澳大_折扣_普货,
                            澳大_折扣_带电=澳大_折扣_带电,
                            澳大_折扣_特货=澳大_折扣_特货,
                        )
                        data_msg_e = {'Detailed_orders': '0', 'msg_e': '替换成功'}
                        return HttpResponse(json.dumps(data_msg_e))


            try:
                objs = models_Tophatter.logistics_statistic.objects.filter(USER_ID=USER_ID).values().last()
                if objs:
                    objs = objs
                else:
                    objs = models_Tophatter.logistics_statistic.objects.filter(USER_ID=0).values().last()
            except Exception as e:
                objs = models_Tophatter.logistics_statistic.objects.filter(USER_ID=0).values().last()

            context = {
                'LogDatas': objs,
            }
            return render(request, 'PruAndLog/logistics_statistic.html',context)

#汇率信息
def exchange_rate_show(request):
    user_app.change_info(request, 'TOP_seller')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID','PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            # 销售数量及均价总览
            Exchange_Rate_0 = []
            Exchange_Rate = []
            try:
                exchange_rates = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate_0','exchange_rate','save_time')

                for exchange_rate in exchange_rates:
                    exchange_rate['exchange_rate_old'] = [0, 0]
                    exchange_rate['exchange_rate_new'] = [0, 0]
                    this_date = exchange_rate['save_time']
                    this_date = time.mktime(this_date.timetuple())

                    exchange_rate['exchange_rate_old'][0] = this_date * 1000
                    exchange_rate['exchange_rate_old'][1] = round(exchange_rate['exchange_rate_0'], 2)
                    Exchange_Rate_0.append(exchange_rate['exchange_rate_old'])

                    exchange_rate['exchange_rate_new'][0] = this_date * 1000
                    exchange_rate['exchange_rate_new'][1] = round(exchange_rate['exchange_rate'], 2)
                    Exchange_Rate.append(exchange_rate['exchange_rate_new'])
            except Exception as e:
                print(e)
            context = {
                'Exchange_Rate_0': Exchange_Rate_0,
                'Exchange_Rate': Exchange_Rate,
            }

            return render(request, 'PruAndLog/exchange_rate_show.html',context)

#仓库情况
def warehouse_show(request):
    user_app.change_info(request, 'TOP_seller')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID','PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >4 and int(PRIVILEGE)!=55:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            保存参数 = request.GET.get('保存参数', '')
            if 保存参数 == '保存参数':
                当日发货数 = request.GET.get('当日发货数', '')
                date_time = request.GET.get('date_time', '')

                if 当日发货数:
                    ind = models_PruAndLog.warehouse_show_data.objects.filter(USER_ID=USER_ID).filter(date_time=date_time).values('发货数').first()
                    try:
                        if ind:
                            models_PruAndLog.warehouse_show_data.objects.filter(USER_ID=USER_ID).filter(date_time=date_time)\
                                .update(发货数=当日发货数,
                                        date_time=date_time)
                            data_msg_e = {'Detailed_orders': '0', 'msg_e': '替换成功'}
                            return HttpResponse(json.dumps(data_msg_e))
                        else:
                            models_PruAndLog.warehouse_show_data.objects.create(
                                                                          USER_ID=USER_ID,
                                                                          date_time=date_time,
                                                                          发货数=当日发货数,
                                                                          save_time=datetime.datetime.now()).save()
                            data_msg_e = {'Detailed_orders': '1', 'msg_e': '保存成功'}
                            return HttpResponse(json.dumps(data_msg_e))
                    except:
                        data_msg_e = {'Detailed_orders': '2', 'msg_e': '失败'}
                        return HttpResponse(json.dumps(data_msg_e))
                else:
                    data_msg_e = {'Detailed_orders': '2', 'msg_e': '请输入发货数量'}
                    return HttpResponse(json.dumps(data_msg_e))
            # 发货数量
            Warehouse_0 = []
            try:
                warehouses = models_PruAndLog.warehouse_show_data.objects.filter(USER_ID=USER_ID).values('发货数','date_time')
                for warehouse in warehouses:
                    warehouse['old'] = [0, 0]
                    this_date = warehouse['date_time']
                    this_date = time.mktime(this_date.timetuple())

                    warehouse['old'][0] = this_date * 1000
                    warehouse['old'][1] = round(warehouse['发货数'], 2)
                    Warehouse_0.append(warehouse['old'])

            except Exception as e:
                print(e)
            context = {
                'Warehouse_0': Warehouse_0,
            }
            return render(request, 'PruAndLog/warehouse_show.html',context)

#日期转换成JOSN的解码函数
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
# 获取API汇率数据
def get_exchange_rate():
    subm = requests.get('http://web.juhe.cn:8080/finance/exchange/rmbquot?key=7aff46ddcb609ee137e99603a3feeab3',timeout=100)
    aa = subm.text
    reponse_dicts = json.loads(aa)
    if subm.status_code == 200:
        a = reponse_dicts.get('result')[0]['data1']['fBuyPri']
        exchange = round(((float(a) / 100))*0.995-0.15, 4)
        models_PruAndLog.get_exchange_rate.objects.create(汇率名 = '美元',
                                                          exchange_rate_0=round((float(a) / 100), 4),
                                                          exchange_rate=exchange,
                                                          save_time=datetime.datetime.now()
                                                         ).save()
sched = BackgroundScheduler()
# 定时获取汇率数据
@sched.scheduled_job('cron',hour='*/3',id='my_task1')
def my_task1():
    get_exchange_rate()
sched.start()