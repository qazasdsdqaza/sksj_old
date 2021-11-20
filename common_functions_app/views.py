import json
import datetime
import time
import requests
import re
import csv
from django.shortcuts import render, redirect, reverse
from jwt import ExpiredSignatureError
from common_functions_app import models as models_common_functions
from PruAndLog import models as models_PruAndLog
from user_app import models as models_user_app
from user_app import views as user_app
from django.db.models import Sum, Count, Max, Avg, Q, F, Case, When, Value, CharField
from ast import literal_eval
import io
import json
import sys
import jwt
from django.http.response import JsonResponse, HttpResponse
from E_commerce import settings
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# 信息汇总显示
def information_aggregation(request):
    user_app.change_info(request, 'information_aggregation')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) > 5:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET":
        start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
            days=7)).date().strftime('%Y-%m-%dT%H:%M')
        end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%dT%H:%M')

        start_time_mouth = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
            days=45)).date().strftime('%Y-%m-%dT%H:%M')
        end_time_mouth = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%dT%H:%M')

        # 销售数量及均价总览
        Table_product_sum = []
        Table_bid_oders = []
        Table_buy_now_oders = []
        Table_hammer_price_local = []
        try:
            # .filter(activated_at_data__gte=start_time_mouth)
            Table_Sales_amounts = models_common_functions.Data_TopData.objects.filter(hammer_price_local__lte=300) \
                .filter(activated_at_data__lt=end_time_mouth).values('activated_at_data').annotate(
                product_sum=Sum('valid_orders'), \
                bid_oders=Sum('bid_oders'), \
                buy_now_oders=Sum('buy_now_oders'), \
                hammer_price_local=Avg('hammer_price_local'), \
                shipping_price_local=Avg('shipping_price_local'), \
                ).order_by('-activated_at_data')

            for Table_Sales_amount in Table_Sales_amounts:
                Table_Sales_amount['hammer_shipping_price'] = round(
                    float(Table_Sales_amount['hammer_price_local']) + float(Table_Sales_amount['shipping_price_local']),
                    2)
                Table_Sales_amount['Table_product_sum'] = [0, 0]
                Table_Sales_amount['Table_bid_oders'] = [0, 0]
                Table_Sales_amount['Table_buy_now_oders'] = [0, 0]
                Table_Sales_amount['Table_hammer_price_local'] = [0, 0]
                this_date = Table_Sales_amount['activated_at_data']
                this_date = time.mktime(this_date.timetuple())

                Table_Sales_amount['Table_product_sum'][0] = this_date * 1000
                Table_Sales_amount['Table_product_sum'][1] = round(Table_Sales_amount['product_sum'], 2)

                Table_product_sum.append(Table_Sales_amount['Table_product_sum'])

                Table_Sales_amount['Table_bid_oders'][0] = this_date * 1000
                Table_Sales_amount['Table_bid_oders'][1] = round(Table_Sales_amount['bid_oders'], 2)
                Table_bid_oders.append(Table_Sales_amount['Table_bid_oders'])

                Table_Sales_amount['Table_buy_now_oders'][0] = this_date * 1000
                Table_Sales_amount['Table_buy_now_oders'][1] = round(Table_Sales_amount['buy_now_oders'], 2)
                Table_buy_now_oders.append(Table_Sales_amount['Table_buy_now_oders'])

                Table_Sales_amount['Table_hammer_price_local'][0] = this_date * 1000
                Table_Sales_amount['Table_hammer_price_local'][1] = round(Table_Sales_amount['hammer_shipping_price'],
                                                                          2)
                Table_hammer_price_local.append(Table_Sales_amount['Table_hammer_price_local'])
        except Exception as e:
            print(e)

        # 卖家排行 TOP
        Table_seller = []
        Table_seller_TOP = []
        Table_seller_mouth = []
        Table_seller_TOP_mouth = []
        try:
            Table_seller_amounts = models_common_functions.Data_TopData.objects.filter(
                activated_at_data__gte=start_time).filter(
                activated_at_data__lt=end_time).values('seller_name').annotate(
                product_sum=Sum('valid_orders')).order_by('-product_sum')[0:30]
            for Table_seller_amount in Table_seller_amounts:
                Table_seller.append(Table_seller_amount['seller_name'])
                Table_seller_TOP.append(Table_seller_amount['product_sum'])
            Table_seller = re.sub("[']", "", str(Table_seller))
            Table_seller = re.sub("[[]", "", str(Table_seller))
            Table_seller = re.sub("[]]", "", str(Table_seller))

            Table_seller_mouth_amounts = models_common_functions.Data_TopData.objects.filter(
                activated_at_data__gte=start_time_mouth) \
                                             .filter(activated_at_data__lt=end_time_mouth).values(
                'seller_name').annotate(product_sum=Sum('valid_orders')).order_by('-product_sum')[0:30]
            for Table_seller_mouth_amount in Table_seller_mouth_amounts:
                Table_seller_mouth.append(Table_seller_mouth_amount['seller_name'])
                Table_seller_TOP_mouth.append(Table_seller_mouth_amount['product_sum'])
            Table_seller_mouth = re.sub("[']", "", str(Table_seller_mouth))
            Table_seller_mouth = re.sub("[[]", "", str(Table_seller_mouth))
            Table_seller_mouth = re.sub("[]]", "", str(Table_seller_mouth))
        except Exception as e:
            print(e)

        # # 标准商品排行 TOP
        # Table_product = []
        # Table_product_TOP = []
        # Table_product_mouth = []
        # Table_product_TOP_mouth = []
        # try:
        #     Table_product_amounts = models_common_functions.Data_TopData.objects.filter(activated_at_data__gte=start_time).filter(
        #         activated_at_data__lt=end_time).values('standard_product_id').annotate(
        #         product_sum=Sum('valid_orders')).order_by('-product_sum')[0:30]
        #     for Table_product_amount in Table_product_amounts:
        #         Table_product.append(Table_product_amount['standard_product_id'])
        #         Table_product_TOP.append(Table_product_amount['product_sum'])
        #
        #
        #     Table_product_mouth_amounts = models_common_functions.Data_TopData.objects.filter(activated_at_data__gte=start_time_mouth).filter(activated_at_data__lt=end_time_mouth) \
        #                                       .values('standard_product_id').annotate( product_sum=Sum('valid_orders')).order_by('-product_sum')[0:30]
        #     for Table_product_mouth_amount in Table_product_mouth_amounts:
        #         Table_product_mouth.append(Table_product_mouth_amount['standard_product_id'])
        #         Table_product_TOP_mouth.append(Table_product_mouth_amount['product_sum'])
        # except Exception as e:
        #     print(e)
        # # 品类排行 TOP
        # Table_taxonomy = []
        # Table_taxonomy_TOP = []
        # Table_taxonomy_mouth = []
        # Table_taxonomy_TOP_mouth = []
        # try:
        #     Table_taxonomy_amounts = models_common_functions.Data_TopData.objects.filter(activated_at_data__gte=start_time).filter(
        #         activated_at_data__lt=end_time) \
        #                                .values('taxonomy_values_0').annotate(product_sum=Sum('valid_orders')).order_by(
        #         '-product_sum')[0:15]
        #     for Table_taxonomy_amount in Table_taxonomy_amounts:
        #         Table_taxonomy.append(Table_taxonomy_amount['taxonomy_values_0'])
        #         Table_taxonomy_TOP.append(Table_taxonomy_amount['product_sum'])
        #     Table_taxonomy = re.sub("[']", "", str(Table_taxonomy))
        #     Table_taxonomy = re.sub("[[]", "", str(Table_taxonomy))
        #     Table_taxonomy = re.sub("[]]", "", str(Table_taxonomy))
        #
        #     Table_taxonomy_mouth_amounts = models_common_functions.Data_TopData.objects.filter(
        #         activated_at_data__gte=start_time_mouth).filter(activated_at_data__lt=end_time_mouth) \
        #                                      .values('taxonomy_values_0').annotate(
        #         product_sum=Sum('valid_orders')).order_by('-product_sum')[0:15]
        #     for Table_taxonomy_mouth_amount in Table_taxonomy_mouth_amounts:
        #         Table_taxonomy_mouth.append(Table_taxonomy_mouth_amount['taxonomy_values_0'])
        #         Table_taxonomy_TOP_mouth.append(Table_taxonomy_mouth_amount['product_sum'])
        #     Table_taxonomy_mouth = re.sub("[']", "", str(Table_taxonomy_mouth))
        #     Table_taxonomy_mouth = re.sub("[[]", "", str(Table_taxonomy_mouth))
        #     Table_taxonomy_mouth = re.sub("[]]", "", str(Table_taxonomy_mouth))
        # except Exception as e:
        #     print(e)
        context = {
            # 'user': user,
            # 日期图表
            'Table_product_sum': Table_product_sum,
            'Table_bid_oders': Table_bid_oders,
            'Table_buy_now_oders': Table_buy_now_oders,
            'Table_hammer_price_local': Table_hammer_price_local,

            # 卖家排行 TOP
            # 最近一周
            'Table_seller': Table_seller,
            'Table_seller_TOP': Table_seller_TOP,
            # 最近一月
            'Table_seller_mouth': Table_seller_mouth,
            'Table_seller_TOP_mouth': Table_seller_TOP_mouth,

            # # 标准商品排行 TOP
            # # 最近一周
            # 'Table_product': Table_product,
            # 'Table_product_TOP': Table_product_TOP,
            # # 最近一月
            # 'Table_product_mouth': Table_product_mouth,
            # 'Table_product_TOP_mouth': Table_product_TOP_mouth,

            # # 品类分布
            # # 最近一周
            # 'Table_taxonomy': Table_taxonomy,
            # 'Table_taxonomy_TOP': Table_taxonomy_TOP,
            # # 最近一月
            # 'Table_taxonomy_mouth': Table_taxonomy_mouth,
            # 'Table_taxonomy_TOP_mouth': Table_taxonomy_TOP_mouth,
        }
        return render(request, 'common_functions/information_aggregation.html', context)


def TOP_statistics(request):
    """ 以下部分为原代码 """
    # if not request.session.get('username'):
    #     return redirect(reverse('user_app:login'))
    # USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    # USER_ID = USER[0]['USER_ID']
    # PRIVILEGE = USER[0]['PRIVILEGE']
    # if int(PRIVILEGE) > 5:
    #     return render(request, '../../user_app/templates/404.html')

    """ 新增代码 """
    token = request.META.get('HTTP_X_TOKEN')
    try:
        if token:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            username = payload['data']['username']
            user_app.change_info(request, 'TOP_statistics', username)
            USER = models_user_app.User.objects.filter(username=username).values('USER_ID', 'PRIVILEGE')
            USER_ID = USER[0]['USER_ID']
            PRIVILEGE = USER[0]['PRIVILEGE']
            if int(PRIVILEGE) > 5:
                return JsonResponse({"code": 1, "message": "权限不足"})
        else:
            return JsonResponse({"code": 1, "message": "无效的token"})
    except ExpiredSignatureError:
        return JsonResponse({'code': 1, 'msg': '请重新登录'})

    if request.method == "POST":
        # 1688图片查找
        img = request.GET.get('top_img_url', '')
        if img != '':
            user_app.change_info(request, '1688图片搜索', username)
            url = img
            subm = requests.get(url, timeout=30)
            print("status code:", subm.status_code)
            open('C:\\shengkongshuju\\static\\user_files_directory\\TOP_img_to_own\\' + url[29:-13] + '.jpg',
                 'wb').write(subm.content)
            # open('F:\\shengkongshuju\\static\\user_files_directory\\TOP_img_to_own\\' + url[29:-13] + '.jpg', 'wb').write(subm.content)
            img_url = {'img_url': url[29:-13] + '.jpg'}
            return JsonResponse(img_url)
        # 卖家姓名备注
        CN_user_id = request.GET.get('CN_user_id', '')
        CN_seller_name = request.GET.get('CN_seller_name', '')
        if CN_user_id:
            user_app.change_info(request, '修改卖家备注名', username)
            index = models_common_functions.CN_seller_name.objects.filter(USER_ID=USER_ID, CN_user_id=CN_user_id)
            if index:
                models_common_functions.CN_seller_name.objects.filter(USER_ID=USER_ID,
                                                                      CN_user_id=CN_user_id).update(
                    CN_seller_name=CN_seller_name)
                data_msg_e = {'msg_e': '替换成功'}
                return JsonResponse(data_msg_e)
            else:
                models_common_functions.CN_seller_name.objects.create(
                    USER_ID=USER_ID,
                    CN_user_id=CN_user_id,
                    CN_seller_name=CN_seller_name
                )
                data_msg_e = {'msg_e': '保存成功'}
                return JsonResponse(data_msg_e)
        #
        own_all_standard_product_id = request.GET.get('own_all_standard_product_id', '')
        if own_all_standard_product_id:
            user_app.change_info(request, '编辑商品详细备注', username)
            own_all_product_price = request.GET.get('own_all_product_price', '')
            own_all_product_weight = request.GET.get('own_all_product_weight', '')
            own_all_product_name = request.GET.get('own_all_product_name', '')
            own_all_product_taxonomy = request.GET.get('own_all_product_taxonomy', '')
            own_all_product_1688addrass = request.GET.get('own_all_product_1688addrass', '')
            own_all_product_ave_sfb = request.GET.get('own_all_product_ave_sfb', '')
            own_all_product_colloct = request.GET.get('own_all_product_colloct', '')
            own_all_product_beizhu = request.GET.get('own_all_product_beizhu', '')
            index = models_common_functions.own_product_edit.objects.filter(
                USER_ID=USER_ID,
                own_all_standard_product_id=own_all_standard_product_id
            )
            if index:
                models_common_functions.own_product_edit.objects.filter(
                    USER_ID=USER_ID,
                    own_all_standard_product_id=own_all_standard_product_id
                ).update(
                    own_all_product_price=own_all_product_price,
                    own_all_product_weight=own_all_product_weight,
                    own_all_product_name=own_all_product_name,
                    own_all_product_taxonomy=own_all_product_taxonomy,
                    own_all_product_1688addrass=own_all_product_1688addrass,
                    own_all_product_ave_sfb=own_all_product_ave_sfb,
                    own_all_product_colloct=own_all_product_colloct,
                    own_all_product_beizhu=own_all_product_beizhu
                )
                data_msg_e = {'msg_e': '替换成功'}
                return JsonResponse(data_msg_e)
            else:
                models_common_functions.own_product_edit.objects.create(
                    USER_ID=USER_ID,
                    own_all_standard_product_id=own_all_standard_product_id,
                    own_all_product_price=own_all_product_price,
                    own_all_product_weight=own_all_product_weight,
                    own_all_product_name=own_all_product_name,
                    own_all_product_taxonomy=own_all_product_taxonomy,
                    own_all_product_1688addrass=own_all_product_1688addrass,
                    own_all_product_ave_sfb=own_all_product_ave_sfb,
                    own_all_product_colloct=own_all_product_colloct,
                    own_all_product_beizhu=own_all_product_beizhu
                )
                data_msg_e = {'msg_e': '保存成功'}
                return JsonResponse(data_msg_e)

        操作 = request.GET.get('操作', '')  # 操作
        if 操作 == '操作':
            导出类型 = request.GET.get('导出类型', '')  # 导出订单
            加入商品库 = request.GET.get('加入商品库', '')  # 加入商品库
            checkStatus = request.GET.get('checkStatus', '')  # 复选框选择商品的信息
            if 导出类型 == 'CSV':
                if checkStatus:
                    try:
                        products_list = literal_eval(checkStatus)
                        user_app.change_info(request, '导出详细订单-TOP_statistics')
                        with open("C:\\shengkongshuju\\static\\user_files_directory\\导出平台数据\\商品详情.csv", 'w',
                                  encoding='utf-8', newline='') as fp:
                            # with open("F:\\E_commerce\\static\\导出平台商品\\商品详情.csv", 'w', encoding='utf-8', newline='') as fp:
                            headers = ('ParentSKU(必填)', 'SKU（必填）', '产品分类', '产品标题（必填）', '产品描述（必填）',  # 5
                                       '物品状况（必填）', '产品品牌', '产品材质', '尺寸', '颜色', '库存(必填)', '零售价', '目标价(必填)',  # 13
                                       '一口价(必填)', '拍卖安排费出价', '起拍价', '来源url', '运费(必填)', '发货地(必填)', '处理时间(必填)',  # 20
                                       '运输重量', '快速运输运费（美国）', '快速运输时间', '附加项目价格', '最大日销售量', '配件价格', '配件描述',  # 27
                                       '主图（URL）地址(必填)', '附图1（URL）地址', '附图2（URL）地址', '附图3（URL）地址', '附图4（URL）地址',
                                       # 32
                                       '附图5（URL）地址', '附图6（URL）地址', '附图7（URL）地址', '成交价', '商品编号', '评分', '评论数',
                                       '收藏数')  # 35
                            writer = csv.writer(fp, dialect='excel')
                            writer.writerow(headers)  # 写入一行
                            for products_id in products_list:
                                try:
                                    objs_load_orders = models_common_functions.Data_TopData.objects.filter(
                                        lots_id=products_id).values_list(
                                        'lots_id', 'taxonomy_values_0', 'title', 'description', 'retail_price',
                                        'buy_now_price',
                                        'starting_bid_amount', 'shipping_price_local', 'image_urls_0',
                                        'image_urls_1',
                                        'image_urls_2', 'image_urls_3', 'image_urls_4', 'image_urls_5',
                                        'ratings_average', 'ratings_count', 'alerts_count')

                                    products = list(objs_load_orders[0])
                                    products_s = products

                                    load_orders_facets = models_common_functions.Data_TopData.objects.filter(
                                        lots_id=products_id).values(
                                        'facets', 'lot_upsells', 'image_urls_0', 'lots_id', 'product_parent_id',
                                        'hammer_price_local', 'shipping_price_local',
                                        'standard_product_id')  # 获取详细参数信息

                                    try:
                                        of = models_common_functions.own_product_edit.objects.filter(
                                            own_all_standard_product_id=load_orders_facets[0][
                                                'standard_product_id']).values(
                                            'own_all_product_name', 'own_all_product_taxonomy')
                                        if of:
                                            if of[0]['own_all_product_name']:
                                                products_s[0] = of[0]['own_all_product_name']
                                            if of[0]['own_all_product_taxonomy']:
                                                products_s[1] = of[0]['own_all_product_taxonomy']
                                    except Exception as e:
                                        print(e)

                                    facet_Material = ''
                                    facet_Condition = 'New'
                                    facet_Available_Sizes = ''
                                    facet_Available_Colors = ''
                                    for facet in literal_eval(load_orders_facets[0]['facets']):
                                        if facet[0] == 'Material':
                                            facet_Material = facet[1]
                                        if facet[0] == 'Condition':
                                            facet_Condition = facet[1]
                                        if facet[0] == 'Available Sizes':
                                            facet_Available_Sizes = facet[1]
                                        if facet[0] == 'Available Colors':
                                            facet_Available_Colors = facet[1]
                                    # print(facet_Material,facet_Condition,facet_Available_Sizes,facet_Available_Colors)

                                    lot_upsells_description = ''
                                    lot_upsells_amount = ''
                                    if load_orders_facets[0]['lot_upsells']:
                                        lot_upsells_0 = literal_eval(load_orders_facets[0]['lot_upsells'])
                                        try:
                                            lot_upsells_description_1 = lot_upsells_0[0]['description']
                                            lot_upsells_amount_1 = lot_upsells_0[0]['amount']
                                        except:
                                            lot_upsells_description_1 = ''
                                            lot_upsells_amount_1 = ''
                                        try:
                                            lot_upsells_description_2 = lot_upsells_0[1]['description']
                                            lot_upsells_amount_2 = lot_upsells_0[1]['amount']
                                        except:
                                            lot_upsells_description_2 = ''
                                            lot_upsells_amount_2 = ''
                                        if lot_upsells_description_2 != '':
                                            lot_upsells_description = lot_upsells_description_2
                                            lot_upsells_amount = lot_upsells_amount_2
                                        else:
                                            lot_upsells_description = lot_upsells_description_1
                                            lot_upsells_amount = lot_upsells_amount_1

                                    if load_orders_facets[0]['hammer_price_local']:
                                        hammer_price_local = float(load_orders_facets[0]['hammer_price_local'])
                                    else:
                                        hammer_price_local = 0

                                    if load_orders_facets[0]['shipping_price_local']:
                                        shipping_price_local = float(load_orders_facets[0]['shipping_price_local'])
                                    else:
                                        shipping_price_local = 0

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
                                    # products_s.insert(24, load_orders_facets[0]['image_urls_0'])  # 主图
                                    products_s.insert(30, '')  # 图6
                                    products_s.insert(31, '')  # 图7
                                    products_s.insert(32, hammer_price_local + shipping_price_local)  # 成交价+运费
                                    products_s.insert(33, load_orders_facets[0]['lots_id'])  # 商品编号

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
                                                    products_s0.insert(1, products_s[
                                                        0] + '-' + facet_Size + '-' + facet_Color)
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
                    except Exception as e:
                        print(e)
                    Detailed_orders = {'Detailed_orders': '1', 'msge': '成功'}
                    return HttpResponse(json.dumps(Detailed_orders))
                else:
                    Detailed_orders = {'Detailed_orders': '0', 'msge': '请选择商品'}
                    return HttpResponse(json.dumps(Detailed_orders))

            if 加入商品库:
                user_app.change_info(request, '加入商品库-TOP_statistics')
                if int(PRIVILEGE) > 4:
                    Detailed_orders = {'Detailed_orders': '0', 'msge': '无权限'}
                    return HttpResponse(json.dumps(Detailed_orders))
                if checkStatus != '[]' and checkStatus != '':
                    products_list = literal_eval(checkStatus)
                    for products_id in products_list:
                        # 获取自己店铺产品
                        产品材质 = ''
                        产品条件 = ''
                        产品尺寸 = ''
                        产品颜色 = ''
                        配件价格 = ''
                        配件描述 = ''
                        产品名称 = products_id
                        产品分类 = '|'
                        try:
                            Product = models_common_functions.Data_TopData.objects.filter(
                                lots_id=products_id).values_list()
                            if 加入商品库 == '评分>3.5':
                                if Product[0][28] != None and Product[0][28] > 3.5:
                                    产品ID = Product[0][2]
                                    产品标准ID = Product[0][3]
                                    产品标题 = Product[0][7]
                                    产品描述 = Product[0][13]
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

                                    一口价 = Product[0][20]
                                    if 一口价 == 'None':
                                        一口价 = '0'
                                    # 目标价 = Product[0][13]
                                    # 底价 = Product[0][17]
                                    # # 底价 = re.sub('None', '', 底价)
                                    零售价 = Product[0][21]
                                    if 零售价 == 'None':
                                        零售价 = '0'
                                    # SFB = Product[0][16]
                                    起拍价 = Product[0][22]
                                    if 起拍价 == 'None':
                                        起拍价 = '0'

                                    运输费用 = Product[0][24]
                                    if 运输费用 == 'None':
                                        运输费用 = '0'
                                    # 运输重量 = Product[0][21]
                                    # 处理时间 = Product[0][23]
                                    # 处理时间 = re.sub('None', '', str(处理时间))
                                    # 最大日销售数量 = Product[0][15]
                                    # CAMPAIGN = Product[0][34]

                                    try:
                                        详细配件 = literal_eval(Product[0][29])
                                        if 详细配件 != None:
                                            for 配件 in 详细配件:
                                                if 配件['description'] != None:
                                                    配件价格 = 配件['amount']
                                                    配件价格 = re.sub('\.0', '', 配件价格)
                                                    if 配件价格 == 'None':
                                                        配件价格 = 0
                                                    配件描述 = 配件['description']
                                    except Exception as e:
                                        print(e)

                                    产品图片1 = Product[0][14]
                                    产品图片2 = Product[0][15]
                                    产品图片3 = Product[0][16]
                                    产品图片4 = Product[0][17]
                                    产品图片5 = Product[0][18]
                                    产品图片6 = Product[0][19]
                                    try:
                                        of = models_common_functions.own_product_edit.objects.filter(
                                            USER_ID=USER_ID, own_all_standard_product_id=str(产品标准ID)) \
                                            .values('own_all_product_name', 'own_all_product_taxonomy')
                                        if of:
                                            if of[0]['own_all_product_name']:
                                                产品名称 = of[0]['own_all_product_name']
                                            if of[0]['own_all_product_taxonomy']:
                                                产品分类 = of[0]['own_all_product_taxonomy']
                                    except Exception as e:
                                        print(e)

                                    index = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID,
                                                                                             lots_id=products_id)
                                    if index:
                                        models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID,
                                                                                         lots_id=products_id) \
                                            .update(updated_at=datetime.datetime.now(), product_name=产品名称)
                                    else:
                                        twz = models_PruAndLog.Products_All_Own.objects.create(
                                            USER_ID=USER_ID,
                                            product_name=产品名称,
                                            internal_id=产品ID,
                                            standard_product_id=产品标准ID,
                                            category=产品分类,
                                            title=产品标题,
                                            description=产品描述,
                                            condition=产品条件,
                                            # brand='',
                                            material=产品材质,
                                            available_quantity='1000',
                                            color=产品颜色,
                                            size=产品尺寸,

                                            retail_price='20',
                                            cost_basis='20',
                                            minimum_bid_amount=起拍价,
                                            max_daily_schedules='1000',
                                            scheduling_fee_bid='0',
                                            reserve_price='20',
                                            shipping_price=运输费用,
                                            shipping_origin='China',
                                            # fulfillment_partner='',
                                            weight='0',
                                            days_to_deliver='5',
                                            # days_to_fulfill='',

                                            # expedited_shipping_price=expedited_shipping_price,
                                            # expedited_days_to_deliver=expedited_days_to_deliver,
                                            # buy_one_get_one_available=None,
                                            # upsells=upsells,
                                            accessory_price=配件价格,
                                            accessory_description=配件描述,

                                            primary_image=产品图片1,
                                            all_images=产品图片1 + '|' + 产品图片2 + '|' + 产品图片3 + '|' + 产品图片4 + '|' + 产品图片5 + '|' + 产品图片6,
                                            # # ratings_count='',
                                            # # ratings_average='',
                                            campaign_name='None',
                                            buy_now_price=一口价,

                                            created_at=datetime.datetime.now(),
                                            updated_at=datetime.datetime.now(),
                                            # disabled_at=disabled_at

                                            lots_id=products_id,
                                        )
                                        twz.save()
                            elif 加入商品库 == '无限制':
                                产品ID = Product[0][2]
                                产品标准ID = Product[0][3]
                                产品标题 = Product[0][7]
                                产品描述 = Product[0][13]
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

                                一口价 = Product[0][20]
                                if 一口价 == 'None':
                                    一口价 = '0'
                                # 目标价 = Product[0][13]
                                # 底价 = Product[0][17]
                                # # 底价 = re.sub('None', '', 底价)
                                零售价 = Product[0][21]
                                if 零售价 == 'None':
                                    零售价 = '0'
                                # SFB = Product[0][16]
                                起拍价 = Product[0][22]
                                if 起拍价 == 'None':
                                    起拍价 = '0'

                                运输费用 = Product[0][24]
                                if 运输费用 == 'None':
                                    运输费用 = '0'
                                # 运输重量 = Product[0][21]
                                # 处理时间 = Product[0][23]
                                # 处理时间 = re.sub('None', '', str(处理时间))
                                # 最大日销售数量 = Product[0][15]
                                # CAMPAIGN = Product[0][34]

                                try:
                                    详细配件 = literal_eval(Product[0][29])
                                    if 详细配件 != None:
                                        for 配件 in 详细配件:
                                            if 配件['description'] != None:
                                                配件价格 = 配件['amount']
                                                配件价格 = re.sub('\.0', '', 配件价格)
                                                if 配件价格 == 'None':
                                                    配件价格 = 0
                                                配件描述 = 配件['description']
                                except Exception as e:
                                    print(e)

                                产品图片1 = Product[0][14]
                                产品图片2 = Product[0][15]
                                产品图片3 = Product[0][16]
                                产品图片4 = Product[0][17]
                                产品图片5 = Product[0][18]
                                产品图片6 = Product[0][19]
                                try:
                                    of = models_common_functions.own_product_edit.objects.filter(USER_ID=USER_ID,
                                                                                                 own_all_standard_product_id=str(
                                                                                                     产品标准ID)) \
                                        .values('own_all_product_name', 'own_all_product_taxonomy')
                                    if of:
                                        if of[0]['own_all_product_name']:
                                            产品名称 = of[0]['own_all_product_name']
                                        if of[0]['own_all_product_taxonomy']:
                                            产品分类 = of[0]['own_all_product_taxonomy']
                                except Exception as e:
                                    print(e)

                                index = models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID,
                                                                                         lots_id=products_id)
                                if index:
                                    models_PruAndLog.Products_All_Own.objects.filter(USER_ID=USER_ID,
                                                                                     lots_id=products_id) \
                                        .update(updated_at=datetime.datetime.now(),
                                                product_name=产品名称)
                                else:
                                    twz = models_PruAndLog.Products_All_Own.objects.create(
                                        USER_ID=USER_ID,
                                        product_name=产品名称,
                                        internal_id=产品ID,
                                        standard_product_id=产品标准ID,
                                        category=产品分类,
                                        title=产品标题,
                                        description=产品描述,
                                        condition=产品条件,
                                        # brand='',
                                        material=产品材质,
                                        available_quantity='1000',
                                        color=产品颜色,
                                        size=产品尺寸,

                                        retail_price='20',
                                        cost_basis='20',
                                        minimum_bid_amount=起拍价,
                                        max_daily_schedules='1000',
                                        scheduling_fee_bid='0',
                                        reserve_price='20',
                                        shipping_price=运输费用,
                                        shipping_origin='China',
                                        # fulfillment_partner='',
                                        weight='0',
                                        days_to_deliver='5',
                                        # days_to_fulfill='',

                                        # expedited_shipping_price=expedited_shipping_price,
                                        # expedited_days_to_deliver=expedited_days_to_deliver,
                                        # buy_one_get_one_available=None,
                                        # upsells=upsells,
                                        accessory_price=配件价格,
                                        accessory_description=配件描述,

                                        primary_image=产品图片1,
                                        all_images=产品图片1 + '|' + 产品图片2 + '|' + 产品图片3 + '|' + 产品图片4 + '|' + 产品图片5 + '|' + 产品图片6,
                                        # # ratings_count='',
                                        # # ratings_average='',
                                        campaign_name='None',
                                        buy_now_price=一口价,

                                        created_at=datetime.datetime.now(),
                                        updated_at=datetime.datetime.now(),
                                        # disabled_at=disabled_at

                                        lots_id=products_id,
                                    )
                                    twz.save()
                        except Exception as e:
                            print(e)
                    Detailed_orders = {'Detailed_orders': '1', 'msge': '成功'}
                    return HttpResponse(json.dumps(Detailed_orders))
                else:
                    Detailed_orders = {'Detailed_orders': '0', 'msge': '请选择商品'}
                    return HttpResponse(json.dumps(Detailed_orders))

            Detailed_orders = {'Detailed_orders': '0', 'msge': '请选择下拉选项'}
            return HttpResponse(json.dumps(Detailed_orders))
        py_dict = json.loads(request.body.decode())
        start_time = py_dict.get('start_time', '')  # 开始时间
        end_time = py_dict.get('end_time', '')  # 结束时间
        Lots_id = py_dict.get('Lots_id', '')  # 商品ID  1
        standard_product_id = py_dict.get('standard_product_id', '')  # 标准商品ID  1
        seller_name = py_dict.get('seller_name', '')  # 卖家姓名  1
        product_name = py_dict.get('product_name', '')  # 商品名称  1
        price_min = py_dict.get('price_min', '')  # 最低价
        price_max = py_dict.get('price_max', '')  # 最高价
        seller_id = py_dict.get('seller_id', '')  # 卖家ID  1
        product_type = py_dict.get('product_type', '')  # 订单类型  1
        product_collection = py_dict.get('product_collection', '')  # 商品收藏  1
        limit = py_dict.get('limit', '')  # 查询的每页数量   1
        page = py_dict.get('page', '')  # 查询页
        Sort_field = py_dict.get('Sort_field', '')  # 排序字段
        Sort_order = py_dict.get('Sort_order', '')  # 排序方式

        if price_min == '':
            price_min = 0
        if price_max == '':
            price_max = 9999

        if start_time == '':
            start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                days=1)).date().strftime('%Y-%m-%d %H:%M')
        if end_time == '':
            end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d %H:%M')

        if product_type == '':
            product_type = '全部订单'

        if product_collection == '':
            product_collection = '全部商品'

        if Sort_field == '':
            Sort_field = 'valid_orders'

        if Sort_order == 'desc' or Sort_order == '':
            Sort_order = '-'
        elif Sort_order == 'asc':
            Sort_order = ''
        else:
            Sort_order = '-'
        if not limit:
            return JsonResponse({'code': 400, 'message': '缺少limit参数'})
        if not page:
            return JsonResponse({'code': 400, 'message': '缺少page参数'})
        if limit == '' and page == '':
            collect_sellers = models_common_functions.CN_seller_name.objects.filter(USER_ID=USER_ID).values()  # 已备注的卖家
            context0 = {'PRIVILEGE': PRIVILEGE,
                        'start_time': start_time,
                        'end_time': end_time,
                        'standard_product_id': standard_product_id,
                        'seller_id': seller_id,
                        'collect_sellers': [i for i in collect_sellers]
                        }
            return JsonResponse(context0)
        try:
            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            objs = models_common_functions.Data_TopData.objects.filter(activated_at_data__gte=start_time).filter(
                activated_at_data__lt=end_time)
            if standard_product_id != '':
                objs = objs.filter(standard_product_id=standard_product_id)
            if Lots_id != '':
                objs = objs.filter(lots_id=Lots_id)
            if seller_name != '':
                objs = objs.filter(seller_name=seller_name)
            if seller_id != '':
                objs = objs.filter(user_id=seller_id)
            if product_name != '':
                objs = objs.filter(title__contains=product_name)

            objs = objs.filter(hammer_price_local__gte=price_min).filter(hammer_price_local__lte=price_max)

            if product_type == '全部订单':
                count_all = objs.values('product_parent_id').annotate(lots=Count('total_orders')).count()
                objs = objs.values(
                    'product_parent_id', 'image_urls_0', 'image_urls_1', 'image_urls_2', 'image_urls_3',
                    'image_urls_4', 'image_urls_5', 'starting_bid_amount', 'standard_product_id',
                    'shipping_price_local', 'seller_name', 'user_id', 'title', 'description',
                    'taxonomy_values_0', 'taxonomy_values_1', 'bid_orders', 'buy_now_orders',
                    'taxonomy_values_2'
                ).annotate(
                    lots_id=Max('lots_id'),
                    product_sum=Sum('total_orders'),
                    valid_orders=Sum('valid_orders'),
                    buyer_id=Sum('buyer_id'),
                    # bid_hammer_price=Sum(Case(When(order_type=0, then=Value('hammer_price_local'))), output_field=CharField()),
                    hammer_price_local=Avg('hammer_price_local'),
                    ratings_average=Avg('ratings_average'),
                    ratings_count=Avg('ratings_count'),
                    alerts_count=Avg('alerts_count'),
                    lot_upsells=Max('lot_upsells'),
                    facets=Max('facets'),
                    # 新增代码
                    bid_order_count=Sum('bid_orders'),
                    buy_now_order_count=Sum('buy_now_orders'),
                ).order_by(Sort_order + Sort_field)[page_star:page_end]
            elif product_type == '一口价(拍)':
                count_all = objs.filter(~Q(bid_oders=0)).values('product_parent_id').annotate(
                    lots=Count('buy_now_orders')).count()
                objs = objs.filter(~Q(bid_orders=0)).values(
                    'product_parent_id', 'image_urls_0', 'image_urls_1',
                    'image_urls_2', 'image_urls_3', 'image_urls_4',
                    'image_urls_5', 'starting_bid_amount', 'standard_product_id',
                    'shipping_price_local', 'seller_name', 'user_id', 'title',
                    'description', 'taxonomy_values_0', 'taxonomy_values_1',
                    'taxonomy_values_2'
                ).annotate(
                    lots_id=Max('lots_id'),
                    product_sum=Sum('total_orders'),
                    valid_orders=Sum('buy_now_orders'),
                    buyer_id=Sum('buyer_id'),
                    hammer_price_local=Avg('hammer_price_local'),
                    ratings_average=Avg('ratings_average'),
                    ratings_count=Avg('ratings_count'),
                    alerts_count=Avg('alerts_count'),
                    lot_upsells=Max('lot_upsells'),
                    facets=Max('facets')
                ).order_by(
                    Sort_order + Sort_field)[page_star:page_end]
            elif product_type == '一口价(纯)':
                count_all = objs.filter(bid_orders=0).values('product_parent_id').annotate(
                    lots=Count('buy_now_orders')).count()
                objs = objs.filter(bid_orders=0).values(
                    'product_parent_id', 'image_urls_0', 'image_urls_1',
                    'image_urls_2', 'image_urls_3', 'image_urls_4',
                    'image_urls_5', 'starting_bid_amount', 'standard_product_id',
                    'shipping_price_local', 'seller_name', 'user_id', 'title',
                    'description', 'taxonomy_values_0', 'taxonomy_values_1',
                    'taxonomy_values_2'
                ).annotate(
                    lots_id=Max('lots_id'),
                    product_sum=Sum('total_orders'),
                    valid_orders=Sum('buy_now_orders'),
                    buyer_id=Sum('buyer_id'),
                    hammer_price_local=Avg('hammer_price_local'),
                    ratings_average=Avg('ratings_average'),
                    ratings_count=Avg('ratings_count'),
                    alerts_count=Avg('alerts_count'),
                    lot_upsells=Max('lot_upsells'),
                    facets=Max('facets')
                ).order_by(
                    Sort_order + Sort_field)[page_star:page_end]
            elif product_type == '一口价(全)':
                count_all = objs.values('product_parent_id').annotate(lots=Count('buy_now_orders')).count()
                objs = objs.values(
                    'product_parent_id', 'image_urls_0', 'image_urls_1', 'image_urls_2', 'image_urls_3',
                    'image_urls_4', 'image_urls_5', 'starting_bid_amount', 'standard_product_id',
                    'shipping_price_local', 'seller_name', 'user_id', 'title', 'description',
                    'taxonomy_values_0', 'taxonomy_values_1', 'taxonomy_values_2'
                ).annotate(
                    lots_id=Max('lots_id'),
                    product_sum=Sum('total_orders'),
                    valid_orders=Sum('buy_now_orders'),
                    buyer_id=Sum('buyer_id'),
                    hammer_price_local=Avg('hammer_price_local'),
                    ratings_average=Avg('ratings_average'),
                    ratings_count=Avg('ratings_count'),
                    alerts_count=Avg('alerts_count'),
                    lot_upsells=Max('lot_upsells'),
                    facets=Max('facets')
                ).order_by(
                    Sort_order + Sort_field)[page_star:page_end]
            elif product_type == '竞拍价':
                count_all = objs.values('product_parent_id').annotate(lots=Count('bid_orders')).count()
                objs = objs.values(
                    'product_parent_id', 'image_urls_0', 'image_urls_1', 'image_urls_2', 'image_urls_3',
                    'image_urls_4', 'image_urls_5', 'starting_bid_amount', 'standard_product_id',
                    'shipping_price_local', 'seller_name', 'user_id', 'title', 'description',
                    'taxonomy_values_0', 'taxonomy_values_1', 'taxonomy_values_2'
                ).annotate(
                    lots_id=Max('lots_id'),
                    product_sum=Sum('total_orders'),
                    valid_orders=Sum('bid_orders'),
                    buyer_id=Sum('buyer_id'),
                    hammer_price_local=Avg('hammer_price_local'),
                    ratings_average=Avg('ratings_average'),
                    ratings_count=Avg('ratings_count'),
                    alerts_count=Avg('alerts_count'),
                    lot_upsells=Max('lot_upsells'),
                    facets=Max('facets')
                ).order_by(
                    Sort_order + Sort_field)[page_star:page_end]

            for obj in objs:
                obj['facets_em'] = []
                obj['lots_id'] = str(obj['lots_id'])
                obj['hammer_shipping_price'] = round(
                    float(obj['hammer_price_local']) + float(obj['shipping_price_local']), 2)
                # obj['avg_hammer_price'] = round(obj['hammer_shipping_price'] / float(obj['valid_orders']), 2)
                if obj['bid_orders']:
                    obj['action_price'] = round(
                        float(obj['hammer_price_local']) + float(obj['shipping_price_local']) / float(obj['bid_orders']), 2
                    )
                else:
                    obj['action_price'] = 0
                if obj['buy_now_orders']:
                    obj['buy_now_shipping_price'] = round(
                        float(obj['hammer_price_local']) + float(obj['shipping_price_local']), 2
                    ) / float(obj['buy_now_orders'])
                else:
                    obj['buy_now_shipping_price'] = 0
                for facet in literal_eval(obj['facets']):
                    facet_em = facet[0] + '：' + facet[1]
                    obj['facets_em'].append(facet_em)
                if obj['lot_upsells']:
                    lot_upsells = literal_eval(obj['lot_upsells'])

                    try:
                        obj['lot_upsells_description_1'] = lot_upsells[0]['description']
                        obj['lot_upsells_amount_1'] = lot_upsells[0]['amount']
                        obj['lot_upsells_full_description_1'] = lot_upsells[0]['full_description']
                    except:
                        obj['lot_upsells_description_1'] = ''
                        obj['lot_upsells_amount_1'] = ''
                        obj['lot_upsells_full_description_1'] = ''

                    try:
                        obj['lot_upsells_description_2'] = lot_upsells[1]['description']
                        obj['lot_upsells_amount_2'] = lot_upsells[1]['amount']
                        obj['lot_upsells_full_description_2'] = lot_upsells[1]['full_description']
                    except:
                        obj['lot_upsells_description_2'] = ''
                        obj['lot_upsells_amount_2'] = ''
                        obj['lot_upsells_full_description_2'] = ''
                obj['image_urls'] = obj['image_urls_0'][:-12] + 'medium.jpg'
                if obj['hammer_price_local']:
                    obj['hammer_price_local'] = round(obj['hammer_price_local'], 2)
                if obj['ratings_average']:
                    obj['ratings_average'] = round(obj['ratings_average'], 2)
                if obj['ratings_count']:
                    obj['ratings_count'] = round(obj['ratings_count'])
                if obj['alerts_count']:
                    obj['alerts_count'] = round(obj['alerts_count'])

                obj['taxonomy_values'] = ''
                if obj['taxonomy_values_0']:
                    obj['taxonomy_values'] = obj['taxonomy_values_0']
                if obj['taxonomy_values_1']:
                    obj['taxonomy_values'] = obj['taxonomy_values'] + '|' + obj['taxonomy_values_1']
                if obj['taxonomy_values_2']:
                    obj['taxonomy_values'] = obj['taxonomy_values'] + '|' + obj['taxonomy_values_2']

                ob = models_common_functions.CN_seller_name.objects.filter(USER_ID=USER_ID,
                                                                           CN_user_id=obj['user_id']).values(
                    'CN_seller_name')
                if ob:
                    obj['CN_seller_name'] = ob[0]['CN_seller_name']  # 备注名

                oc = models_common_functions.own_product_edit.objects.filter(USER_ID=USER_ID,
                                                                             own_all_standard_product_id=obj[
                                                                                 'standard_product_id']).values(
                    'own_all_product_price', 'own_all_product_weight', 'own_all_product_name',
                    'own_all_product_taxonomy', 'own_all_product_1688addrass',
                    'own_all_product_ave_sfb', 'own_all_product_colloct', 'own_all_product_beizhu'
                )
                obj['own_all_product_price'] = ''
                obj['own_all_product_weight'] = ''
                obj['own_all_product_name'] = ''
                obj['own_all_product_taxonomy'] = ''
                obj['own_all_product_1688addrass'] = ''
                obj['own_all_product_ave_sfb'] = ''
                obj['own_all_product_colloct'] = ''
                obj['own_all_product_beizhu'] = ''
                if oc:
                    obj['own_all_product_price'] = oc[0]['own_all_product_price']
                    obj['own_all_product_weight'] = oc[0]['own_all_product_weight']
                    obj['own_all_product_name'] = oc[0]['own_all_product_name']
                    obj['own_all_product_taxonomy'] = oc[0]['own_all_product_taxonomy']
                    obj['own_all_product_1688addrass'] = oc[0]['own_all_product_1688addrass']
                    obj['own_all_product_ave_sfb'] = oc[0]['own_all_product_ave_sfb']
                    obj['own_all_product_colloct'] = oc[0]['own_all_product_colloct']
                    obj['own_all_product_beizhu'] = oc[0]['own_all_product_beizhu']
                if product_collection == '收藏商品':
                    if oc[0]['own_all_product_colloct'] != '收藏':
                        objs.delete()

            context = {
                'code': 20000,
                'message': '平台统计',
                'count': count_all,
                'data': list(objs),
            }
            return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'code': 500, 'message': '%s' % e})
    else:
        return JsonResponse({'code': 405, 'message': 'GET方法不允许'})


def TOP_goodslist(request):
    user_app.change_info(request, 'TOP_goodslist')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) > 5:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            start_time = request.GET.get('start_time', '')  # 开始时间
            end_time = request.GET.get('end_time', '')  # 结束时间
            standard_product_id = request.GET.get('standard_product_id', '')  # 标准商品ID
            product_name = request.GET.get('product_name', '')  # 商品名称
            limit = request.GET.get('limit', '')  # 查询的每页数量
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

        if start_time == '':
            start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                days=1)).date().strftime('%Y-%m-%d %H:%M')
        if end_time == '':
            end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d %H:%M')

        if Sort_field == '':
            Sort_field = 'valid_orders'

        if Sort_order == 'desc' or Sort_order == '':
            Sort_order = '-'
        elif Sort_order == 'asc':
            Sort_order = ''
        else:
            Sort_order = '-'

        if limit == '' and page == '':
            context0 = {'start_time': start_time,
                        'end_time': end_time,
                        'standard_product_id': standard_product_id}
            return render(request, 'common_functions/TOP_goodslist.html', context0)

        try:
            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            objs = models_common_functions.Data_TopData.objects.filter(activated_at_data__gte=start_time).filter(
                activated_at_data__lt=end_time)
            if standard_product_id != '':
                objs = objs.filter(standard_product_id=standard_product_id)
            if product_name != '':
                objs = objs.filter(title__contains=product_name)

            count_all = objs.values('standard_product_id').annotate(lots=Count('bid_oders')).count()
            objs = objs.values('standard_product_id').annotate(product_sum=Sum('total_orders'), \
                                                               valid_orders=Sum('valid_orders'), \
                                                               bid_oders=Sum('bid_oders'), \
                                                               buy_now_oders=Sum('buy_now_oders'), \
                                                               image_urls_0=Max('image_urls_0'), \
                                                               user_number=Count('user_id', distinct=True), \
                                                               product_parent_id_number=Count('product_parent_id',
                                                                                              distinct=True), \
                                                               hammer_price_local=Avg('hammer_price_local'), \
                                                               shipping_price_local=Avg('shipping_price_local'), \
                                                               ratings_average=Avg('ratings_average'), \
                                                               ratings_count=Sum('ratings_count'), \
                                                               alerts_count=Sum('alerts_count')).order_by(
                Sort_order + Sort_field)[page_star:page_end]

            for obj in objs:
                obj['image_urls'] = obj['image_urls_0'][:-12] + 'medium.jpg'
                obj['hammer_shipping_price'] = round(
                    float(obj['hammer_price_local']) + float(obj['shipping_price_local']),
                    2)

                if obj['hammer_price_local']:
                    obj['hammer_price_local'] = round(obj['hammer_price_local'], 2)
                if obj['ratings_average']:
                    obj['ratings_average'] = round(obj['ratings_average'], 2)
                if obj['ratings_count']:
                    obj['ratings_count'] = round(obj['ratings_count'])
                if obj['alerts_count']:
                    obj['alerts_count'] = round(obj['alerts_count'])

        except Exception as e:
            print(e)

        context = {
            'code': 0,
            'msg': '',
            'count': count_all,
            'data': list(objs),
        }
        if request.GET.get('page', ''):
            return HttpResponse(json.dumps(context))

        return render(request, 'common_functions/TOP_goodslist.html')


def TOP_seller(request):
    user_app.change_info(request, 'TOP_seller')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) > 5:
        return render(request, '../../user_app/templates/404.html')
    try:
        exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
    except:
        exchange_rate = 6.3000

    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            start_time = request.GET.get('start_time', '')  # 开始时间
            end_time = request.GET.get('end_time', '')  # 结束时间
            seller_name = request.GET.get('seller_name', '')  # 卖家姓名  1
            seller_id = request.GET.get('seller_id', '')  # 卖家ID  1
            特殊筛选 = request.GET.get('特殊筛选', '')  # 特殊筛选   1
            limit = request.GET.get('limit', '')  # 查询的每页数量
            page = request.GET.get('page', '')  # 查询页
            Sort_field = request.GET.get('Sort_field', '')  # 排序字段
            Sort_order = request.GET.get('Sort_order', '')  # 排序方式

        if start_time == '':
            start_time = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                days=1)).date().strftime('%Y-%m-%d %H:%M')
        if end_time == '':
            end_time = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%d %H:%M')

        if Sort_field == '':
            Sort_field = 'valid_orders'

        if Sort_order == 'desc' or Sort_order == '':
            Sort_order = '-'
        elif Sort_order == 'asc':
            Sort_order = ''
        else:
            Sort_order = '-'

        if limit == '' and page == '':
            collect_sellers = models_common_functions.CN_seller_name.objects.filter(USER_ID=USER_ID).values()  # 已备注的卖家
            context0 = {'start_time': start_time,
                        'end_time': end_time,
                        'seller_id': seller_id,
                        'collect_sellers': collect_sellers, }
            return render(request, 'common_functions/TOP_seller.html', context0)
        try:
            page_star = int(limit) * (int(page) - 1)
            page_end = page_star + int(limit)
            count_all = 0

            objs = models_common_functions.Data_TopData.objects.filter(activated_at_data__gte=start_time).filter(
                activated_at_data__lt=end_time)
            if seller_name != '':
                objs = objs.filter(seller_name=seller_name)
            if seller_id != '':
                objs = objs.filter(user_id=seller_id)
            if 特殊筛选 == '只做一口价':
                objs = objs.filter(~Q(buy_now_oders=0) & Q(bid_oders=0))

            count_all = objs.values('user_id').annotate(lots=Count('user_id')).count()
            objs = objs.values('seller_name', 'user_id').annotate(product_sum=Sum('total_orders'), \
                                                                  valid_orders=Sum('valid_orders'), \
                                                                  bid_oders=Sum('bid_oders'), \
                                                                  buyer_id=Sum('buyer_id'), \
                                                                  buy_now_oders=Sum('buy_now_oders'), \
                                                                  products=Count('product_parent_id', distinct=True), \
                                                                  hammer_price_local=Avg('hammer_price_local'), \
                                                                  shipping_price_local=Avg('shipping_price_local'), \
                                                                  ratings_average=Avg('ratings_average'), \
                                                                  ratings_count=Sum('ratings_count'), \
                                                                  alerts_count=Sum('alerts_count')).order_by(
                Sort_order + Sort_field)[page_star:page_end]

            for obj in objs:
                obj['hammer_shipping_price'] = round(
                    float(obj['hammer_price_local']) + float(obj['shipping_price_local']), 2)
                if obj['hammer_price_local']:
                    obj['hammer_price_local'] = round(obj['hammer_price_local'], 2)
                if obj['ratings_average']:
                    obj['ratings_average'] = round(obj['ratings_average'], 2)
                if obj['ratings_count']:
                    obj['ratings_count'] = round(obj['ratings_count'])
                if obj['alerts_count']:
                    obj['alerts_count'] = round(obj['alerts_count'])

                ob = models_common_functions.CN_seller_name.objects.filter(USER_ID=USER_ID,
                                                                           CN_user_id=obj['user_id']).values(
                    'CN_seller_name')
                if ob:
                    obj['CN_seller_name'] = ob[0]['CN_seller_name']  # 备注名

            collect_sellers = models_common_functions.CN_seller_name.objects.values()  # 已备注的卖家

        except Exception as e:
            print(e)

        context = {
            'code': 0,
            'msg': '',
            'count': count_all,
            'data': list(objs),
        }
        if request.GET.get('page', ''):
            return HttpResponse(json.dumps(context))
        return render(request, 'common_functions/TOP_seller.html')


# 所有展示
def TOP_show(request):
    user_app.change_info(request, 'TOP_show')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) > 5:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET":
        start_time_mouth = request.GET.get('start_time_mouth', '')  # 统计时间
        end_time_mouth = request.GET.get('end_time_mouth', '')  # 统计时间
        product_parent_id = request.GET.get('product_parent_id', '')  # 商品ID
        standard_product_id = request.GET.get('standard_product_id', '')  # 商品标准ID
        user_id = request.GET.get('user_id', '')  # 卖家ID

        if start_time_mouth == '':
            start_time_mouth = (datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                days=90)).date().strftime('%Y-%m-%dT%H:%M')
        if end_time_mouth == '':
            end_time_mouth = (datetime.datetime.now() - datetime.timedelta(hours=15)).date().strftime('%Y-%m-%dT%H:%M')

        # 销售数量及均价总览
        Table_product_sum = []
        Table_bid_oders = []
        Table_buy_now_oders = []
        Table_hammer_price_local = []
        try:
            Table_Sales_amounts = models_common_functions.Data_TopData.objects.filter(
                activated_at_data__gte=start_time_mouth).filter(
                activated_at_data__lt=end_time_mouth).filter(hammer_price_local__lte=300)

            if product_parent_id != '':
                Table_Sales_amounts = Table_Sales_amounts.filter(product_parent_id=product_parent_id)

            if standard_product_id != '':
                Table_Sales_amounts = Table_Sales_amounts.filter(standard_product_id=standard_product_id)

            if user_id != '':
                Table_Sales_amounts = Table_Sales_amounts.filter(user_id=user_id)

            Table_Sales_amounts = Table_Sales_amounts.values('activated_at_data').annotate(
                product_sum=Sum('valid_orders'), \
                bid_oders=Sum('bid_oders'), \
                buy_now_oders=Sum('buy_now_oders'), \
                hammer_price_local=Avg('hammer_price_local'), \
                shipping_price_local=Avg('shipping_price_local'), \
                ).order_by('-activated_at_data')

            for Table_Sales_amount in Table_Sales_amounts:
                Table_Sales_amount['hammer_shipping_price'] = round(
                    float(Table_Sales_amount['hammer_price_local']) + float(Table_Sales_amount['shipping_price_local']),
                    2)
                Table_Sales_amount['Table_product_sum'] = [0, 0]
                Table_Sales_amount['Table_bid_oders'] = [0, 0]
                Table_Sales_amount['Table_buy_now_oders'] = [0, 0]
                Table_Sales_amount['Table_hammer_price_local'] = [0, 0]
                this_date = Table_Sales_amount['activated_at_data']
                this_date = time.mktime(this_date.timetuple())

                Table_Sales_amount['Table_product_sum'][0] = this_date * 1000
                Table_Sales_amount['Table_product_sum'][1] = round(Table_Sales_amount['product_sum'], 2)

                Table_product_sum.append(Table_Sales_amount['Table_product_sum'])

                Table_Sales_amount['Table_bid_oders'][0] = this_date * 1000
                Table_Sales_amount['Table_bid_oders'][1] = round(Table_Sales_amount['bid_oders'], 2)
                Table_bid_oders.append(Table_Sales_amount['Table_bid_oders'])

                Table_Sales_amount['Table_buy_now_oders'][0] = this_date * 1000
                Table_Sales_amount['Table_buy_now_oders'][1] = round(Table_Sales_amount['buy_now_oders'], 2)
                Table_buy_now_oders.append(Table_Sales_amount['Table_buy_now_oders'])

                Table_Sales_amount['Table_hammer_price_local'][0] = this_date * 1000
                Table_Sales_amount['Table_hammer_price_local'][1] = round(Table_Sales_amount['hammer_shipping_price'],
                                                                          2)
                Table_hammer_price_local.append(Table_Sales_amount['Table_hammer_price_local'])
        except Exception as e:
            print(e)

        context = {
            # 'user': user,
            # 'product_parent_id': product_parent_id,
            # 'standard_product_id': standard_product_id,
            # 'user_id': user_id,
            # 'start_time_mouth': start_time_mouth,
            # 'end_time_mouth': end_time_mouth,

            # 日期图表
            'Table_product_sum': Table_product_sum,
            'Table_bid_oders': Table_bid_oders,
            'Table_buy_now_oders': Table_buy_now_oders,
            'Table_hammer_price_local': Table_hammer_price_local,

        }
        return HttpResponse(json.dumps(context))
        # return render(request, 'TOP_show.html', context)
