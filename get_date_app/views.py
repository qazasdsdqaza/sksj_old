import json
import datetime
import time
import requests
import re
import os
import django
from django.db.models import Sum, Count, Max, Min, Avg, Q, F
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler


os.environ['DJANGO_SETTINGS_MODULE'] = 'E_commerce.settings'
django.setup()

from common_functions_app import models as models_common_functions
from Tophatter_app import models as models_top_hatter
from five_miles_app import models as models_five_miles


global proxies
proxies = []


def all_ip():
    # 1 获取到数据
    global proxies
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S')
    ips = ['175.6.103.159:1081', '113.219.215.194:1081', '113.141.180.229:1081',
           '113.141.168.222:1081', '117.33.136.249:1081', '113.142.56.104:1081',
           '117.33.175.76:1081', '219.144.95.68:1081', '113.219.214.105:1081']

    # ips = ['175.6.67.90:1081', '175.6.100.91:1081',  '175.6.56.116:1081',
    #        '175.6.148.240:1081', '113.219.214.249:1081',   '106.225.198.133:1081',
    #        '182.106.188.191:1081', '106.225.197.85:1081', '175.6.80.240:1081']
    try:
        for ip in ips:
            proxies_founds = {
                'http': 'socks5://{}'.format(ip),
                'https': 'socks5://{}'.format(ip)
            }
            proxies.append(proxies_founds)
    except Exception as e:
        print(e)
        print('更新IP库失败')


# 获取全部TOP数据存到数据库
# def myfunc1(i, proxy):
def myfunc1(i):
    # # 1 获取到数据
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    # }
    # try:
    #     url = ('https://cn.tophatter.com/api/v1/lots/' + str(i) + '?source=lot-view-slot')
    #     s = requests.session()
    #     s.headers.update(headers)
    #     # s.proxies.update(proxy)
    #     subm = s.get(url, timeout=20)
    #
    #     # subm = requests.get(url, timeout=20)
    #     print("ALL status code:", subm.status_code, str(i))
    #     activated_at = None
    #     if subm.status_code == 200:
    #         aa = subm.text
    #         reponse_dict = json.loads(aa)
    #         # print(reponse_dict)
    #
    #         lots_id = reponse_dict.get('id')
    #         # 2 保存到数据库
    #         top_id = reponse_dict.get('id')
    #         product_parent_id = reponse_dict.get('product_parent_id')
    #         standard_product_id = reponse_dict.get('standard_product_id')
    #         user_id = reponse_dict.get('user_id')
    #         buyer_id = reponse_dict.get('buyer_id')
    #         default_variation_id = reponse_dict.get('default_variation_id')
    #         title = reponse_dict.get('title')
    #         taxonomy_values_0 = ''
    #         taxonomy_values_1 = ''
    #         taxonomy_values_2 = ''
    #         taxonomy_values_3 = ''
    #         try:
    #             for j in range(len(reponse_dict.get('taxonomy_values'))):
    #                 if j == 0:
    #                     taxonomy_values_0 = reponse_dict.get('taxonomy_values')[0]
    #                 if j == 1:
    #                     taxonomy_values_1 = reponse_dict.get('taxonomy_values')[1]
    #                 if j == 2:
    #                     taxonomy_values_2 = reponse_dict.get('taxonomy_values')[2]
    #                 if j == 3:
    #                     taxonomy_values_3 = reponse_dict.get('taxonomy_values')[3]
    #         except:
    #             taxonomy_values_0 = ''
    #             taxonomy_values_1 = ''
    #             taxonomy_values_2 = ''
    #             taxonomy_values_3 = ''
    #         facets = reponse_dict.get('facets')
    #         description = reponse_dict.get('description')
    #
    #         new_guarantee = reponse_dict.get('new_guarantee')
    #
    #         image_urls_0 = ''
    #         image_urls_1 = ''
    #         image_urls_2 = ''
    #         image_urls_3 = ''
    #         image_urls_4 = ''
    #         image_urls_5 = ''
    #         try:
    #             for ii in range(len(reponse_dict.get('image_urls'))):
    #                 if ii == 0:
    #                     image_urls_0 = reponse_dict.get('image_urls')[0][0:62] + 'original.jpg'
    #                 if ii == 1:
    #                     image_urls_1 = reponse_dict.get('image_urls')[1][0:62] + 'original.jpg'
    #                 if ii == 2:
    #                     image_urls_2 = reponse_dict.get('image_urls')[2][0:62] + 'original.jpg'
    #                 if ii == 3:
    #                     image_urls_3 = reponse_dict.get('image_urls')[3][0:62] + 'original.jpg'
    #                 if ii == 4:
    #                     image_urls_4 = reponse_dict.get('image_urls')[4][0:62] + 'original.jpg'
    #                 if ii == 5:
    #                     image_urls_5 = reponse_dict.get('image_urls')[5][0:62] + 'original.jpg'
    #         except:
    #             image_urls_0 = ''
    #             image_urls_1 = ''
    #             image_urls_2 = ''
    #             image_urls_3 = ''
    #             image_urls_4 = ''
    #             image_urls_5 = ''
    #
    #         main_image_width = reponse_dict.get('main_image_width')
    #         main_image_height = reponse_dict.get('main_image_height')
    #         main_image = reponse_dict.get('main_image')[0:62] + 'original.jpg'
    #         currency = reponse_dict.get('currency')
    #         buy_now_price = reponse_dict.get('buy_now_price')
    #         buy_now_price_local = reponse_dict.get('buy_now_price_local')
    #         buy_now_price_with_symbol = reponse_dict.get('buy_now_price_with_symbol')
    #         retail_price = reponse_dict.get('retail_price')
    #
    #         retail_price_local = reponse_dict.get('retail_price_local')
    #         retail_price_with_symbol = reponse_dict.get('retail_price_with_symbol')
    #         retail_price_with_partial_symbol = reponse_dict.get('retail_price_with_partial_symbol')
    #         buy_now_discount = reponse_dict.get('buy_now_discount')
    #         starting_bid_amount = reponse_dict.get('starting_bid_amount')
    #         starting_bid_amount_local = reponse_dict.get('starting_bid_amount_local')
    #         starting_bid_amount_with_symbol = reponse_dict.get('starting_bid_amount_with_symbol')
    #         hammer_price = reponse_dict.get('hammer_price')
    #         hammer_price_local = reponse_dict.get('hammer_price_local')
    #         hammer_price_with_symbol = reponse_dict.get('hammer_price_with_symbol')
    #
    #         shipping_price = reponse_dict.get('shipping_price')
    #         shipping_price_local = reponse_dict.get('shipping_price_local')
    #         shipping_price_with_symbol = reponse_dict.get('shipping_price_with_symbol')
    #         alternate_title = reponse_dict.get('alternate_title')
    #         product_brand = reponse_dict.get('product_brand')
    #         product_model = reponse_dict.get('product_model')
    #         alert = reponse_dict.get('alert')
    #         hide_reminder = reponse_dict.get('hide_reminder')
    #         alerts_count = reponse_dict.get('alerts_count')
    #         seller_name = reponse_dict.get('seller_name')
    #
    #         seller_positive_feedback_count = reponse_dict.get('seller_positive_feedback_count')
    #         seller_lots_sold = reponse_dict.get('seller_lots_sold')
    #         calculate_ratings_count = reponse_dict.get('calculate_ratings_count')
    #         ratings_count_string = reponse_dict.get('ratings_count_string')
    #         ratings_average_string = reponse_dict.get('ratings_average_string')
    #         ratings_count = reponse_dict.get('ratings_count')
    #         ratings_average = reponse_dict.get('ratings_average')
    #         sizing_ratings = reponse_dict.get('sizing_ratings')
    #         recent_ratings = reponse_dict.get('recent_ratings')
    #         view_all_ratings = reponse_dict.get('view_all_ratings')
    #
    #         ships_to_user_country = reponse_dict.get('ships_to_user_country')
    #         shipping_description_local = reponse_dict.get('shipping_description_local')
    #         variations = None  # reponse_dict.get('variations')
    #
    #         try:
    #             lot_upsells = reponse_dict.get('lot_upsells')
    #         except:
    #             lot_upsells = None
    #
    #         generic_sections = reponse_dict.get('generic_sections')
    #         analytics = reponse_dict.get('analytics')
    #         note = reponse_dict.get('note')
    #         buyer_prompt = reponse_dict.get('buyer_prompt')
    #
    #         activated_at = reponse_dict.get('activated_at')
    #         if activated_at:
    #             activated_at = reponse_dict.get('activated_at')[0:19]
    #             activated_at_data = reponse_dict.get('bidding_ended_at')[0:10]
    #         else:
    #             activated_at = None
    #             activated_at_data = None
    #
    #         bidding_started_at = reponse_dict.get('bidding_started_at')
    #         if bidding_started_at:
    #             bidding_started_at = reponse_dict.get('bidding_started_at')[0:19]
    #             bidding_started_at_data = reponse_dict.get('bidding_started_at')[0:10]
    #         else:
    #             bidding_started_at = None
    #             bidding_started_at_data = None
    #
    #         bidding_ended_at = reponse_dict.get('bidding_ended_at')
    #         if bidding_ended_at:
    #             bidding_ended_at = reponse_dict.get('bidding_ended_at')[0:19]
    #         else:
    #             bidding_ended_at = None
    #
    #         try:
    #             twz = models_common_functions.TopData.objects.create(top_id=top_id,
    #                                                                  lots_id=lots_id,
    #                                                                  product_parent_id=product_parent_id,
    #                                                                  standard_product_id=standard_product_id,
    #                                                                  user_id=user_id,
    #                                                                  buyer_id=buyer_id,
    #                                                                  default_variation_id=default_variation_id,
    #                                                                  title=title,
    #                                                                  taxonomy_values_0=taxonomy_values_0,
    #                                                                  taxonomy_values_1=taxonomy_values_1,
    #                                                                  taxonomy_values_2=taxonomy_values_2,
    #                                                                  taxonomy_values_3=taxonomy_values_3,
    #                                                                  facets=facets,
    #                                                                  description=description,
    #
    #                                                                  new_guarantee=new_guarantee,
    #                                                                  image_urls_0=image_urls_0,
    #                                                                  image_urls_1=image_urls_1,
    #                                                                  image_urls_2=image_urls_2,
    #                                                                  image_urls_3=image_urls_3,
    #                                                                  image_urls_4=image_urls_4,
    #                                                                  image_urls_5=image_urls_5,
    #                                                                  main_image_width=main_image_width,
    #                                                                  main_image_height=main_image_height,
    #                                                                  main_image=main_image,
    #                                                                  currency=currency,
    #                                                                  buy_now_price=buy_now_price,
    #                                                                  buy_now_price_local=buy_now_price_local,
    #                                                                  buy_now_price_with_symbol=buy_now_price_with_symbol,
    #                                                                  retail_price=retail_price,
    #
    #                                                                  retail_price_local=retail_price_local,
    #                                                                  retail_price_with_symbol=retail_price_with_symbol,
    #                                                                  retail_price_with_partial_symbol=retail_price_with_partial_symbol,
    #                                                                  buy_now_discount=buy_now_discount,
    #                                                                  starting_bid_amount=starting_bid_amount,
    #                                                                  starting_bid_amount_local=starting_bid_amount_local,
    #                                                                  starting_bid_amount_with_symbol=starting_bid_amount_with_symbol,
    #                                                                  hammer_price=hammer_price,
    #                                                                  hammer_price_local=hammer_price_local,
    #                                                                  hammer_price_with_symbol=hammer_price_with_symbol,
    #
    #                                                                  shipping_price=shipping_price,
    #                                                                  shipping_price_local=shipping_price_local,
    #                                                                  shipping_price_with_symbol=shipping_price_with_symbol,
    #                                                                  alternate_title=alternate_title,
    #                                                                  product_brand=product_brand,
    #                                                                  product_model=product_model,
    #                                                                  alert=alert,
    #                                                                  hide_reminder=hide_reminder,
    #                                                                  alerts_count=alerts_count,
    #                                                                  seller_name=seller_name,
    #
    #                                                                  seller_positive_feedback_count=seller_positive_feedback_count,
    #                                                                  seller_lots_sold=seller_lots_sold,
    #                                                                  calculate_ratings_count=calculate_ratings_count,
    #                                                                  ratings_count_string=ratings_count_string,
    #                                                                  ratings_average_string=ratings_average_string,
    #                                                                  ratings_count=ratings_count,
    #                                                                  ratings_average=ratings_average,
    #                                                                  sizing_ratings=sizing_ratings,
    #                                                                  recent_ratings=recent_ratings,
    #                                                                  view_all_ratings=view_all_ratings,
    #
    #                                                                  ships_to_user_country=ships_to_user_country,
    #                                                                  shipping_description_local=shipping_description_local,
    #                                                                  variations=variations,
    #                                                                  lot_upsells=lot_upsells,
    #                                                                  generic_sections=generic_sections,
    #                                                                  analytics=analytics,
    #                                                                  note=note,
    #                                                                  buyer_prompt=buyer_prompt,
    #                                                                  activated_at=activated_at,
    #                                                                  bidding_started_at=bidding_started_at,
    #                                                                  bidding_ended_at=bidding_ended_at,
    #
    #                                                                  bidding_started_at_data=bidding_started_at_data,
    #                                                                  activated_at_data=activated_at_data,
    #                                                                  )
    #             twz.save()
    #             print('所有商品保存成功')
    #         except Exception as e:
    #             print(e)
    #             print('所有商品save faile')
    #     return activated_at
    # except Exception as e:
    #     print(e)
    #     print(proxy)
    #     print('所有商品 not this id')
    #     return False
    #     # subm.status_code=1
    #     # return subm.status_code

    # 1 获取到数据
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        url = ('https://cn.tophatter.com/api/v1/lots/' + str(i) + '?source=lot-view-slot')
        s = requests.session()
        s.headers.update(headers)
        # s.proxies.update(proxy)
        subm = s.get(url, timeout=20)

        # subm = requests.get(url, timeout=20)
        print("ALL status code:", subm.status_code, str(i))
        activated_at = None
        if subm.status_code == 200:
            aa = subm.text
            reponse_dict = json.loads(aa)
            # print(reponse_dict)

            lots_id = reponse_dict.get('id')
            main_image_width = reponse_dict.get('main_image_width')
            main_image_height = reponse_dict.get('main_image_height')
            main_image = reponse_dict.get('main_image')[0:62] + 'original.jpg'
            currency = reponse_dict.get('currency')
            buy_now_price = reponse_dict.get('buy_now_price')
            buy_now_price_local = reponse_dict.get('buy_now_price_local')
            buy_now_price_with_symbol = reponse_dict.get('buy_now_price_with_symbol')
            retail_price = reponse_dict.get('retail_price')
            retail_price_local = reponse_dict.get('retail_price_local')
            retail_price_with_symbol = reponse_dict.get('retail_price_with_symbol')
            retail_price_with_partial_symbol = reponse_dict.get('retail_price_with_partial_symbol')
            buy_now_discount = reponse_dict.get('buy_now_discount')
            starting_bid_amount = reponse_dict.get('starting_bid_amount')
            starting_bid_amount_local = reponse_dict.get('starting_bid_amount_local')
            starting_bid_amount_with_symbol = reponse_dict.get('starting_bid_amount_with_symbol')
            hammer_price = reponse_dict.get('hammer_price')
            hammer_price_local = reponse_dict.get('hammer_price_local')
            hammer_price_with_symbol = reponse_dict.get('hammer_price_with_symbol')
            shipping_price = reponse_dict.get('shipping_price')
            shipping_price_local = reponse_dict.get('shipping_price_local')
            shipping_price_with_symbol = reponse_dict.get('shipping_price_with_symbol')
            alternate_title = reponse_dict.get('alternate_title')
            product_brand = reponse_dict.get('product_brand')
            product_model = reponse_dict.get('product_model')
            alert = reponse_dict.get('alert')
            hide_reminder = reponse_dict.get('hide_reminder')
            alerts_count = reponse_dict.get('alerts_count')
            seller_name = reponse_dict.get('seller_name')
            seller_positive_feedback_count = reponse_dict.get('seller_positive_feedback_count')
            seller_lots_sold = reponse_dict.get('seller_lots_sold')
            calculate_ratings_count = reponse_dict.get('calculate_ratings_count')
            ratings_count_string = reponse_dict.get('ratings_count_string')
            ratings_average_string = reponse_dict.get('ratings_average_string')
            ratings_count = reponse_dict.get('ratings_count')
            ratings_average = reponse_dict.get('ratings_average')
            sizing_ratings = reponse_dict.get('sizing_ratings')
            recent_ratings = reponse_dict.get('recent_ratings')
            view_all_ratings = reponse_dict.get('view_all_ratings')
            ships_to_user_country = reponse_dict.get('ships_to_user_country')
            shipping_description_local = reponse_dict.get('shipping_description_local')
            top_id = reponse_dict.get('id')
            product_parent_id = reponse_dict.get('product_parent_id')
            standard_product_id = reponse_dict.get('standard_product_id')
            user_id = reponse_dict.get('user_id')
            buyer_id = reponse_dict.get('buyer_id')
            default_variation_id = reponse_dict.get('default_variation_id')
            title = reponse_dict.get('title')
            facets = reponse_dict.get('facets')
            description = reponse_dict.get('description')
            new_guarantee = reponse_dict.get('new_guarantee')
            generic_sections = reponse_dict.get('generic_sections')
            analytics = reponse_dict.get('analytics')
            note = reponse_dict.get('note')
            buyer_prompt = reponse_dict.get('buyer_prompt')
            activated_at = reponse_dict.get('activated_at')

            # 2 保存到数据库
            try:
                product_video_url = reponse_dict.get('product_video_url')
            except Exception as e:
                product_video_url = ''

            try:
                name_your_price = reponse_dict.get('name_your_price')
            except KeyError:
                name_your_price = None
            taxonomy_values_0 = ''
            taxonomy_values_1 = ''
            taxonomy_values_2 = ''
            taxonomy_values_3 = ''

            try:
                for j in range(len(reponse_dict.get('taxonomy_values'))):
                    if j == 0:
                        taxonomy_values_0 = reponse_dict.get('taxonomy_values')[0]
                    if j == 1:
                        taxonomy_values_1 = reponse_dict.get('taxonomy_values')[1]
                    if j == 2:
                        taxonomy_values_2 = reponse_dict.get('taxonomy_values')[2]
                    if j == 3:
                        taxonomy_values_3 = reponse_dict.get('taxonomy_values')[3]
            except Exception as e:
                print(e)
                taxonomy_values_0 = ''
                taxonomy_values_1 = ''
                taxonomy_values_2 = ''
                taxonomy_values_3 = ''

            image_urls = []
            try:
                img_list = reponse_dict.get('image_urls')
                if img_list:
                    list1 = []
                    for img in img_list:
                        list1.append(img[:62] + 'original.jpg')
                        image_urls = list1
            except KeyError:
                image_urls = []

            try:
                main_image = reponse_dict.get('main_image')[0:62] + 'original.jpg'
            except TypeError:
                main_image = None

            image_urls_0 = ''
            image_urls_1 = ''
            image_urls_2 = ''
            image_urls_3 = ''
            image_urls_4 = ''
            image_urls_5 = ''

            try:
                for ii in range(len(reponse_dict.get('image_urls'))):
                    if ii == 0:
                        image_urls_0 = reponse_dict.get('image_urls')[0][0:62] + 'original.jpg'
                    if ii == 1:
                        image_urls_1 = reponse_dict.get('image_urls')[1][0:62] + 'original.jpg'
                    if ii == 2:
                        image_urls_2 = reponse_dict.get('image_urls')[2][0:62] + 'original.jpg'
                    if ii == 3:
                        image_urls_3 = reponse_dict.get('image_urls')[3][0:62] + 'original.jpg'
                    if ii == 4:
                        image_urls_4 = reponse_dict.get('image_urls')[4][0:62] + 'original.jpg'
                    if ii == 5:
                        image_urls_5 = reponse_dict.get('image_urls')[5][0:62] + 'original.jpg'
            except Exception as e:
                print(e)
                image_urls_0 = ''
                image_urls_1 = ''
                image_urls_2 = ''
                image_urls_3 = ''
                image_urls_4 = ''
                image_urls_5 = ''

            variations = None  # reponse_dict.get('variations')

            try:
                lot_upsells = reponse_dict.get('lot_upsells')
            except Exception as e:
                print(e)
                lot_upsells = None

            if activated_at:
                activated_at = activated_at[0:19]
                activated_at_data = reponse_dict.get('bidding_ended_at')[0:10]
            else:
                activated_at = None
                activated_at_data = None

            bidding_started_at = reponse_dict.get('bidding_started_at')
            if bidding_started_at:
                bidding_started_at = bidding_started_at[0:19]
                bidding_started_at_data = reponse_dict.get('bidding_started_at')[0:10]
            else:
                bidding_started_at = None
                bidding_started_at_data = None

            bidding_ended_at = reponse_dict.get('bidding_ended_at')
            if bidding_ended_at:
                bidding_ended_at = bidding_ended_at[0:19]
            else:
                bidding_ended_at = None

            # 拍卖单 0
            # 一口价单(纯) 1
            # 议价单 2
            # 一口价(拍) 3
            # 流拍订单 4
            # 9为初始值
            order_type = 9
            if name_your_price:  # 议价单 order_type=2
                order_type = 2
            elif bidding_started_at and bidding_ended_at:  # 拍卖单 order_type=0
                order_type = 0
            elif not bidding_started_at and bidding_ended_at:  # 一口价单 order_type=1
                order_type = 1
            elif not hammer_price:
                order_type = 4

            try:
                exist_lots_id = models_common_functions.TopData.objects.filter(lots_id=lots_id)
                if not exist_lots_id:
                    models_common_functions.TopData.objects.create(
                        top_id=top_id,
                        lots_id=lots_id,
                        product_parent_id=product_parent_id,
                        standard_product_id=standard_product_id,
                        user_id=user_id,
                        buyer_id=buyer_id,
                        default_variation_id=default_variation_id,
                        title=title,
                        product_video_url=product_video_url,
                        taxonomy_values_0=taxonomy_values_0,
                        taxonomy_values_1=taxonomy_values_1,
                        taxonomy_values_2=taxonomy_values_2,
                        taxonomy_values_3=taxonomy_values_3,
                        facets=facets,
                        description=description,
                        order_type=order_type,
                        image_urls=image_urls,
                        new_guarantee=new_guarantee,
                        image_urls_0=image_urls_0,
                        image_urls_1=image_urls_1,
                        image_urls_2=image_urls_2,
                        image_urls_3=image_urls_3,
                        image_urls_4=image_urls_4,
                        image_urls_5=image_urls_5,
                        main_image_width=main_image_width,
                        main_image_height=main_image_height,
                        main_image=main_image,
                        currency=currency,
                        buy_now_price=buy_now_price,
                        buy_now_price_local=buy_now_price_local,
                        buy_now_price_with_symbol=buy_now_price_with_symbol,
                        retail_price=retail_price,
                        retail_price_local=retail_price_local,
                        retail_price_with_symbol=retail_price_with_symbol,
                        retail_price_with_partial_symbol=retail_price_with_partial_symbol,
                        buy_now_discount=buy_now_discount,
                        starting_bid_amount=starting_bid_amount,
                        starting_bid_amount_local=starting_bid_amount_local,
                        starting_bid_amount_with_symbol=starting_bid_amount_with_symbol,
                        hammer_price=hammer_price,
                        hammer_price_local=hammer_price_local,
                        hammer_price_with_symbol=hammer_price_with_symbol,
                        shipping_price=shipping_price,
                        shipping_price_local=shipping_price_local,
                        shipping_price_with_symbol=shipping_price_with_symbol,
                        alternate_title=alternate_title,
                        product_brand=product_brand,
                        product_model=product_model,
                        alert=alert,
                        hide_reminder=hide_reminder,
                        alerts_count=alerts_count,
                        seller_name=seller_name,
                        seller_positive_feedback_count=seller_positive_feedback_count,
                        seller_lots_sold=seller_lots_sold,
                        calculate_ratings_count=calculate_ratings_count,
                        ratings_count_string=ratings_count_string,
                        ratings_average_string=ratings_average_string,
                        ratings_count=ratings_count,
                        ratings_average=ratings_average,
                        sizing_ratings=sizing_ratings,
                        recent_ratings=recent_ratings,
                        view_all_ratings=view_all_ratings,
                        ships_to_user_country=ships_to_user_country,
                        shipping_description_local=shipping_description_local,
                        variations=variations,
                        lot_upsells=lot_upsells,
                        generic_sections=generic_sections,
                        analytics=analytics,
                        note=note,
                        buyer_prompt=buyer_prompt,
                        activated_at=activated_at,
                        bidding_started_at=bidding_started_at,
                        bidding_ended_at=bidding_ended_at,
                        bidding_started_at_data=bidding_started_at_data,
                        activated_at_data=activated_at_data
                    )
                    print('所有商品保存成功')
                else:
                    print('lots_id重复,跳过本次保存')
            except Exception as e:
                print('所有商品save failed')
                raise e
        return activated_at
    except Exception as e:
        print(e)
        # print(proxy)
        print('所有商品 not this id')
        return False
        # subm.status_code=1
        # return subm.status_code


# 统计TOP数据
def myfunc_colocet():
    # 删除top获取数据大于15天的
    aaa = str(datetime.datetime.now() - datetime.timedelta(days=10))[0:13]
    time_hours_local = datetime.datetime.strptime(aaa + ':00:00', '%Y-%m-%d %H:%M:%S')
    models_common_functions.TopData.objects.filter(activated_at__lte=time_hours_local).delete()
    models_common_functions.TopData.objects.filter(save_time__lte=time_hours_local).delete()
    # 对top数据进行统计
    a = str(datetime.datetime.now() - datetime.timedelta(hours=15))[11:13]
    a = '06'
    print(a)
    # 前天
    if a == '01' or a == '22':
        bbb = str(datetime.datetime.now() - datetime.timedelta(hours=61))[0:11]
        aaa = str(datetime.datetime.now() - datetime.timedelta(hours=37))[0:11]
        start_time = datetime.datetime.strptime(bbb + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(aaa + '00:00:00', '%Y-%m-%d %H:%M:%S')
        models_common_functions.Data_TopData.objects.filter(activated_at_data=start_time).delete()
        # 获取所有成交的订单
        try:
            objs = models_common_functions.TopData.objects.filter(~Q(activated_at=None)).filter(
                activated_at__gte=start_time).filter(activated_at__lte=end_time)
            objs = objs.values(
                'product_parent_id', 'title', 'description', 'facets', 'starting_bid_amount',
                'shipping_price_local', 'seller_name', 'user_id', 'standard_product_id',
                'image_urls_0', 'image_urls_1', 'image_urls_2', 'image_urls_3', 'image_urls_4',
                'image_urls_5', 'buy_now_price', 'retail_price',
                'taxonomy_values_0', 'taxonomy_values_1', 'taxonomy_values_2'
            ).annotate(
                lots_id=Min('lots_id'),
                product_sum_total=Count('bidding_started_at'),
                ratings_average=Avg('ratings_average'),
                ratings_count=Avg('ratings_count'),
                lot_upsells=Max('lot_upsells'),
                alerts_count=Avg('alerts_count'),
                order_type=F('order_type')
            )
            for obj in objs:
                try:
                    objs_a = models_common_functions.TopData.objects.filter(~Q(activated_at=None)).filter(
                        activated_at__gte=start_time).filter(activated_at__lte=end_time)
                    objs_a = objs_a.filter(product_parent_id=obj['product_parent_id']) \
                        .filter(title=obj['title']) \
                        .filter(description=obj['description']) \
                        .filter(facets=obj['facets']) \
                        .filter(starting_bid_amount=obj['starting_bid_amount']) \
                        .filter(shipping_price_local=obj['shipping_price_local']) \
                        .filter(seller_name=obj['seller_name']) \
                        .filter(user_id=obj['user_id']) \
                        .filter(standard_product_id=obj['standard_product_id']) \
                        .filter(image_urls_0=obj['image_urls_0']) \
                        .filter(image_urls_1=obj['image_urls_1']) \
                        .filter(image_urls_2=obj['image_urls_2']) \
                        .filter(image_urls_3=obj['image_urls_3']) \
                        .filter(image_urls_4=obj['image_urls_4']) \
                        .filter(image_urls_5=obj['image_urls_5']) \
                        .filter(buy_now_price=obj['buy_now_price']) \
                        .filter(retail_price=obj['retail_price']) \
                        .filter(taxonomy_values_0=obj['taxonomy_values_0']) \
                        .filter(taxonomy_values_1=obj['taxonomy_values_1']) \
                        .filter(taxonomy_values_2=obj['taxonomy_values_2']) \
                        .filter(~Q(buyer_id=None)) \
                        .filter(order_type=obj['order_type']) \
                        .filter(~Q(hammer_price_local=0)) \
                        .values('product_parent_id').annotate(
                        product_sum_valid=Count('id'),
                        bid_orders=Count('bidding_started_at'),
                        buyer_id=Count('buyer_id', distinct=True),
                        hammer_price_local=Avg('hammer_price')
                    )
                    hammer_price_local = objs_a[0]['hammer_price_local']
                    product_sum_valid = objs_a[0]['product_sum_valid']
                    bid_orders = objs_a[0]['bid_orders']
                    buyer_id = objs_a[0]['buyer_id']
                    buy_now_orders = objs_a[0]['product_sum_valid'] - objs_a[0]['bid_orders']
                except Exception as e:
                    hammer_price_local = 0
                    product_sum_valid = 0
                    bid_orders = 0
                    buyer_id = 0
                    buy_now_orders = 0
                    print(e)

                try:
                    models_common_functions.Data_TopData.objects.create(
                        lots_id=obj['lots_id'],
                        product_parent_id=obj['product_parent_id'],
                        standard_product_id=obj['standard_product_id'],
                        user_id=obj['user_id'],
                        buyer_id=buyer_id,
                        title=obj['title'],
                        taxonomy_values_0=obj['taxonomy_values_0'],
                        taxonomy_values_1=obj['taxonomy_values_1'],
                        taxonomy_values_2=obj['taxonomy_values_2'],
                        facets=obj['facets'],
                        description=obj['description'],
                        order_type=obj['order_type'],
                        image_urls_0=obj['image_urls_0'],
                        image_urls_1=obj['image_urls_1'],
                        image_urls_2=obj['image_urls_2'],
                        image_urls_3=obj['image_urls_3'],
                        image_urls_4=obj['image_urls_4'],
                        image_urls_5=obj['image_urls_5'],

                        buy_now_price=obj['buy_now_price'],
                        retail_price=obj['retail_price'],

                        starting_bid_amount=obj['starting_bid_amount'],
                        hammer_price_local=hammer_price_local,
                        shipping_price_local=obj['shipping_price_local'],
                        alerts_count=obj['alerts_count'],
                        seller_name=obj['seller_name'],
                        ratings_count=obj['ratings_count'],
                        ratings_average=obj['ratings_average'],

                        lot_upsells=obj['lot_upsells'],
                        activated_at_data=start_time,
                        total_orders=obj['product_sum_total'],
                        valid_orders=product_sum_valid,
                        bid_orders=bid_orders,
                        buy_now_oders=buy_now_orders,
                    )
                    print('所有订单成功')
                except Exception as e:
                    print(e)
                    print('所有订单失败1')
        except Exception as e:
            print(e)
            print('所有订单失败2')
        # 获取表格统计数据
    # 昨天
    if a == '01' or a == '06' or a == '09' or a == '14' or a == '18' or a == '22' or a == '23' or a == '24':
        bbb = str(datetime.datetime.now() - datetime.timedelta(hours=39))[0:11]
        aaa = str(datetime.datetime.now() - datetime.timedelta(hours=15))[0:11]
        start_time = datetime.datetime.strptime(bbb + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(aaa + '00:00:00', '%Y-%m-%d %H:%M:%S')
        models_common_functions.Data_TopData.objects.filter(activated_at_data=start_time).delete()
        # 获取所有成交的订单
        # start_time = '2020-05-23 00:00:00'
        # end_time = '2020-05-24 00:00:00'
        # 获取所有成交的订单
        try:
            objs = models_common_functions.TopData.objects.filter(~Q(activated_at=None)).filter(
                activated_at__gte=start_time).filter(activated_at__lte=end_time)
            objs = objs.values(
                'product_parent_id', 'title', 'description', 'facets', 'starting_bid_amount',
                'shipping_price_local', 'seller_name', 'user_id', 'standard_product_id',
                'image_urls_0', 'image_urls_1', 'image_urls_2', 'image_urls_3', 'image_urls_4',
                'image_urls_5', 'buy_now_price', 'retail_price',
                'taxonomy_values_0', 'taxonomy_values_1', 'taxonomy_values_2'
            ).annotate(
                lots_id=Min('lots_id'),
                product_sum_total=Count('bidding_started_at'),
                ratings_average=Avg('ratings_average'),
                ratings_count=Avg('ratings_count'),
                lot_upsells=Max('lot_upsells'),
                alerts_count=Avg('alerts_count'),
                order_type=F('order_type')
            )
            for obj in objs:
                try:
                    objs_a = models_common_functions.TopData.objects.filter(~Q(activated_at=None)).filter(
                        activated_at__gte=start_time).filter(activated_at__lte=end_time)
                    objs_a = objs_a.filter(product_parent_id=obj['product_parent_id']) \
                        .filter(title=obj['title']) \
                        .filter(description=obj['description']) \
                        .filter(facets=obj['facets']) \
                        .filter(starting_bid_amount=obj['starting_bid_amount']) \
                        .filter(shipping_price_local=obj['shipping_price_local']) \
                        .filter(seller_name=obj['seller_name']) \
                        .filter(user_id=obj['user_id']) \
                        .filter(standard_product_id=obj['standard_product_id']) \
                        .filter(image_urls_0=obj['image_urls_0']) \
                        .filter(image_urls_1=obj['image_urls_1']) \
                        .filter(image_urls_2=obj['image_urls_2']) \
                        .filter(image_urls_3=obj['image_urls_3']) \
                        .filter(image_urls_4=obj['image_urls_4']) \
                        .filter(image_urls_5=obj['image_urls_5']) \
                        .filter(buy_now_price=obj['buy_now_price']) \
                        .filter(retail_price=obj['retail_price']) \
                        .filter(taxonomy_values_0=obj['taxonomy_values_0']) \
                        .filter(taxonomy_values_1=obj['taxonomy_values_1']) \
                        .filter(taxonomy_values_2=obj['taxonomy_values_2']) \
                        .filter(~Q(buyer_id=None)) \
                        .filter(order_type=obj['order_type']) \
                        .filter(~Q(hammer_price_local=0)) \
                        .values('product_parent_id').annotate(
                        product_sum_valid=Count('id'),
                        bid_orders=Count('bidding_started_at'),
                        buyer_id=Count('buyer_id', distinct=True),
                        hammer_price_local=Avg('hammer_price')
                    )
                    hammer_price_local = objs_a[0]['hammer_price_local']
                    product_sum_valid = objs_a[0]['product_sum_valid']
                    bid_orders = objs_a[0]['bid_orders']
                    buyer_id = objs_a[0]['buyer_id']
                    buy_now_orders = objs_a[0]['product_sum_valid'] - objs_a[0]['bid_orders']
                except Exception as e:
                    hammer_price_local = 0
                    product_sum_valid = 0
                    bid_orders = 0
                    buyer_id = 0
                    buy_now_orders = 0
                    print('昨天: %s' % e)

                try:
                    models_common_functions.Data_TopData.objects.create(
                        lots_id=obj['lots_id'],
                        product_parent_id=obj['product_parent_id'],
                        standard_product_id=obj['standard_product_id'],
                        user_id=obj['user_id'],
                        buyer_id=buyer_id,
                        title=obj['title'],
                        taxonomy_values_0=obj['taxonomy_values_0'],
                        taxonomy_values_1=obj['taxonomy_values_1'],
                        taxonomy_values_2=obj['taxonomy_values_2'],
                        facets=obj['facets'],
                        description=obj['description'],
                        order_type=obj['order_type'],
                        image_urls_0=obj['image_urls_0'],
                        image_urls_1=obj['image_urls_1'],
                        image_urls_2=obj['image_urls_2'],
                        image_urls_3=obj['image_urls_3'],
                        image_urls_4=obj['image_urls_4'],
                        image_urls_5=obj['image_urls_5'],

                        buy_now_price=obj['buy_now_price'],
                        retail_price=obj['retail_price'],

                        starting_bid_amount=obj['starting_bid_amount'],
                        hammer_price_local=hammer_price_local,
                        shipping_price_local=obj['shipping_price_local'],
                        alerts_count=obj['alerts_count'],
                        seller_name=obj['seller_name'],
                        ratings_count=obj['ratings_count'],
                        ratings_average=obj['ratings_average'],

                        lot_upsells=obj['lot_upsells'],

                        activated_at_data=start_time,
                        total_orders=obj['product_sum_total'],
                        valid_orders=product_sum_valid,
                        bid_orders=bid_orders,
                        buy_now_orders=buy_now_orders,
                    )
                    print('所有订单成功')
                except Exception as e:
                    print(e)
                    print('所有订单失败1')
        except Exception as e:
            print(e)
            print('所有订单失败2')
    # 今天
    if a == '01' or a == '06' or a == '09' or a == '14' or a == '18' or a == '22' or a == '23':
        bbb = str(datetime.datetime.now() - datetime.timedelta(hours=16))[0:11]
        aaa = str(datetime.datetime.now() + datetime.timedelta(hours=11))[0:11]
        start_time = datetime.datetime.strptime(bbb + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(aaa + '00:00:00', '%Y-%m-%d %H:%M:%S')
        models_common_functions.Data_TopData.objects.filter(activated_at_data=start_time).delete()
        # 获取所有成交的订单
        # start_time = '2020-05-23 00:00:00'
        # end_time = '2020-05-24 00:00:00'
        # 获取所有成交的订单
        try:
            objs = models_common_functions.TopData.objects.filter(~Q(activated_at=None)).filter(
                activated_at__gte=start_time).filter(activated_at__lte=end_time)
            objs = objs.values(
                'product_parent_id', 'title', 'description', 'facets', 'starting_bid_amount',
                'shipping_price_local', 'seller_name', 'user_id', 'standard_product_id',
                'image_urls_0', 'image_urls_1', 'image_urls_2', 'image_urls_3', 'image_urls_4',
                'image_urls_5', 'buy_now_price', 'retail_price',
                'taxonomy_values_0', 'taxonomy_values_1', 'taxonomy_values_2'
            ).annotate(
                lots_id=Min('lots_id'),
                product_sum_total=Count('bidding_started_at'),
                ratings_average=Avg('ratings_average'),
                ratings_count=Avg('ratings_count'),
                lot_upsells=Max('lot_upsells'),
                alerts_count=Avg('alerts_count'),
                order_type=F('order_type')
            )
            for obj in objs:
                try:
                    objs_a = models_common_functions.TopData.objects.filter(~Q(activated_at=None)).filter(
                        activated_at__gte=start_time).filter(activated_at__lte=end_time)
                    objs_a = objs_a.filter(product_parent_id=obj['product_parent_id']) \
                        .filter(title=obj['title']) \
                        .filter(description=obj['description']) \
                        .filter(facets=obj['facets']) \
                        .filter(starting_bid_amount=obj['starting_bid_amount']) \
                        .filter(shipping_price_local=obj['shipping_price_local']) \
                        .filter(seller_name=obj['seller_name']) \
                        .filter(user_id=obj['user_id']) \
                        .filter(standard_product_id=obj['standard_product_id']) \
                        .filter(image_urls_0=obj['image_urls_0']) \
                        .filter(image_urls_1=obj['image_urls_1']) \
                        .filter(image_urls_2=obj['image_urls_2']) \
                        .filter(image_urls_3=obj['image_urls_3']) \
                        .filter(image_urls_4=obj['image_urls_4']) \
                        .filter(image_urls_5=obj['image_urls_5']) \
                        .filter(buy_now_price=obj['buy_now_price']) \
                        .filter(retail_price=obj['retail_price']) \
                        .filter(taxonomy_values_0=obj['taxonomy_values_0']) \
                        .filter(taxonomy_values_1=obj['taxonomy_values_1']) \
                        .filter(taxonomy_values_2=obj['taxonomy_values_2']) \
                        .filter(~Q(buyer_id=None)) \
                        .filter(order_type=obj['order_type']) \
                        .filter(~Q(hammer_price_local=0)) \
                        .values('product_parent_id').annotate(
                        product_sum_valid=Count('id'),
                        bid_orders=Count('bidding_started_at'),
                        buyer_id=Count('buyer_id', distinct=True),
                        hammer_price_local=Avg('hammer_price')
                    )
                    hammer_price_local = objs_a[0]['hammer_price_local']
                    product_sum_valid = objs_a[0]['product_sum_valid']
                    bid_orders = objs_a[0]['bid_orders']
                    buyer_id = objs_a[0]['buyer_id']
                    buy_now_orders = objs_a[0]['product_sum_valid'] - objs_a[0]['bid_orders']
                except Exception as e:
                    hammer_price_local = 0
                    product_sum_valid = 0
                    bid_orders = 0
                    buyer_id = 0
                    buy_now_orders = 0
                    print(e)

                try:
                    models_common_functions.Data_TopData.objects.create(
                        lots_id=obj['lots_id'],
                        product_parent_id=obj['product_parent_id'],
                        standard_product_id=obj['standard_product_id'],
                        user_id=obj['user_id'],
                        buyer_id=buyer_id,
                        title=obj['title'],
                        taxonomy_values_0=obj['taxonomy_values_0'],
                        taxonomy_values_1=obj['taxonomy_values_1'],
                        taxonomy_values_2=obj['taxonomy_values_2'],
                        facets=obj['facets'],
                        description=obj['description'],
                        image_urls_0=obj['image_urls_0'],
                        image_urls_1=obj['image_urls_1'],
                        image_urls_2=obj['image_urls_2'],
                        image_urls_3=obj['image_urls_3'],
                        image_urls_4=obj['image_urls_4'],
                        image_urls_5=obj['image_urls_5'],
                        order_type=obj['order_type'],
                        buy_now_price=obj['buy_now_price'],
                        retail_price=obj['retail_price'],

                        starting_bid_amount=obj['starting_bid_amount'],
                        hammer_price_local=hammer_price_local,
                        shipping_price_local=obj['shipping_price_local'],
                        alerts_count=obj['alerts_count'],
                        seller_name=obj['seller_name'],
                        ratings_count=obj['ratings_count'],
                        ratings_average=obj['ratings_average'],

                        lot_upsells=obj['lot_upsells'],

                        activated_at_data=start_time,
                        total_orders=obj['product_sum_total'],
                        valid_orders=product_sum_valid,
                        bid_orders=bid_orders,
                        buy_now_orders=buy_now_orders,
                    )
                    print('所有订单成功')
                except Exception as e:
                    print(e)
                    print('所有订单失败1')
        except Exception as e:
            print(e)
            print('所有订单失败2')


# 统计TOP数据:销售数量及均价总览
def get_sales_amounts():
    # a = str(datetime.datetime.now() - datetime.timedelta(hours=15))[11:13]
    # if a=='02'or a=='06'or a=='10'or a=='14'or a=='18'or a=='23':
    # models.Table_Sales_amounts.objects.all().delete()
    # 获取所有成交的订单
    try:
        objs = models_common_functions.Data_TopData.objects.values('activated_at_data').annotate(
            product_sum=Sum('valid_orders'),
            bid_orders=Sum('bid_orders'),
            buy_now_orders=Sum('buy_now_orders'),
            hammer_price_local=Avg('hammer_price_local')
        ).order_by('-activated_at_data')

        for obj in objs:
            try:
                models_common_functions.Table_Sales_amounts.objects.create(
                    STAR_DATE=obj['activated_at_data'].date(),
                    product_sum=obj['product_sum'],
                    bid_orders=obj['bid_orders'],
                    buy_now_orders=obj['buy_now_orders'],
                    avg_amount=obj['hammer_price_local']
                )
                # twz.save()
                print('所有订单成功')
            except Exception as e:
                print(e)
                print('所有订单失败1')
    except Exception as e:
        print(e)
        print('所有订单失败2')


# 获取peformence_每3小时的销售数据
def get_performance_data_hours_time():
    try:
        models_top_hatter.Performance_hours_time.objects.filter(~Q(TIME_SELECT=None)).delete()
        TIMES = ["today", "yesterday", "last_week", "last_30_days"]
        for TIME in TIMES:
            for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
                try:
                    store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][0]
                    store_APIToken = \
                        models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_APIToken')[0][0]
                    USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]

                    subm = requests.get(
                        'https://tophatter.com/merchant_api/v1/performance/auctions.json?access_token=' + store_APIToken + '&duration=' + TIME,
                        timeout=100)
                    print("实时——status code:", subm.status_code, store_name, TIME)
                    aa = subm.text
                    reponse_dicts = json.loads(aa)
                    # 2 保存到数据库
                    if subm.status_code == 200:
                        for reponse_dict in reponse_dicts:
                            store_name = store_name
                            identifier = reponse_dict['table']['identifier']
                            cost_basis = reponse_dict['table']['cost_basis']
                            schedules = reponse_dict['table']['schedules']
                            orders = reponse_dict['table']['orders']
                            revenue = reponse_dict['table']['revenue']
                            fees = reponse_dict['table']['fees']
                            scheduling_fees = reponse_dict['table']['scheduling_fees']

                            try:
                                twz = models_top_hatter.Performance_hours_time.objects.create(
                                    USER_ID=USER_ID,
                                    store_name=store_name,
                                    identifier=identifier,
                                    cost_basis=cost_basis,
                                    schedules=schedules,
                                    orders=orders,
                                    revenue=revenue,
                                    fees=fees,
                                    scheduling_fees=scheduling_fees,
                                    time_local=(datetime.datetime.now() - datetime.timedelta(hours=15)).date(),
                                    TIME_SELECT=TIME,
                                )
                                twz.save()
                                # print(store_name+' today_success')
                            except Exception as e:
                                print(e)
                                print('PerformanceData today save faile')
                except Exception as e:
                    print(e)
        # 按照特定时间点保存数据 3小时
        a = str(datetime.datetime.now() - datetime.timedelta(hours=15))[11:13]
        b = max(models_top_hatter.Performance_hours_time.objects.filter(~Q(time_hours_local=None)).values_list(
            'time_hours_local'))[0]
        c = datetime.datetime.strptime((str(datetime.datetime.now() - datetime.timedelta(hours=15))[0:13]) + ':00:00',
                                       '%Y-%m-%d %H:%M:%S')
        if b != c:
            if a == '03' or a == '06' or a == '09' or a == '12' or a == '15' or a == '18' or a == '21' or a == '23':
                for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
                    try:
                        store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][
                            0]
                        store_APIToken = \
                            models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_APIToken')[0][0]
                        USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]
                        subm = requests.get(
                            'https://tophatter.com/merchant_api/v1/performance/auctions.json?access_token=' + store_APIToken + '&duration=today',
                            timeout=100)
                        print("3小时——status code:", subm.status_code)
                        aa = subm.text
                        reponse_dicts = json.loads(aa)
                        # 2 保存到数据库
                        if subm.status_code == 200:
                            for reponse_dict in reponse_dicts:
                                store_name = store_name
                                identifier = reponse_dict['table']['identifier']
                                cost_basis = reponse_dict['table']['cost_basis']
                                schedules = reponse_dict['table']['schedules']
                                orders = reponse_dict['table']['orders']
                                revenue = reponse_dict['table']['revenue']
                                fees = reponse_dict['table']['fees']
                                scheduling_fees = reponse_dict['table']['scheduling_fees']

                                aaa = str(datetime.datetime.now() - datetime.timedelta(hours=15))[0:13]
                                time_hours_local = datetime.datetime.strptime(aaa + ':00:00', '%Y-%m-%d %H:%M:%S')

                                try:
                                    twz = models_top_hatter.Performance_hours_time.objects.create(
                                        USER_ID=USER_ID,
                                        store_name=store_name,
                                        identifier=identifier,
                                        cost_basis=cost_basis,
                                        schedules=schedules,
                                        orders=orders,
                                        revenue=revenue,
                                        fees=fees,
                                        scheduling_fees=scheduling_fees,
                                        time_local=(datetime.datetime.now() - datetime.timedelta(hours=15)).date(),
                                        time_hours_local=time_hours_local,
                                        time_hours_local_symbol=a
                                    )
                                    twz.save()
                                    print(store_name + ' 3小时_success')
                                except Exception as e:
                                    print(e)
                                    print('PerformanceData_yesterday save faile')
                    except Exception as e:
                        print(e)
        # 获取peformence_yesterday销售数据
        a = (datetime.datetime.now() - datetime.timedelta(hours=16) - datetime.timedelta(days=1)).date()
        b = max(models_top_hatter.Performance_hours_time.objects.filter(TIME_SELECT=None).filter(
            time_hours_local_symbol='yestoday').values_list('time_local'))[0]
        # print(a,b)
        if a != b:
            for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
                try:
                    store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][0]
                    store_APIToken = \
                        models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_APIToken')[0][0]
                    USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]
                    subm = requests.get(
                        'https://tophatter.com/merchant_api/v1/performance/auctions.json?access_token=' + store_APIToken + '&duration=yesterday',
                        timeout=100)
                    print("peformence_yesterday ——status code:", subm.status_code)
                    aa = subm.text
                    reponse_dicts = json.loads(aa)
                    # 2 保存到数据库
                    if subm.status_code == 200:
                        for reponse_dict in reponse_dicts:
                            store_name = store_name
                            identifier = reponse_dict['table']['identifier']
                            cost_basis = reponse_dict['table']['cost_basis']
                            schedules = reponse_dict['table']['schedules']
                            orders = reponse_dict['table']['orders']
                            revenue = reponse_dict['table']['revenue']
                            fees = reponse_dict['table']['fees']
                            scheduling_fees = reponse_dict['table']['scheduling_fees']

                            try:
                                twz = models_top_hatter.Performance_hours_time.objects.create(
                                    USER_ID=USER_ID,
                                    store_name=store_name,
                                    identifier=identifier,
                                    cost_basis=cost_basis,
                                    schedules=schedules,
                                    orders=orders,
                                    revenue=revenue,
                                    fees=fees,
                                    scheduling_fees=scheduling_fees,
                                    time_hours_local_symbol='yestoday',
                                    time_local=(datetime.datetime.now() - datetime.timedelta(
                                        hours=16) - datetime.timedelta(days=1)).date()
                                )
                                twz.save()
                                print(store_name + ' yestoday_success')
                            except Exception as e:
                                print(e)
                                print('PerformanceData_yesterday save faile')
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


# # 获取后台API销售数据存到数据库(订单数据30分钟一次)
def get_store_data_1():
    # 1 删除2019年数据

    # 2 获取到数据
    for PAGE in range(1, 3):
        models_top_hatter.StoreSellData.objects.filter(paid_at__lte='2021-01-01 00:00:00').delete()

        PAGE = str(PAGE)
        print('storedata1--' + PAGE)
        i = 0
        for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
            try:
                store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][0]
                store_APIToken = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_APIToken')[0][
                    0]
                USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]

                data = {
                    'access_token': store_APIToken,
                    'page': PAGE,
                    'per_page': '200'
                }
                # print(PAGE)
                # print(store_APIToken)
                subm = requests.get('https://tophatter.com/merchant_api/v1/orders.json', data=data, timeout=100)

                # subm = requests.get(url)
                print("status code:", subm.status_code)
                aa = subm.text
                reponse_dicts = json.loads(aa)

                # 2 保存到数据库
                # print(len(reponse_dicts))
                for reponse_dict in reponse_dicts:
                    order_id = reponse_dict.get('order_id')
                    status = reponse_dict.get('status')

                    if status == 'paid':
                        status_paid = status + str(order_id)
                        status_shipped = None
                        status_refunded = None
                    elif status == 'shipped':
                        status_paid = None
                        status_shipped = status + str(order_id)
                        status_refunded = None
                    elif status == 'refunded':
                        status_paid = None
                        status_shipped = None
                        status_refunded = status + str(order_id)

                    carrier = reponse_dict.get('carrier')
                    tracking_number = reponse_dict.get('tracking_number')
                    fulfillment_partner = reponse_dict.get('fulfillment_partner')
                    product_name = reponse_dict.get('product_name')
                    product_identifier = reponse_dict.get('product_identifier')
                    product_internal_id = reponse_dict.get('product_internal_id')
                    variation_identifier = reponse_dict.get('variation_identifier')
                    variation_internal_id = reponse_dict.get('variation_internal_id')
                    customer_id = reponse_dict.get('customer_id')
                    customer_name = reponse_dict.get('customer_name')
                    address1 = reponse_dict.get('address1')
                    address2 = reponse_dict.get('address2')
                    city = reponse_dict.get('city')
                    state = reponse_dict.get('state')
                    postal_code = reponse_dict.get('postal_code')
                    country = reponse_dict.get('country')
                    related_order_ids = reponse_dict.get('related_order_ids')
                    service_type = reponse_dict.get('service_type')

                    # available_refunds_buyer_fee = reponse_dict.get('available_refunds').get('buyer_fee')

                    refund_amount = reponse_dict.get('refund_amount')
                    disbursement_amount = reponse_dict.get('disbursement_amount')
                    seller_fees_amount = reponse_dict.get('seller_fees_amount')

                    seller_fees_type_sfb = None
                    seller_fees_amount_sfb = None
                    seller_fees_type_com = None
                    seller_fees_amount_com = None
                    seller_fees_type_pro = None
                    seller_fees_amount_pro = None
                    ab = reponse_dict.get('seller_fees')
                    # print(ab)
                    if ab:
                        for j in range(len(reponse_dict.get('seller_fees'))):
                            if j == 0:
                                type = reponse_dict.get('seller_fees')[0]['type']
                                amount = reponse_dict.get('seller_fees')[0]['amount']
                                if type == 'scheduling_fee':
                                    seller_fees_type_sfb = type + str(order_id)
                                    seller_fees_amount_sfb = amount
                                elif type == 'commission_fee':
                                    seller_fees_type_com = type + str(order_id)
                                    seller_fees_amount_com = amount
                                elif type == 'processing_fee':
                                    seller_fees_type_pro = type + str(order_id)
                                    seller_fees_amount_pro = amount

                            if j == 1:
                                type1 = reponse_dict.get('seller_fees')[1]['type']
                                amount1 = reponse_dict.get('seller_fees')[1]['amount']
                                if type1 == 'scheduling_fee':
                                    seller_fees_type_sfb = type1 + str(order_id)
                                    seller_fees_amount_sfb = amount1
                                elif type1 == 'commission_fee':
                                    seller_fees_type_com = type1 + str(order_id)
                                    seller_fees_amount_com = amount1
                                elif type1 == 'processing_fee':
                                    seller_fees_type_pro = type1 + str(order_id)
                                    seller_fees_amount_pro = amount1

                            if j == 2:
                                type2 = reponse_dict.get('seller_fees')[2]['type']
                                amount2 = reponse_dict.get('seller_fees')[2]['amount']
                                if type2 == 'scheduling_fee':
                                    seller_fees_type_sfb = type2 + str(order_id)
                                    seller_fees_amount_sfb = amount2
                                elif type2 == 'commission_fee':
                                    seller_fees_type_com = type2 + str(order_id)
                                    seller_fees_amount_com = amount2
                                elif type2 == 'processing_fee':
                                    seller_fees_type_pro = type2 + str(order_id)
                                    seller_fees_amount_pro = amount2

                    if seller_fees_type_sfb == None:
                        seller_fees_type_buy_nows = 'buy_nows' + str(order_id)
                        seller_fees_type_buy_nows_price = disbursement_amount
                    else:
                        seller_fees_type_buy_nows = None
                        seller_fees_type_buy_nows_price = None

                    upsells_type_description1 = None
                    upsells_amount1 = None
                    upsells_description1 = None
                    upsells_type_description2 = None
                    upsells_amount2 = None
                    upsells_description2 = None

                    a = reponse_dict.get('upsells')
                    if a:
                        for j in range(len(reponse_dict.get('upsells'))):
                            if j == 0:
                                type = reponse_dict.get('upsells')[0]['type_description']
                                amount = reponse_dict.get('upsells')[0]['amount']
                                description = reponse_dict.get('upsells')[0]['description']
                                if type == 'buy_one_get_one':
                                    upsells_type_description1 = type + str(order_id)
                                    upsells_amount1 = amount
                                    upsells_description1 = description
                                elif type == 'accessory':
                                    upsells_type_description2 = type + str(order_id)
                                    upsells_amount2 = amount
                                    upsells_description2 = description
                            if j == 1:
                                type2 = reponse_dict.get('upsells')[1]['type_description']
                                amount2 = reponse_dict.get('upsells')[1]['amount']
                                description2 = reponse_dict.get('upsells')[1]['description']
                                if type2 == 'buy_one_get_one':
                                    upsells_type_description1 = type2 + str(order_id)
                                    upsells_amount1 = amount2
                                    upsells_description1 = description2
                                elif type2 == 'accessory':
                                    upsells_type_description2 = type2 + str(order_id)
                                    upsells_amount2 = amount2
                                    upsells_description2 = description2

                    created_at = reponse_dict.get('created_at')
                    if created_at:
                        created_at = reponse_dict.get('created_at')[0:18]
                        data_time_created_at = created_at[0:10]
                        hours_time_created_at = created_at[11:13]
                    else:
                        created_at = None
                        data_time_created_at = None
                        hours_time_created_at = None

                    paid_at = reponse_dict.get('paid_at')
                    if paid_at:
                        paid_at = reponse_dict.get('paid_at')[0:18]
                        data_time_paid_at = paid_at[0:10]
                    else:
                        paid_at = None
                        data_time_paid_at = None

                    refunded_at = reponse_dict.get('refunded_at')
                    if refunded_at:
                        refunded_at = reponse_dict.get('refunded_at')[0:18]
                        refunded_AT = datetime.datetime.strptime(refunded_at, "%Y-%m-%dT%H:%M:%S")
                        created_AT = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
                        aa = (refunded_AT - created_AT).days
                        # print(aa)
                        if tracking_number:
                            # print(refunded_AT - created_AT)
                            refunded_at_own = None
                            refunded_at_buyer = refunded_at
                            refund_amount_own = None
                            refund_amount_buyer = disbursement_amount
                        else:
                            refunded_at_own = refunded_at
                            refunded_at_buyer = None
                            refund_amount_own = disbursement_amount
                            refund_amount_buyer = None
                    else:
                        refunded_at_own = None
                        refunded_at_buyer = None
                        refund_amount_own = None
                        refund_amount_buyer = None

                    updated_at = reponse_dict.get('updated_at')
                    if updated_at:
                        updated_at = reponse_dict.get('updated_at')[0:18]
                    else:
                        updated_at = None

                    canceled_at = reponse_dict.get('canceled_at')
                    if canceled_at:
                        canceled_at = reponse_dict.get('canceled_at')[0:18]
                        canceled_refund_amount = refund_amount
                        canceled_disbursement_amount = disbursement_amount
                        canceled_seller_fees_amount = seller_fees_amount
                    else:
                        canceled_at = None
                        canceled_refund_amount = None
                        canceled_disbursement_amount = None
                        canceled_seller_fees_amount = None

                    product_quantity = reponse_dict.get('product_quantity')

                    SKU_price = 0
                    SKU_parts_price = 0
                    SKU_freight = 0
                    SKU_parts_freight = 0
                    SKU_buy_one_freight = 0
                    Pingyou_min7_SKU_freight = 0
                    Pingyou_max7_SKU_freight = 0
                    try:
                        a = max(models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(
                            STAR_DATE__lte=data_time_paid_at).values_list('STAR_DATE'))[0]
                    except:
                        a = min(models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).values_list(
                            'STAR_DATE'))[0]
                    obj1 = models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(
                        STAR_DATE=a).values()  # 物流规则数据（匹配下单时间的物流规则）
                    if country == 'GBR':
                        普货每克 = float(obj1[0]['英国_每克_普货']) * float(obj1[0]['英国_折扣_普货'])
                        普货挂号 = float(obj1[0]['英国_挂号_普货']) * float(obj1[0]['英国_折扣_普货'])
                        带电每克 = float(obj1[0]['英国_每克_带电']) * float(obj1[0]['英国_折扣_带电'])
                        带电挂号 = float(obj1[0]['英国_挂号_带电']) * float(obj1[0]['英国_折扣_带电'])
                        特货每克 = float(obj1[0]['英国_每克_特货']) * float(obj1[0]['英国_折扣_特货'])
                        特货挂号 = float(obj1[0]['英国_挂号_特货']) * float(obj1[0]['英国_折扣_特货'])
                    elif country == 'CAN':
                        普货每克 = float(obj1[0]['加拿_每克_普货']) * float(obj1[0]['加拿_折扣_普货'])
                        普货挂号 = float(obj1[0]['加拿_挂号_普货']) * float(obj1[0]['加拿_折扣_普货'])
                        带电每克 = float(obj1[0]['加拿_每克_带电']) * float(obj1[0]['加拿_折扣_带电'])
                        带电挂号 = float(obj1[0]['加拿_挂号_带电']) * float(obj1[0]['加拿_折扣_带电'])
                        特货每克 = float(obj1[0]['加拿_每克_特货']) * float(obj1[0]['加拿_折扣_特货'])
                        特货挂号 = float(obj1[0]['加拿_挂号_特货']) * float(obj1[0]['加拿_折扣_特货'])
                    elif country == 'AUS':
                        普货每克 = float(obj1[0]['澳大_每克_普货']) * float(obj1[0]['澳大_折扣_普货'])
                        普货挂号 = float(obj1[0]['澳大_挂号_普货']) * float(obj1[0]['澳大_折扣_普货'])
                        带电每克 = float(obj1[0]['澳大_每克_带电']) * float(obj1[0]['澳大_折扣_带电'])
                        带电挂号 = float(obj1[0]['澳大_挂号_带电']) * float(obj1[0]['澳大_折扣_带电'])
                        特货每克 = float(obj1[0]['澳大_每克_特货']) * float(obj1[0]['澳大_折扣_特货'])
                        特货挂号 = float(obj1[0]['澳大_挂号_特货']) * float(obj1[0]['澳大_折扣_特货'])
                    else:
                        普货每克 = float(obj1[0]['美国_每克_普货']) * float(obj1[0]['美国_折扣_普货'])
                        普货挂号 = float(obj1[0]['美国_挂号_普货']) * float(obj1[0]['美国_折扣_普货'])
                        带电每克 = float(obj1[0]['美国_每克_带电']) * float(obj1[0]['美国_折扣_带电'])
                        带电挂号 = float(obj1[0]['美国_挂号_带电']) * float(obj1[0]['美国_折扣_带电'])
                        特货每克 = float(obj1[0]['美国_每克_特货']) * float(obj1[0]['美国_折扣_特货'])
                        特货挂号 = float(obj1[0]['美国_挂号_特货']) * float(obj1[0]['美国_折扣_特货'])

                    try:
                        obj2 = models_top_hatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(
                            identifier=product_identifier).values()  # 商品基本参数

                        if obj2[0]['SKU_price']:
                            price = obj2[0]['SKU_price']
                        else:
                            price = '0'

                        if obj2[0]['SKU_parts_price']:
                            parts_price = obj2[0]['SKU_parts_price']
                        else:
                            parts_price = '0'

                        if obj2[0]['SKU_weight']:
                            weight = obj2[0]['SKU_weight']
                        else:
                            weight = '0'

                        if obj2[0]['SKU_parts_weight']:
                            parts_weight = obj2[0]['SKU_parts_weight']
                        else:
                            parts_weight = '0'

                        if obj2[0]['HAI_SKU_freight']:
                            HAI_SKU_freight = obj2[0]['HAI_SKU_freight']
                        else:
                            HAI_SKU_freight = '0'

                        if obj2[0]['Pingyou_min7_SKU_freight']:
                            Pingyou_min7_SKU_freight = obj2[0]['Pingyou_min7_SKU_freight']
                        else:
                            Pingyou_min7_SKU_freight = '0'

                        if obj2[0]['Pingyou_max7_SKU_freight']:
                            Pingyou_max7_SKU_freight = obj2[0]['Pingyou_max7_SKU_freight']
                        else:
                            Pingyou_max7_SKU_freight = '0'

                        if obj2[0]['SKU_variety'] == '普货':
                            SKU_freight = (float(weight) * 普货每克) + 普货挂号
                            if upsells_type_description2:
                                SKU_parts_freight = float(parts_weight) * 普货每克
                            if upsells_type_description1:
                                SKU_buy_one_freight = float(weight) * 普货每克
                        elif obj2[0]['SKU_variety'] == '带电':
                            SKU_freight = (float(weight) * 带电每克) + 带电挂号
                            if upsells_type_description2:
                                SKU_parts_freight = float(parts_weight) * 带电每克
                            if upsells_type_description1:
                                SKU_buy_one_freight = float(weight) * 带电每克
                        elif obj2[0]['SKU_variety'] == '特货':
                            SKU_freight = (float(weight) * 特货每克) + 特货挂号
                            if upsells_type_description2:
                                SKU_parts_freight = float(parts_weight) * 特货每克
                            if upsells_type_description1:
                                SKU_buy_one_freight = float(weight) * 特货每克
                        elif obj2[0]['SKU_variety'] == '海运' or obj2[0]['SKU_variety'] == '输入运费':
                            SKU_freight = float(HAI_SKU_freight)
                        elif obj2[0]['SKU_variety'] == '平邮':
                            if (float(disbursement_amount) + float(seller_fees_amount)) < 7:
                                SKU_freight = float(Pingyou_min7_SKU_freight)
                            else:
                                SKU_freight = float(Pingyou_max7_SKU_freight)

                        else:
                            SKU_freight = 0
                            SKU_parts_freight = 0
                            SKU_buy_one_freight = 0

                        SKU_price = round(float(price), 2)
                        SKU_freight = round(SKU_freight, 2)
                        SKU_parts_freight = round(SKU_parts_freight, 2)
                        if SKU_parts_freight:
                            SKU_parts_price = round(float(parts_price), 2)
                        else:
                            SKU_parts_price = 0
                        SKU_buy_one_freight = round(SKU_buy_one_freight, 2)
                        if SKU_buy_one_freight:
                            SKU_buy_one_price = round(float(price), 2)
                        else:
                            SKU_buy_one_price = 0
                    except Exception as e:
                        print(e)

                    idenx = models_top_hatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(order_id=order_id)
                    if idenx:
                        # print('替换')
                        # print(idenx)
                        try:
                            models_top_hatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(order_id=order_id) \
                                .update(
                                status=status,
                                status_paid=status_paid,
                                status_shipped=status_shipped,
                                status_refunded=status_refunded,
                                carrier=carrier,
                                tracking_number=tracking_number,
                                related_order_ids=related_order_ids,
                                service_type=service_type,
                                # fulfillment_partner = fulfillment_partner,
                                # product_name = product_name,
                                # product_identifier = product_identifier,
                                # product_internal_id = product_internal_id,
                                # variation_identifier = variation_identifier,
                                # variation_internal_id = variation_internal_id,
                                # customer_id = customer_id,
                                # customer_name = customer_name,
                                # address1 = address1,
                                # address2 = address2,
                                # city = city,
                                # state = state,
                                # postal_code = postal_code,
                                # country = country,
                                # available_refunds_buyer_fee = available_refunds_buyer_fee,
                                refund_amount=refund_amount,
                                disbursement_amount=disbursement_amount,
                                seller_fees_amount=seller_fees_amount,

                                seller_fees_type_sfb=seller_fees_type_sfb,
                                seller_fees_amount_sfb=seller_fees_amount_sfb,
                                seller_fees_type_com=seller_fees_type_com,
                                seller_fees_amount_com=seller_fees_amount_com,
                                seller_fees_type_pro=seller_fees_type_pro,
                                seller_fees_amount_pro=seller_fees_amount_pro,
                                seller_fees_type_buy_nows=seller_fees_type_buy_nows,
                                seller_fees_type_buy_nows_price=seller_fees_type_buy_nows_price,

                                upsells_type_description1=upsells_type_description1,
                                upsells_amount1=upsells_amount1,
                                upsells_description1=upsells_description1,
                                upsells_type_description2=upsells_type_description2,
                                upsells_amount2=upsells_amount2,
                                upsells_description2=upsells_description2,

                                refunded_at=refunded_at,
                                refunded_at_own=refunded_at_own,
                                refunded_at_buyer=refunded_at_buyer,
                                refund_amount_own=refund_amount_own,
                                refund_amount_buyer=refund_amount_buyer,
                                paid_at=paid_at,
                                created_at=created_at,
                                updated_at=updated_at,
                                canceled_at=canceled_at,

                                canceled_refund_amount=canceled_refund_amount,
                                canceled_disbursement_amount=canceled_disbursement_amount,
                                canceled_seller_fees_amount=canceled_seller_fees_amount,

                                data_time_created_at=data_time_created_at,
                                hours_time_created_at=hours_time_created_at,
                                data_time_paid_at=data_time_paid_at,
                                product_quantity=product_quantity,

                                SKU_price=SKU_price,
                                SKU_freight=SKU_freight,
                                SKU_parts_price=SKU_parts_price,
                                SKU_parts_freight=SKU_parts_freight,
                                SKU_buy_one_price=SKU_buy_one_price,
                                SKU_buy_one_freight=SKU_buy_one_freight
                            )
                            print(PAGE + store_name + '订单数据替换(1) success')
                        except Exception as e:
                            print(e)
                            print('替换 storedata faile')
                    else:
                        try:
                            twz = models_top_hatter.StoreSellData.objects.create(
                                USER_ID=USER_ID,
                                store_name=store_name,
                                order_id=order_id,
                                related_order_ids=related_order_ids,
                                service_type=service_type,

                                status=status,
                                status_paid=status_paid,
                                status_shipped=status_shipped,
                                status_refunded=status_refunded,
                                carrier=carrier,
                                tracking_number=tracking_number,
                                fulfillment_partner=fulfillment_partner,
                                product_name=product_name,
                                product_identifier=product_identifier,
                                product_internal_id=product_internal_id,
                                variation_identifier=variation_identifier,
                                variation_internal_id=variation_internal_id,
                                customer_id=customer_id,
                                customer_name=customer_name,
                                address1=address1,
                                address2=address2,
                                city=city,
                                state=state,
                                postal_code=postal_code,
                                country=country,
                                # available_refunds_buyer_fee = available_refunds_buyer_fee,
                                refund_amount=refund_amount,
                                disbursement_amount=disbursement_amount,
                                seller_fees_amount=seller_fees_amount,

                                seller_fees_type_sfb=seller_fees_type_sfb,
                                seller_fees_amount_sfb=seller_fees_amount_sfb,
                                seller_fees_type_com=seller_fees_type_com,
                                seller_fees_amount_com=seller_fees_amount_com,
                                seller_fees_type_pro=seller_fees_type_pro,
                                seller_fees_amount_pro=seller_fees_amount_pro,
                                seller_fees_type_buy_nows=seller_fees_type_buy_nows,
                                seller_fees_type_buy_nows_price=seller_fees_type_buy_nows_price,

                                upsells_type_description1=upsells_type_description1,
                                upsells_amount1=upsells_amount1,
                                upsells_description1=upsells_description1,
                                upsells_type_description2=upsells_type_description2,
                                upsells_amount2=upsells_amount2,
                                upsells_description2=upsells_description2,

                                refunded_at=refunded_at,
                                refunded_at_own=refunded_at_own,
                                refunded_at_buyer=refunded_at_buyer,
                                refund_amount_own=refund_amount_own,
                                refund_amount_buyer=refund_amount_buyer,
                                paid_at=paid_at,
                                created_at=created_at,
                                updated_at=updated_at,
                                canceled_at=canceled_at,

                                canceled_refund_amount=canceled_refund_amount,
                                canceled_disbursement_amount=canceled_disbursement_amount,
                                canceled_seller_fees_amount=canceled_seller_fees_amount,

                                data_time_created_at=data_time_created_at,
                                hours_time_created_at=hours_time_created_at,
                                data_time_paid_at=data_time_paid_at,
                                product_quantity=product_quantity,

                                SKU_price=SKU_price,
                                SKU_freight=SKU_freight,
                                SKU_parts_price=SKU_parts_price,
                                SKU_parts_freight=SKU_parts_freight,
                                SKU_buy_one_price=SKU_buy_one_price,
                                SKU_buy_one_freight=SKU_buy_one_freight
                            )
                            twz.save()
                            print(PAGE + store_name + '订单数据保存(1) success')
                            # print(PAGE)
                        except Exception as e:
                            print(e)
                            print('保存 storedata faile')
            except Exception as e:
                print(e)
                print('not this storedata 数据')
                # return False


# 获取后台API销售数据存到数据库(订单数据3小时一次，4000单)
def get_store_data_2():
    # 1 删除2021年数据

    # 2 获取到数据
    for PAGE in range(3, 50):
        models_top_hatter.StoreSellData.objects.filter(paid_at__lte='2021-01-01 00:00:00').delete()

        PAGE = str(PAGE)
        print('storedata1--' + PAGE)
        i = 0
        for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
            try:
                store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][0]
                store_APIToken = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_APIToken')[0][
                    0]
                USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]

                data = {
                    'access_token': store_APIToken,
                    'page': PAGE,
                    'per_page': '200'
                }
                # print(PAGE)
                # print(store_APIToken)
                subm = requests.get('https://tophatter.com/merchant_api/v1/orders.json', data=data, timeout=100)

                # subm = requests.get(url)
                print("status code:", subm.status_code)
                aa = subm.text
                reponse_dicts = json.loads(aa)

                # 2 保存到数据库
                # print(len(reponse_dicts))
                for reponse_dict in reponse_dicts:
                    order_id = reponse_dict.get('order_id')
                    status = reponse_dict.get('status')

                    if status == 'paid':
                        status_paid = status + str(order_id)
                        status_shipped = None
                        status_refunded = None
                    elif status == 'shipped':
                        status_paid = None
                        status_shipped = status + str(order_id)
                        status_refunded = None
                    elif status == 'refunded':
                        status_paid = None
                        status_shipped = None
                        status_refunded = status + str(order_id)

                    carrier = reponse_dict.get('carrier')
                    tracking_number = reponse_dict.get('tracking_number')
                    fulfillment_partner = reponse_dict.get('fulfillment_partner')
                    product_name = reponse_dict.get('product_name')
                    product_identifier = reponse_dict.get('product_identifier')
                    product_internal_id = reponse_dict.get('product_internal_id')
                    variation_identifier = reponse_dict.get('variation_identifier')
                    variation_internal_id = reponse_dict.get('variation_internal_id')
                    customer_id = reponse_dict.get('customer_id')
                    customer_name = reponse_dict.get('customer_name')
                    address1 = reponse_dict.get('address1')
                    address2 = reponse_dict.get('address2')
                    city = reponse_dict.get('city')
                    state = reponse_dict.get('state')
                    postal_code = reponse_dict.get('postal_code')
                    country = reponse_dict.get('country')
                    related_order_ids = reponse_dict.get('related_order_ids')
                    service_type = reponse_dict.get('service_type')

                    # available_refunds_buyer_fee = reponse_dict.get('available_refunds').get('buyer_fee')

                    refund_amount = reponse_dict.get('refund_amount')
                    disbursement_amount = reponse_dict.get('disbursement_amount')
                    seller_fees_amount = reponse_dict.get('seller_fees_amount')

                    seller_fees_type_sfb = None
                    seller_fees_amount_sfb = None
                    seller_fees_type_com = None
                    seller_fees_amount_com = None
                    seller_fees_type_pro = None
                    seller_fees_amount_pro = None
                    ab = reponse_dict.get('seller_fees')
                    # print(ab)
                    if ab:
                        for j in range(len(reponse_dict.get('seller_fees'))):
                            if j == 0:
                                type = reponse_dict.get('seller_fees')[0]['type']
                                amount = reponse_dict.get('seller_fees')[0]['amount']
                                if type == 'scheduling_fee':
                                    seller_fees_type_sfb = type + str(order_id)
                                    seller_fees_amount_sfb = amount
                                elif type == 'commission_fee':
                                    seller_fees_type_com = type + str(order_id)
                                    seller_fees_amount_com = amount
                                elif type == 'processing_fee':
                                    seller_fees_type_pro = type + str(order_id)
                                    seller_fees_amount_pro = amount

                            if j == 1:
                                type1 = reponse_dict.get('seller_fees')[1]['type']
                                amount1 = reponse_dict.get('seller_fees')[1]['amount']
                                if type1 == 'scheduling_fee':
                                    seller_fees_type_sfb = type1 + str(order_id)
                                    seller_fees_amount_sfb = amount1
                                elif type1 == 'commission_fee':
                                    seller_fees_type_com = type1 + str(order_id)
                                    seller_fees_amount_com = amount1
                                elif type1 == 'processing_fee':
                                    seller_fees_type_pro = type1 + str(order_id)
                                    seller_fees_amount_pro = amount1

                            if j == 2:
                                type2 = reponse_dict.get('seller_fees')[2]['type']
                                amount2 = reponse_dict.get('seller_fees')[2]['amount']
                                if type2 == 'scheduling_fee':
                                    seller_fees_type_sfb = type2 + str(order_id)
                                    seller_fees_amount_sfb = amount2
                                elif type2 == 'commission_fee':
                                    seller_fees_type_com = type2 + str(order_id)
                                    seller_fees_amount_com = amount2
                                elif type2 == 'processing_fee':
                                    seller_fees_type_pro = type2 + str(order_id)
                                    seller_fees_amount_pro = amount2

                    if seller_fees_type_sfb == None:
                        seller_fees_type_buy_nows = 'buy_nows' + str(order_id)
                        seller_fees_type_buy_nows_price = disbursement_amount
                    else:
                        seller_fees_type_buy_nows = None
                        seller_fees_type_buy_nows_price = None

                    upsells_type_description1 = None
                    upsells_amount1 = None
                    upsells_description1 = None
                    upsells_type_description2 = None
                    upsells_amount2 = None
                    upsells_description2 = None

                    a = reponse_dict.get('upsells')
                    if a:
                        for j in range(len(reponse_dict.get('upsells'))):
                            if j == 0:
                                type = reponse_dict.get('upsells')[0]['type_description']
                                amount = reponse_dict.get('upsells')[0]['amount']
                                description = reponse_dict.get('upsells')[0]['description']
                                if type == 'buy_one_get_one':
                                    upsells_type_description1 = type + str(order_id)
                                    upsells_amount1 = amount
                                    upsells_description1 = description
                                elif type == 'accessory':
                                    upsells_type_description2 = type + str(order_id)
                                    upsells_amount2 = amount
                                    upsells_description2 = description
                            if j == 1:
                                type2 = reponse_dict.get('upsells')[1]['type_description']
                                amount2 = reponse_dict.get('upsells')[1]['amount']
                                description2 = reponse_dict.get('upsells')[1]['description']
                                if type2 == 'buy_one_get_one':
                                    upsells_type_description1 = type2 + str(order_id)
                                    upsells_amount1 = amount2
                                    upsells_description1 = description2
                                elif type2 == 'accessory':
                                    upsells_type_description2 = type2 + str(order_id)
                                    upsells_amount2 = amount2
                                    upsells_description2 = description2

                    created_at = reponse_dict.get('created_at')
                    if created_at:
                        created_at = reponse_dict.get('created_at')[0:18]
                        data_time_created_at = created_at[0:10]
                        hours_time_created_at = created_at[11:13]
                    else:
                        created_at = None
                        data_time_created_at = None
                        hours_time_created_at = None

                    paid_at = reponse_dict.get('paid_at')
                    if paid_at:
                        paid_at = reponse_dict.get('paid_at')[0:18]
                        data_time_paid_at = paid_at[0:10]
                    else:
                        paid_at = None
                        data_time_paid_at = None

                    refunded_at = reponse_dict.get('refunded_at')
                    if refunded_at:
                        refunded_at = reponse_dict.get('refunded_at')[0:18]
                        refunded_AT = datetime.datetime.strptime(refunded_at, "%Y-%m-%dT%H:%M:%S")
                        created_AT = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
                        aa = (refunded_AT - created_AT).days
                        # print(aa)
                        if tracking_number:
                            # print(refunded_AT - created_AT)
                            refunded_at_own = None
                            refunded_at_buyer = refunded_at
                            refund_amount_own = None
                            refund_amount_buyer = disbursement_amount
                        else:
                            refunded_at_own = refunded_at
                            refunded_at_buyer = None
                            refund_amount_own = disbursement_amount
                            refund_amount_buyer = None
                    else:
                        refunded_at_own = None
                        refunded_at_buyer = None
                        refund_amount_own = None
                        refund_amount_buyer = None

                    updated_at = reponse_dict.get('updated_at')
                    if updated_at:
                        updated_at = reponse_dict.get('updated_at')[0:18]
                    else:
                        updated_at = None

                    canceled_at = reponse_dict.get('canceled_at')
                    if canceled_at:
                        canceled_at = reponse_dict.get('canceled_at')[0:18]
                        canceled_refund_amount = refund_amount
                        canceled_disbursement_amount = disbursement_amount
                        canceled_seller_fees_amount = seller_fees_amount
                    else:
                        canceled_at = None
                        canceled_refund_amount = None
                        canceled_disbursement_amount = None
                        canceled_seller_fees_amount = None

                    product_quantity = reponse_dict.get('product_quantity')

                    SKU_price = 0
                    SKU_parts_price = 0
                    SKU_freight = 0
                    SKU_parts_freight = 0
                    SKU_buy_one_freight = 0
                    Pingyou_min7_SKU_freight = 0
                    Pingyou_max7_SKU_freight = 0
                    try:
                        a = max(models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(
                            STAR_DATE__lte=data_time_paid_at).values_list('STAR_DATE'))[0]
                    except:
                        a = min(models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).values_list(
                            'STAR_DATE'))[0]
                    obj1 = models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(
                        STAR_DATE=a).values()  # 物流规则数据（匹配下单时间的物流规则）
                    if country == 'GBR':
                        普货每克 = float(obj1[0]['英国_每克_普货']) * float(obj1[0]['英国_折扣_普货'])
                        普货挂号 = float(obj1[0]['英国_挂号_普货']) * float(obj1[0]['英国_折扣_普货'])
                        带电每克 = float(obj1[0]['英国_每克_带电']) * float(obj1[0]['英国_折扣_带电'])
                        带电挂号 = float(obj1[0]['英国_挂号_带电']) * float(obj1[0]['英国_折扣_带电'])
                        特货每克 = float(obj1[0]['英国_每克_特货']) * float(obj1[0]['英国_折扣_特货'])
                        特货挂号 = float(obj1[0]['英国_挂号_特货']) * float(obj1[0]['英国_折扣_特货'])
                    elif country == 'CAN':
                        普货每克 = float(obj1[0]['加拿_每克_普货']) * float(obj1[0]['加拿_折扣_普货'])
                        普货挂号 = float(obj1[0]['加拿_挂号_普货']) * float(obj1[0]['加拿_折扣_普货'])
                        带电每克 = float(obj1[0]['加拿_每克_带电']) * float(obj1[0]['加拿_折扣_带电'])
                        带电挂号 = float(obj1[0]['加拿_挂号_带电']) * float(obj1[0]['加拿_折扣_带电'])
                        特货每克 = float(obj1[0]['加拿_每克_特货']) * float(obj1[0]['加拿_折扣_特货'])
                        特货挂号 = float(obj1[0]['加拿_挂号_特货']) * float(obj1[0]['加拿_折扣_特货'])
                    elif country == 'AUS':
                        普货每克 = float(obj1[0]['澳大_每克_普货']) * float(obj1[0]['澳大_折扣_普货'])
                        普货挂号 = float(obj1[0]['澳大_挂号_普货']) * float(obj1[0]['澳大_折扣_普货'])
                        带电每克 = float(obj1[0]['澳大_每克_带电']) * float(obj1[0]['澳大_折扣_带电'])
                        带电挂号 = float(obj1[0]['澳大_挂号_带电']) * float(obj1[0]['澳大_折扣_带电'])
                        特货每克 = float(obj1[0]['澳大_每克_特货']) * float(obj1[0]['澳大_折扣_特货'])
                        特货挂号 = float(obj1[0]['澳大_挂号_特货']) * float(obj1[0]['澳大_折扣_特货'])
                    else:
                        普货每克 = float(obj1[0]['美国_每克_普货']) * float(obj1[0]['美国_折扣_普货'])
                        普货挂号 = float(obj1[0]['美国_挂号_普货']) * float(obj1[0]['美国_折扣_普货'])
                        带电每克 = float(obj1[0]['美国_每克_带电']) * float(obj1[0]['美国_折扣_带电'])
                        带电挂号 = float(obj1[0]['美国_挂号_带电']) * float(obj1[0]['美国_折扣_带电'])
                        特货每克 = float(obj1[0]['美国_每克_特货']) * float(obj1[0]['美国_折扣_特货'])
                        特货挂号 = float(obj1[0]['美国_挂号_特货']) * float(obj1[0]['美国_折扣_特货'])

                    try:
                        obj2 = models_top_hatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(
                            identifier=product_identifier).values()  # 商品基本参数

                        if obj2[0]['SKU_price']:
                            price = obj2[0]['SKU_price']
                        else:
                            price = '0'

                        if obj2[0]['SKU_parts_price']:
                            parts_price = obj2[0]['SKU_parts_price']
                        else:
                            parts_price = '0'

                        if obj2[0]['SKU_weight']:
                            weight = obj2[0]['SKU_weight']
                        else:
                            weight = '0'

                        if obj2[0]['SKU_parts_weight']:
                            parts_weight = obj2[0]['SKU_parts_weight']
                        else:
                            parts_weight = '0'

                        if obj2[0]['HAI_SKU_freight']:
                            HAI_SKU_freight = obj2[0]['HAI_SKU_freight']
                        else:
                            HAI_SKU_freight = '0'

                        if obj2[0]['Pingyou_min7_SKU_freight']:
                            Pingyou_min7_SKU_freight = obj2[0]['Pingyou_min7_SKU_freight']
                        else:
                            Pingyou_min7_SKU_freight = '0'

                        if obj2[0]['Pingyou_max7_SKU_freight']:
                            Pingyou_max7_SKU_freight = obj2[0]['Pingyou_max7_SKU_freight']
                        else:
                            Pingyou_max7_SKU_freight = '0'

                        if obj2[0]['SKU_variety'] == '普货':
                            SKU_freight = (float(weight) * 普货每克) + 普货挂号
                            if upsells_type_description2:
                                SKU_parts_freight = float(parts_weight) * 普货每克
                            if upsells_type_description1:
                                SKU_buy_one_freight = float(weight) * 普货每克
                        elif obj2[0]['SKU_variety'] == '带电':
                            SKU_freight = (float(weight) * 带电每克) + 带电挂号
                            if upsells_type_description2:
                                SKU_parts_freight = float(parts_weight) * 带电每克
                            if upsells_type_description1:
                                SKU_buy_one_freight = float(weight) * 带电每克
                        elif obj2[0]['SKU_variety'] == '特货':
                            SKU_freight = (float(weight) * 特货每克) + 特货挂号
                            if upsells_type_description2:
                                SKU_parts_freight = float(parts_weight) * 特货每克
                            if upsells_type_description1:
                                SKU_buy_one_freight = float(weight) * 特货每克
                        elif obj2[0]['SKU_variety'] == '海运' or obj2[0]['SKU_variety'] == '输入运费':
                            SKU_freight = float(HAI_SKU_freight)
                        elif obj2[0]['SKU_variety'] == '平邮':
                            if (float(disbursement_amount) + float(seller_fees_amount)) < 7:
                                SKU_freight = float(Pingyou_min7_SKU_freight)
                            else:
                                SKU_freight = float(Pingyou_max7_SKU_freight)

                        else:
                            SKU_freight = 0
                            SKU_parts_freight = 0
                            SKU_buy_one_freight = 0

                        SKU_price = round(float(price), 2)
                        SKU_freight = round(SKU_freight, 2)
                        SKU_parts_freight = round(SKU_parts_freight, 2)
                        if SKU_parts_freight:
                            SKU_parts_price = round(float(parts_price), 2)
                        else:
                            SKU_parts_price = 0
                        SKU_buy_one_freight = round(SKU_buy_one_freight, 2)
                        if SKU_buy_one_freight:
                            SKU_buy_one_price = round(float(price), 2)
                        else:
                            SKU_buy_one_price = 0
                    except Exception as e:
                        print(e)

                    idenx = models_top_hatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(order_id=order_id)
                    if idenx:
                        # print('替换')
                        # print(idenx)
                        try:
                            models_top_hatter.StoreSellData.objects.filter(USER_ID=USER_ID).filter(order_id=order_id) \
                                .update(
                                status=status,
                                status_paid=status_paid,
                                status_shipped=status_shipped,
                                status_refunded=status_refunded,
                                carrier=carrier,
                                tracking_number=tracking_number,
                                related_order_ids=related_order_ids,
                                service_type=service_type,
                                # fulfillment_partner = fulfillment_partner,
                                # product_name = product_name,
                                # product_identifier = product_identifier,
                                # product_internal_id = product_internal_id,
                                # variation_identifier = variation_identifier,
                                # variation_internal_id = variation_internal_id,
                                # customer_id = customer_id,
                                # customer_name = customer_name,
                                # address1 = address1,
                                # address2 = address2,
                                # city = city,
                                # state = state,
                                # postal_code = postal_code,
                                # country = country,
                                # available_refunds_buyer_fee = available_refunds_buyer_fee,
                                refund_amount=refund_amount,
                                disbursement_amount=disbursement_amount,
                                seller_fees_amount=seller_fees_amount,

                                seller_fees_type_sfb=seller_fees_type_sfb,
                                seller_fees_amount_sfb=seller_fees_amount_sfb,
                                seller_fees_type_com=seller_fees_type_com,
                                seller_fees_amount_com=seller_fees_amount_com,
                                seller_fees_type_pro=seller_fees_type_pro,
                                seller_fees_amount_pro=seller_fees_amount_pro,
                                seller_fees_type_buy_nows=seller_fees_type_buy_nows,
                                seller_fees_type_buy_nows_price=seller_fees_type_buy_nows_price,

                                upsells_type_description1=upsells_type_description1,
                                upsells_amount1=upsells_amount1,
                                upsells_description1=upsells_description1,
                                upsells_type_description2=upsells_type_description2,
                                upsells_amount2=upsells_amount2,
                                upsells_description2=upsells_description2,

                                refunded_at=refunded_at,
                                refunded_at_own=refunded_at_own,
                                refunded_at_buyer=refunded_at_buyer,
                                refund_amount_own=refund_amount_own,
                                refund_amount_buyer=refund_amount_buyer,
                                paid_at=paid_at,
                                created_at=created_at,
                                updated_at=updated_at,
                                canceled_at=canceled_at,

                                canceled_refund_amount=canceled_refund_amount,
                                canceled_disbursement_amount=canceled_disbursement_amount,
                                canceled_seller_fees_amount=canceled_seller_fees_amount,

                                data_time_created_at=data_time_created_at,
                                hours_time_created_at=hours_time_created_at,
                                data_time_paid_at=data_time_paid_at,
                                product_quantity=product_quantity,

                                SKU_price=SKU_price,
                                SKU_freight=SKU_freight,
                                SKU_parts_price=SKU_parts_price,
                                SKU_parts_freight=SKU_parts_freight,
                                SKU_buy_one_price=SKU_buy_one_price,
                                SKU_buy_one_freight=SKU_buy_one_freight
                            )
                            print(PAGE + store_name + '订单数据替换(2) success')
                        except Exception as e:
                            print(e)
                            print('替换 storedata faile')
                    else:
                        try:
                            twz = models_top_hatter.StoreSellData.objects.create(
                                USER_ID=USER_ID,
                                store_name=store_name,
                                order_id=order_id,
                                related_order_ids=related_order_ids,
                                service_type=service_type,

                                status=status,
                                status_paid=status_paid,
                                status_shipped=status_shipped,
                                status_refunded=status_refunded,
                                carrier=carrier,
                                tracking_number=tracking_number,
                                fulfillment_partner=fulfillment_partner,
                                product_name=product_name,
                                product_identifier=product_identifier,
                                product_internal_id=product_internal_id,
                                variation_identifier=variation_identifier,
                                variation_internal_id=variation_internal_id,
                                customer_id=customer_id,
                                customer_name=customer_name,
                                address1=address1,
                                address2=address2,
                                city=city,
                                state=state,
                                postal_code=postal_code,
                                country=country,
                                # available_refunds_buyer_fee = available_refunds_buyer_fee,
                                refund_amount=refund_amount,
                                disbursement_amount=disbursement_amount,
                                seller_fees_amount=seller_fees_amount,

                                seller_fees_type_sfb=seller_fees_type_sfb,
                                seller_fees_amount_sfb=seller_fees_amount_sfb,
                                seller_fees_type_com=seller_fees_type_com,
                                seller_fees_amount_com=seller_fees_amount_com,
                                seller_fees_type_pro=seller_fees_type_pro,
                                seller_fees_amount_pro=seller_fees_amount_pro,
                                seller_fees_type_buy_nows=seller_fees_type_buy_nows,
                                seller_fees_type_buy_nows_price=seller_fees_type_buy_nows_price,

                                upsells_type_description1=upsells_type_description1,
                                upsells_amount1=upsells_amount1,
                                upsells_description1=upsells_description1,
                                upsells_type_description2=upsells_type_description2,
                                upsells_amount2=upsells_amount2,
                                upsells_description2=upsells_description2,

                                refunded_at=refunded_at,
                                refunded_at_own=refunded_at_own,
                                refunded_at_buyer=refunded_at_buyer,
                                refund_amount_own=refund_amount_own,
                                refund_amount_buyer=refund_amount_buyer,
                                paid_at=paid_at,
                                created_at=created_at,
                                updated_at=updated_at,
                                canceled_at=canceled_at,

                                canceled_refund_amount=canceled_refund_amount,
                                canceled_disbursement_amount=canceled_disbursement_amount,
                                canceled_seller_fees_amount=canceled_seller_fees_amount,

                                data_time_created_at=data_time_created_at,
                                hours_time_created_at=hours_time_created_at,
                                data_time_paid_at=data_time_paid_at,
                                product_quantity=product_quantity,

                                SKU_price=SKU_price,
                                SKU_freight=SKU_freight,
                                SKU_parts_price=SKU_parts_price,
                                SKU_parts_freight=SKU_parts_freight,
                                SKU_buy_one_price=SKU_buy_one_price,
                                SKU_buy_one_freight=SKU_buy_one_freight
                            )
                            twz.save()
                            print(PAGE + store_name + '订单数据保存(2) success')
                            # print(PAGE)
                        except Exception as e:
                            print(e)
                            print('保存 storedata faile')
            except Exception as e:
                print(e)
                print('not this storedata 数据')
                # return False


# 获取所有商品到数据库(商品数据)
def get_Pruducts():
    # 1 获取到数据
    # models.Products.objects.all().delete()
    for PAGE in range(1, 6):
        try:
            # print(PAGE)
            PAGE = str(PAGE)
            STATUS = ['in_stock', 'enabled', 'disabled', 'deleted']
            for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
                try:
                    try:
                        store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][
                            0]
                        store_APIToken = \
                            models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_APIToken')[0][0]
                        USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]

                        for STATU in STATUS:
                            try:
                                subm = requests.get(
                                    'https://tophatter.com/merchant_api/v1/products.json?access_token=' + store_APIToken + '&status=' + STATU + '&page=' + PAGE + '&per_page=999',
                                    timeout=100)
                                # https://tophatter.com/merchant_api/v1/products.json?access_token=9101c42416cf871d0604530b9cf88183&status=enabled&page=1&per_page=599
                                # print("status code:", subm.status_code)
                                aa = subm.text
                                reponse_dicts = json.loads(aa)
                                # 2 保存到数据库
                                for reponse_dict in reponse_dicts:
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

                                    itms = models_common_functions.Data_TopData.objects.filter(
                                        product_parent_id=internal_id).values('standard_product_id')
                                    if itms:
                                        standard_product_id = itms[0]['standard_product_id']
                                    else:
                                        standard_product_id = None

                                    idenx = models_top_hatter.Products.objects.filter(USER_ID=USER_ID).filter(
                                        identifier=identifier)
                                    if idenx:
                                        try:
                                            models_top_hatter.Products.objects.filter(USER_ID=USER_ID).filter(
                                                identifier=identifier).update(
                                                status=STATU,
                                                store_name=store_name,
                                                identifier=identifier,
                                                internal_id=internal_id,
                                                standard_product_id=standard_product_id,
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
                                            print(store_name + '商品数据替换 success' + '(' + PAGE + ')')
                                        except Exception as e:
                                            print(e)
                                            print('商品数据替换  faile')
                                    else:
                                        try:
                                            twz = models_top_hatter.Products.objects.create(
                                                USER_ID=USER_ID,
                                                status=STATU,
                                                store_name=store_name,
                                                identifier=identifier,
                                                internal_id=internal_id,
                                                standard_product_id=standard_product_id,
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
                                            print(store_name + '商品数据保存 success' + '(' + PAGE + ')')
                                        except Exception as e:
                                            print(e)
                                            print('商品数据保存  faile')
                            except Exception as e:
                                print(e)
                                print('not this Pruducts 数据')
                    except Exception as e:
                        print(e)
                        print('1')
                except Exception as e:
                    print(e)
                    print('2')
        except Exception as e:
            print(e)
            print('3')


# 获取campaign_list
def get_campaign_list():
    # 1 获取到数据
    try:
        for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
            try:
                store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][0]
                store_APIToken = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_APIToken')[0][
                    0]
                USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]
                try:
                    subm = requests.get(
                        'https://tophatter.com/merchant_api/v1/campaigns.json?access_token=' + store_APIToken + '&per_page=1000',
                        timeout=100)
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

                        idenx = models_top_hatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(
                            store_name=store_name).filter(name=name)
                        if idenx:
                            try:
                                models_top_hatter.campaign_list.objects.filter(USER_ID=USER_ID).filter(
                                    store_name=store_name).filter(name=name).update(
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
                                print(store_name + 'CPM替换 success')
                            except Exception as e:
                                print('CPM替换  faile')
                        else:
                            try:
                                twz = models_top_hatter.campaign_list.objects.create(
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
    except Exception as e:
        print(e)
        print('2')


# 获取店铺资金数据（页面抓取）
def get_founds_data():
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    now_utc = datetime.datetime.now() - datetime.timedelta(hours=15)
    now_utc = now_utc.strftime('%Y-%m-%d %H:%M:%S')
    print('使用注意：1、cookies过期需要替换。')
    print('北京时间：' + now)
    print('旧金山时间：' + now_utc)
    print('正在获取资金请求、请稍后……')

    a = str(datetime.datetime.now() - datetime.timedelta(hours=15))[11:13]
    if a == '01' or a == '03' or a == '07' or a == '10' or a == '13' or a == '16' or a == '19' or a == '22':
        for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
            csrf_token_0 = '0'
            csrf_token_1 = '0'
            store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][0]
            cookie = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_cookie')[0][0]
            USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]
            IP_address = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('IP_address')[0][0]
            message = True
            dd = 0
            while message == True:
                time.sleep(2)  # 延时4秒，避免请求过于频繁。
                if IP_address:
                    proxies_founds = {
                        'http': 'socks5://{}'.format(IP_address),
                        'https': 'socks5://{}'.format(IP_address)
                    }
                    try:
                        proxy = proxies_founds
                        headers = {
                            'accept': 'application/json, text/plain, */*',
                            'accept-encoding': 'gzip, deflate, br',
                            'accept-language': 'zh-CN,zh;q=0.9',
                            'cookie': cookie,
                            'HOST': 'cn.tophatter.com',
                            'referer': 'https://cn.tophatter.com/seller/orders?filter=shipped&tracking_status=unknown',
                            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        }
                        ######################################## IP地址数据 ########################
                        # s = requests.session()
                        # s.proxies.update(proxy)
                        # res = s.get('http://myip.ipip.net/')
                        # soup = BeautifulSoup(res.text, 'html.parser').text[:-1]
                        # print(soup)
                        time.sleep(2)  # 延时2秒，避免请求过于频繁。

                        ######################################## upcoming ###############################
                        try:
                            s = requests.session()
                            s.headers.update(headers)
                            s.proxies.update(proxy)
                            res = s.get('https://cn.tophatter.com/seller/payouts?type=ready', timeout=60)
                            if res.status_code != 200:
                                print('cookie过期，请更新！')
                                input("输入回车键结束")
                            else:
                                print('cookie正常！')
                            soup = BeautifulSoup(res.text, 'html.parser')
                            csrf_token_0 = soup.find('td', {"class": "w-25 text-strong"}).text
                            csrf_token_0_0 = csrf_token_0[1:2]
                            csrf_token_0 = re.search(r'[^$]+$', csrf_token_0).group(0)[:-1]
                            if csrf_token_0_0 == '-':
                                csrf_token_0 = csrf_token_0_0 + csrf_token_0
                            csrf_token_0 = re.sub('[,]', '', csrf_token_0)
                        except Exception as e:
                            csrf_token_0 = '0'
                            print(e)
                        time.sleep(4)  # 延时2秒，避免请求过于频繁。
                        ######################################## pending ################################
                        try:
                            s = requests.session()
                            s.headers.update(headers)
                            s.proxies.update(proxy)
                            res = s.get('https://cn.tophatter.com/seller/payouts?type=awaiting', timeout=60)
                            soup = BeautifulSoup(res.text, 'html.parser')
                            csrf_token_1 = soup.find('td', {"class": "w-25 text-strong"}).text
                            csrf_token_1_1 = csrf_token_1[1:2]
                            csrf_token_1 = re.search(r'[^$]+$', csrf_token_1).group(0)[:-1]
                            if csrf_token_1_1 == '-':
                                csrf_token_1 = csrf_token_1_1 + csrf_token_1
                            csrf_token_1 = re.sub('[,]', '', csrf_token_1)
                        except Exception as e:
                            csrf_token_1 = '0'
                            print(e)
                        time.sleep(4)  # 延时2秒，避免请求过于频繁。
                        ######################################## 获取数据正常，跳出循环 ########################
                        print('账号资金成功：' + store_name)
                        # print('店铺资金为:' + csrf_token_0, csrf_token_1, )
                        message = False
                    except Exception as e:
                        csrf_token_0 = '0'
                        csrf_token_1 = '0'
                        print(e)
                        print('继续访问' + str(dd))
                        dd = dd + 1
                        if dd > 10:
                            message = False
            ######################### 保存店铺资金数据 #############################
            try:
                Upcoming = csrf_token_0
                Pending = csrf_token_1
                try:
                    ind = models_top_hatter.Founds.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).filter(
                        Time_Date=(datetime.datetime.now() - datetime.timedelta(hours=15)).date())
                    if ind:
                        if Pending != '' or Upcoming != '':
                            models_top_hatter.Founds.objects.filter(USER_ID=USER_ID).filter(
                                store_name=store_name).filter(
                                Time_Date=(datetime.datetime.now() - datetime.timedelta(hours=15)).date()).update(
                                Upcoming=Upcoming,
                                Pending=Pending,
                                save_time=datetime.datetime.now())
                    else:
                        if Upcoming == '':
                            Upcoming = '0'
                        if Pending == '':
                            Pending = '0'

                        twz = models_top_hatter.Founds.objects.create(store_name=store_name,
                                                                      USER_ID=USER_ID,
                                                                      Upcoming=Upcoming,
                                                                      Pending=Pending,
                                                                      Time_Date=(
                                                                              datetime.datetime.now() - datetime.timedelta(
                                                                          hours=15)).date())
                        twz.save()
                except Exception as e:
                    print(e)
                    print('保存店铺资金数据数据失败，店铺：' + str(store_name) + str(USER_ID))
            except Exception as e:
                print(e)
        print('******店铺资金获取完成******')
    else:
        print('******店铺资金未到指定时间******')


def get_buynow_data():
    print('正在获取一口价页面数据、请稍后……')
    models_top_hatter.buynows_oders.objects.filter(~Q(TIME_SELECT=None)).delete()  # 更新当天数据
    models_top_hatter.buynows_statistics.objects.filter(~Q(TIME_SELECT=None)).delete()  # 更新当天数据
    aa = (datetime.datetime.now() - datetime.timedelta(hours=16) - datetime.timedelta(days=1)).date()
    bb = max(models_top_hatter.buynows_oders.objects.filter(TIME_SELECT=None).filter(
        time_hours_local_symbol='yestoday').values_list('time_local'))[0]
    for i in models_top_hatter.APIAccessToken.objects.values_list('id', flat=True):
        store_name = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_name')[0][0]
        cookie = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('store_cookie')[0][0]
        USER_ID = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('USER_ID')[0][0]
        IP_address = models_top_hatter.APIAccessToken.objects.filter(id=i).values_list('IP_address')[0][0]
        message = True
        dd = 0
        while message == True:
            time.sleep(2)  # 延时4秒，避免请求过于频繁。
            if IP_address:
                proxies_founds = {
                    'http': 'socks5://{}'.format(IP_address),
                    'https': 'socks5://{}'.format(IP_address)
                }
                try:
                    proxy = proxies_founds
                    headers = {
                        'accept': 'application/json, text/plain, */*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'cookie': cookie,
                        'HOST': 'cn.tophatter.com',
                        'referer': 'https://cn.tophatter.com/seller/orders?filter=shipped&tracking_status=unknown',
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    }
                    ######################################## IP地址数据 ########################
                    # s = requests.session()
                    # s.proxies.update(proxy)
                    # res = s.get('http://myip.ipip.net/')
                    # soup = BeautifulSoup(res.text, 'html.parser').text[:-1]
                    # print(soup)
                    time.sleep(2)  # 延时2秒，避免请求过于频繁。
                    ######################################## 一口价数据—today ########################
                    try:
                        s = requests.session()
                        s.headers.update(headers)
                        s.proxies.update(proxy)
                        res = s.get('https://cn.tophatter.com/seller/statistics/buy_nows', timeout=60)  # 一口价—today
                        soup = BeautifulSoup(res.text, 'html.parser')
                    except Exception as e:
                        print(e)
                    ######################################## 一口价数据--Yestoday ########################
                    try:
                        s = requests.session()
                        s.headers.update(headers)
                        s.proxies.update(proxy)
                        res = s.get('https://cn.tophatter.com/seller/statistics/buy_nows?duration=yesterday',
                                    timeout=60)  # 一口价——yestoday
                        soup_yestoday = BeautifulSoup(res.text, 'html.parser')
                    except Exception as e:
                        print(e)
                    ####################################### home页 GOTO 提醒数据 ########################
                    try:
                        s = requests.session()
                        s.headers.update(headers)
                        s.proxies.update(proxy)
                        res = s.get('https://cn.tophatter.com/seller/home', timeout=60)  # home页 GOTO 提醒数据
                        soup_home_GOTO = BeautifulSoup(res.text, 'html.parser')
                    except Exception as e:
                        print(e)
                    ######################################## 获取数据正常，跳出循环 ########################
                    print('账号一口价数据成功：' + store_name)
                    message = False
                except Exception as e:
                    print(e)
                    print('继续访问' + str(dd))
                    dd = dd + 1
                    if dd > 10:
                        message = False
        ########################## 保存一口价数据—today ###############################
        ####### 获取并分析数据#######
        try:
            html_buynows_1 = soup.find('table', {"class": "table table-bordered table-striped"}).tbody.find_all('td')
            buynows_statistics_all = []
            for html_buynows1 in html_buynows_1:  # 一口价列表的 统计栏目  内容
                buynows_statistics = html_buynows1.text
                buynows_statistics = re.sub('[$]', '', buynows_statistics)
                buynows_statistics = re.sub('[\n]', '', buynows_statistics)
                buynows_statistics_all.append(buynows_statistics)

            html_buynows_4 = soup.find('div', {"class": "table-responsive"}).tbody.find_all('tr')
            buynows_oders_all = []
            for html_buynows4 in html_buynows_4:  # 一口价列表的 详细列表数据   内容
                html_buynows = html_buynows4.find_all('td')
                buynows_oders_SKU = html_buynows[0].a['title']
                buynows_oders_SKU = re.sub(r':.*$', "", buynows_oders_SKU)  ############ SKU
                buynows_oders_all.append(buynows_oders_SKU)
                buynows_oders_img = html_buynows[0].img['src']  ######################## 主图
                buynows_oders_all.append(buynows_oders_img)
                buynows_oders_describe = html_buynows[0].a['title']  ################### 描述
                buynows_oders_describe = re.sub(r'^.*:', "", buynows_oders_describe)
                buynows_oders_all.append(buynows_oders_describe)
                for html in html_buynows[1:]:
                    buynows_oders_content = html.text
                    buynows_oders_content = re.sub('[$]', '', buynows_oders_content)
                    buynows_oders_content = re.sub('[\n]', '', buynows_oders_content)
                    buynows_oders_all.append(buynows_oders_content)
                ####### 详细数据栏#######
                identifier_oders = buynows_oders_all[0]
                img_buynows_oders = buynows_oders_all[1]
                describe_oders = buynows_oders_all[2]
                Impressions_oders = buynows_oders_all[3]
                Views_oders = buynows_oders_all[4]
                Orders_oders = buynows_oders_all[5]
                Fees_oders = buynows_oders_all[6]
                CPM_oders = buynows_oders_all[7]
                Cost_per_Order_oders = buynows_oders_all[8]
                buynows_oders_all = []
                try:
                    models_top_hatter.buynows_oders.objects.create(
                        USER_ID=USER_ID,
                        store_name=store_name,
                        identifier=identifier_oders,
                        img_buynows=img_buynows_oders,
                        describe=describe_oders,
                        Impressions=Impressions_oders,
                        Views=Views_oders,
                        Orders=Orders_oders,
                        Fees=Fees_oders,
                        CPM=CPM_oders,
                        Cost_per_Order=Cost_per_Order_oders,
                        time_local=(datetime.datetime.now() - datetime.timedelta(hours=15)).date(),
                        TIME_SELECT='Today',
                    ).save()

                except Exception as e:
                    print(e)
                    print('保存一口价详细列表数据数据失败，店铺：' + store_name)

                # 按照特定时间点保存数据 3小时
                a = str(datetime.datetime.now() - datetime.timedelta(hours=15))[11:13]
                if a == '03' or a == '06' or a == '09' or a == '12' or a == '15' or a == '18' or a == '21' or a == '23':
                    aaa = str(datetime.datetime.now() - datetime.timedelta(hours=15))[0:13]
                    time_hours_local = datetime.datetime.strptime(aaa + ':00:00', '%Y-%m-%d %H:%M:%S')
                    try:
                        models_top_hatter.buynows_oders.objects.create(
                            USER_ID=USER_ID,
                            store_name=store_name,
                            identifier=identifier_oders,
                            img_buynows=img_buynows_oders,
                            describe=describe_oders,
                            Impressions=Impressions_oders,
                            Views=Views_oders,
                            Orders=Orders_oders,
                            Fees=Fees_oders,
                            CPM=CPM_oders,
                            Cost_per_Order=Cost_per_Order_oders,
                            time_local=(datetime.datetime.now() - datetime.timedelta(hours=15)).date(),
                            time_hours_local=time_hours_local,
                            time_hours_local_symbol=a
                        ).save()
                        # print(store_name + ' 3小时_一口价')
                    except Exception as e:
                        print(e)
                        print('3小时_一口价 save faile')
            ####### 统计栏########
            Impressions_statistics = buynows_statistics_all[0]
            Views_statistics = buynows_statistics_all[1]
            Orders_statistics = buynows_statistics_all[2]
            Fees_statistics = buynows_statistics_all[3]
            CPM_statistics = buynows_statistics_all[4]
            Cost_per_Order_statistics = buynows_statistics_all[5]
            buynows_statistics_all = []
            try:
                models_top_hatter.buynows_statistics.objects.create(
                    USER_ID=USER_ID,
                    store_name=store_name,
                    Impressions=Impressions_statistics,
                    Views=Views_statistics,
                    Orders=Orders_statistics,
                    Fees=Fees_statistics,
                    CPM=CPM_statistics,
                    Cost_per_Order=Cost_per_Order_statistics,
                    time_local=(datetime.datetime.now() - datetime.timedelta(hours=15)).date(),
                    TIME_SELECT='Today',
                ).save()
            except Exception as e:
                print(e)
                print('保存一口价页面统计数据失败，店铺：' + store_name)

            # 按照特定时间点保存数据 3小时
            a = str(datetime.datetime.now() - datetime.timedelta(hours=15))[11:13]
            if a == '03' or a == '06' or a == '09' or a == '12' or a == '15' or a == '18' or a == '21' or a == '23':
                aaa = str(datetime.datetime.now() - datetime.timedelta(hours=15))[0:13]
                time_hours_local = datetime.datetime.strptime(aaa + ':00:00', '%Y-%m-%d %H:%M:%S')
                try:
                    models_top_hatter.buynows_statistics.objects.create(
                        USER_ID=USER_ID,
                        store_name=store_name,
                        Impressions=Impressions_statistics,
                        Views=Views_statistics,
                        Orders=Orders_statistics,
                        Fees=Fees_statistics,
                        CPM=CPM_statistics,
                        Cost_per_Order=Cost_per_Order_statistics,
                        time_local=(datetime.datetime.now() - datetime.timedelta(hours=15)).date(),
                        time_hours_local=time_hours_local,
                        time_hours_local_symbol=a
                    ).save()
                    # print(store_name + ' 3小时_一口价')
                except Exception as e:
                    print(e)
                    print('3小时_一口价 save faile')
        except Exception as e:
            print(str(e) + '：无today数据')
        ########################## 保存一口价数据--Yestoday ###############################
        ####### 获取并分析数据#######
        try:
            html_buynows_1 = soup_yestoday.find('table',
                                                {"class": "table table-bordered table-striped"}).tbody.find_all('td')
            buynows_statistics_all = []
            for html_buynows1 in html_buynows_1:  # 一口价列表的 统计栏目  内容
                buynows_statistics = html_buynows1.text
                buynows_statistics = re.sub('[$]', '', buynows_statistics)
                buynows_statistics = re.sub('[\n]', '', buynows_statistics)
                buynows_statistics_all.append(buynows_statistics)

            html_buynows_4 = soup_yestoday.find('div', {"class": "table-responsive"}).tbody.find_all('tr')
            buynows_oders_all = []
            for html_buynows4 in html_buynows_4:  # 一口价列表的 详细列表数据   内容
                html_buynows = html_buynows4.find_all('td')
                buynows_oders_SKU = html_buynows[0].a['title']
                buynows_oders_SKU = re.sub(r':.*$', "", buynows_oders_SKU)  ############ SKU
                buynows_oders_all.append(buynows_oders_SKU)
                buynows_oders_img = html_buynows[0].img['src']  ######################## 主图
                buynows_oders_all.append(buynows_oders_img)
                buynows_oders_describe = html_buynows[0].a['title']  ################### 描述
                buynows_oders_describe = re.sub(r'^.*:', "", buynows_oders_describe)
                buynows_oders_all.append(buynows_oders_describe)
                for html in html_buynows[1:]:
                    buynows_oders_content = html.text
                    buynows_oders_content = re.sub('[$]', '', buynows_oders_content)
                    buynows_oders_content = re.sub('[\n]', '', buynows_oders_content)
                    buynows_oders_all.append(buynows_oders_content)
                ####### 详细数据栏#######
                identifier_oders = buynows_oders_all[0]
                img_buynows_oders = buynows_oders_all[1]
                describe_oders = buynows_oders_all[2]
                Impressions_oders = buynows_oders_all[3]
                Views_oders = buynows_oders_all[4]
                Orders_oders = buynows_oders_all[5]
                Fees_oders = buynows_oders_all[6]
                CPM_oders = buynows_oders_all[7]
                Cost_per_Order_oders = buynows_oders_all[8]
                buynows_oders_all = []

                # 按照特定时间点保存yestoday数据
                if aa != bb:
                    aaa = str(datetime.datetime.now() - datetime.timedelta(hours=15))[0:13]
                    time_hours_local = datetime.datetime.strptime(aaa + ':00:00', '%Y-%m-%d %H:%M:%S')
                    try:
                        models_top_hatter.buynows_oders.objects.create(
                            USER_ID=USER_ID,
                            store_name=store_name,
                            identifier=identifier_oders,
                            img_buynows=img_buynows_oders,
                            describe=describe_oders,
                            Impressions=Impressions_oders,
                            Views=Views_oders,
                            Orders=Orders_oders,
                            Fees=Fees_oders,
                            CPM=CPM_oders,
                            Cost_per_Order=Cost_per_Order_oders,
                            time_local=(datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                                days=1)).date(),
                            time_hours_local=time_hours_local,
                            time_hours_local_symbol='yestoday'
                        ).save()
                        # print(store_name + ' 3小时_一口价')
                    except Exception as e:
                        print(e)
                        print('昨天_一口价 save faile')
            ####### 统计栏########
            Impressions_statistics = buynows_statistics_all[0]
            Views_statistics = buynows_statistics_all[1]
            Orders_statistics = buynows_statistics_all[2]
            Fees_statistics = buynows_statistics_all[3]
            CPM_statistics = buynows_statistics_all[4]
            Cost_per_Order_statistics = buynows_statistics_all[5]
            buynows_statistics_all = []

            # 按照特定时间点保存yestoday数据
            if aa != bb:
                aaa = str(datetime.datetime.now() - datetime.timedelta(hours=15))[0:13]
                time_hours_local = datetime.datetime.strptime(aaa + ':00:00', '%Y-%m-%d %H:%M:%S')
                try:
                    models_top_hatter.buynows_statistics.objects.create(
                        USER_ID=USER_ID,
                        store_name=store_name,
                        Impressions=Impressions_statistics,
                        Views=Views_statistics,
                        Orders=Orders_statistics,
                        Fees=Fees_statistics,
                        CPM=CPM_statistics,
                        Cost_per_Order=Cost_per_Order_statistics,
                        time_local=(datetime.datetime.now() - datetime.timedelta(hours=15) - datetime.timedelta(
                            days=1)).date(),
                        time_hours_local=time_hours_local,
                        time_hours_local_symbol='yestoday'
                    ).save()
                    # print(store_name + ' 3小时_一口价')
                except Exception as e:
                    print(e)
                    print('昨天_一口价 save faile')
        except Exception as e:
            print(str(e) + '：无Yestoday数据')
        ######################### 保存home页 GOTO 提醒数据  ###############################
        try:
            html_home_GOTOS_names = soup_home_GOTO.find_all('div', {"class": "top10"})
            html_home_GOTOS_datas = soup_home_GOTO.find_all('h1', {"class": "my-0"})
            GOTOS_names = []
            GOTOS_datas = []
            for html_home_GOTOS_name in html_home_GOTOS_names:
                a = re.sub('\n', '', html_home_GOTOS_name.get_text())
                GOTOS_names.append(a)
            for html_home_GOTOS_data in html_home_GOTOS_datas:
                b = re.sub('\n', '', html_home_GOTOS_data.get_text())
                GOTOS_datas.append(b)
            models_top_hatter.TODO.objects.filter(USER_ID=USER_ID).filter(store_name=store_name).delete()
            models_top_hatter.TODO.objects.create(
                USER_ID=USER_ID,
                store_name=store_name,
                name=str(GOTOS_names),
                data=str(GOTOS_datas)
            ).save()
            print('保存home数据成功')
        except Exception as e:
            print(str(e) + '：无home数据')
    print('******一口价数据获取完成******')


# 议价商品接收或拒绝（页面刷新数据）
def Refresh_bargaining_data(store_name):
    # 店铺A
    cookie = ''
    ip_port = ''
    try:
        cookie = models_top_hatter.APIAccessToken.objects.filter(USER_ID=1).filter(store_name=store_name).values_list(
            'store_cookie')[0][0]
        ip_port = models_top_hatter.APIAccessToken.objects.filter(USER_ID=1).filter(store_name=store_name).values_list(
            'IP_address')[0][0]
    except Exception as e:
        print(e)

    try:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'HOST': 'cn.tophatter.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        ######################################## IP地址数据 ########################
        # s = requests.session()
        # s.proxies.update(proxy)
        # res = s.get('http://myip.ipip.net/')
        # soup = BeautifulSoup(res.text, 'html.parser').text[:-1]
        # print(soup)
        # time.sleep(2)  # 延时2秒，避免请求过于频繁。
        ######################################## upcoming ###############################
        s = requests.session()
        s.headers.update(headers)
        proxy = {
            'https': 'socks5://' + ip_port,  # 139.159.191.92:1081(A)
            'http': 'socks5://' + ip_port,  # 139.159.191.92:1081(A)
        }
        s.proxies.update(proxy)
        res = s.get(
            'https://cn.tophatter.com/seller/name_your_price_offers?counter=uncountered&filter=all&page=1&per_page=25&sort=date_desc&status=all',
            timeout=60)
        if res.status_code != 200:
            print('cookie过期，请更新！')
            input("输入回车键结束")
        else:
            print(store_name + '-(cookie,IP)正常！')
        soup = BeautifulSoup(res.text, 'html.parser')
        name_your_price_offers = soup.find('table', {"class": "table"}).tbody.find_all('tr', recursive=False)
        authenticity_token = soup.find('meta', {"name": "csrf-token"})['content']
        for name_your_price_offer in name_your_price_offers:
            try:
                actions_status = name_your_price_offer.find('div', {"class": "text-muted text-small top5"}).text
                if actions_status:
                    actions_status_work = actions_status[13:21]
                    if actions_status_work == 'accepted':
                        # actions_ID = name_your_price_offer.find('input').get('name')
                        actions_herf = 'https://cn.tophatter.com' + name_your_price_offer.find('a', {
                            "class": "btn btn-sm btn-success"}).get('href')
                        params = {'authenticity_token': authenticity_token}
                        res = s.post(actions_herf, params)
                        if res.status_code == 200:
                            print(store_name + '-接收正常—accepted')
                        else:
                            print(store_name + '-接收失败—accepted！')
                    # elif actions_status_work == 'rejected':
                    #     # actions_ID = name_your_price_offer.find('input').get('name')
                    #     actions_herf = 'https://cn.tophatter.com' + name_your_price_offer.find('a', {"class": "btn btn-sm btn-danger"}).get('href')
                    #     params = {'authenticity_token': authenticity_token}
                    #     res = s.post(actions_herf, params)
                    #     if res.status_code == 200:
                    #         print(store_name+'-接收正常—rejected')
                    #     else:
                    #         print(store_name+'-接收失败—rejected！')
            except Exception as e:
                a = e
    except Exception as e:
        print(e)


# 获取5miles,资金数据（页面抓取）
def GET_funds_data_5miles():
    for i in models_five_miles.APIAccessToken_5miles.objects.values_list('id', flat=True):
        store_name = models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('store_name')[0][0]
        store_cookie = models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('store_cookie')[0][0]
        USER_ID = models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('USER_ID')[0][0]
        可提现 = ''
        待确认 = ''
        提现中 = ''
        try:
            cookie = store_cookie
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': cookie,
                'Host': 'b.5milesapp.com',
                'Referer': 'https://b.5milesapp.com/payment/balance',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            }
            time.sleep(2)  # 延时2秒，避免请求过于频繁。
            ######################################## upcoming ###############################
            s = requests.session()
            s.headers.update(headers)
            res = s.get('https://b.5milesapp.com/payment/balance', timeout=60)
            if res.status_code != 200:
                print('cookie过期，请更新！')
                input("输入回车键结束")
            else:
                print('cookie正常！')
            soup = BeautifulSoup(res.text, 'html.parser')
            csrf_token_0 = soup.find('table', {"class": "order-info-table"}).text
            # print(csrf_token_0)
            可提现 = re.search(r'(?<=[现]).*?(?=[待确认])', csrf_token_0).group(0)
            可提现 = re.sub('[,]', '', 可提现)
            可提现 = re.sub('[ ]', '', 可提现)
            可提现 = re.sub('[$]', '', 可提现)

            待确认 = re.search(r'(?<=[认]).*?(?=[提现中])', csrf_token_0).group(0)
            待确认 = re.sub('[,]', '', 待确认)
            待确认 = re.sub('[ ]', '', 待确认)
            待确认 = re.sub('[$]', '', 待确认)

            提现中 = re.search(r'[^提现中]+$', csrf_token_0).group(0)
            提现中 = re.sub('[,]', '', 提现中)
            提现中 = re.sub('[ ]', '', 提现中)
            提现中 = re.sub('[$]', '', 提现中)
        except Exception as e:
            print(e)

        ########################## 保存店铺资金数据 #############################
        try:
            ind = models_five_miles.funds_5miles_date.objects.filter(USER_ID=USER_ID).filter(店铺名=store_name).filter(
                Time_Date=(datetime.datetime.now() - datetime.timedelta(hours=15)).date()).values()
            if ind:
                models_five_miles.funds_5miles_date.objects.filter(USER_ID=USER_ID).filter(店铺名=store_name).filter(
                    Time_Date=(datetime.datetime.now() - datetime.timedelta(hours=15)).date()). \
                    update(可提现=可提现, 待确认=待确认, 提现中=提现中, save_time=datetime.datetime.now())
                print('替换成功' + store_name)
            else:
                twz = models_five_miles.funds_5miles_date.objects.create(可提现=可提现, 待确认=待确认, 提现中=提现中,
                                                                         USER_ID=USER_ID,
                                                                         店铺名=store_name,
                                                                         Time_Date=(
                                                                                 datetime.datetime.now() - datetime.timedelta(
                                                                             hours=15)).date())
                twz.save()
                print('保存成功' + store_name)
        except Exception as e:
            print(e)
            print('保存店铺资金数据数据失败，店铺：' + store_name)


def get_5miles_founds_data():
    print('正在获取5miles资金数据、请稍后……')
    GET_funds_data_5miles()
    print('******5miles资金数据获取完成******')


# 获取后台5miles订单数据(订单数据1小时一次)
def get_5miles_orders_date():
    # 1 获取到数据
    for PAGE in range(1, 51):
        DAYS = 1 * (PAGE - 1)
        created_at_start = (datetime.datetime.now() - datetime.timedelta(days=(DAYS + 5))).date().strftime('%Y-%m-%d')
        created_at_end = (datetime.datetime.now() - datetime.timedelta(days=DAYS - 1)).date().strftime('%Y-%m-%d')

        for i in models_five_miles.APIAccessToken_5miles.objects.values_list('id', flat=True):
            try:
                store_name = models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('store_name')[0][
                    0]
                store_APIToken = \
                    models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('store_APIToken')[0][0]
                USER_ID = models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('USER_ID')[0][0]
                headers = {'X-Api-Key': store_APIToken}
                subm = requests.get(
                    'https://hibiscus.5miles.com/api/v2/orders.json?offset=0&limit=100&state=&created_at_start=' + created_at_start + '&created_at_end=' + created_at_end,
                    headers=headers, timeout=50)
                print("status code:", subm.status_code)
                aa = subm.text
                reponse_dicts = json.loads(aa)
                reponse_dicts = reponse_dicts['result']['objects']

                # 2 保存到数据库
                try:
                    for reponse_dict in reponse_dicts:
                        order_id = reponse_dict['id']  # 订单id
                        seq_no = reponse_dict.get('seq_no')  # 订单编号
                        state = reponse_dict.get('state')  # 订单状态
                        shipping_fee = reponse_dict.get('shipping_fee')  # 运费金额
                        amount = reponse_dict.get('amount')  # 成交金额
                        total_amount = reponse_dict.get('total_amount')  # 总金额
                        created_at = reponse_dict.get('created_at')  # 订单付款时间
                        try:
                            paid_at = reponse_dict.get('paid_at')  # 订单付款时间
                        except:
                            paid_at = None
                        buyer_name = reponse_dict.get('buyer_name')  # 买家名称
                        item_lines = reponse_dict.get('item_lines')  # 订单信息
                        shipping_address = reponse_dict.get('shipping_address')  # 发货地址
                        ship_list = reponse_dict.get('ship_list')  # 物流信息
                        try:
                            approved_at = reponse_dict.get('approved_at')  # 订单付款时间
                        except:
                            approved_at_data = None

                        dateArray1 = time.localtime(float(created_at) / 1000)
                        created_at_data = time.strftime("%Y-%m-%d", dateArray1)

                        try:
                            dateArray2 = time.localtime(float(paid_at) / 1000)
                            paid_at_data = time.strftime("%Y-%m-%d", dateArray2)
                        except:
                            paid_at_data = None
                        try:
                            dateArray2 = time.localtime(float(approved_at) / 1000)
                            approved_at_data = time.strftime("%Y-%m-%d", dateArray2)
                        except:
                            approved_at_data = None

                        try:
                            sku_no = item_lines[0]['sku_no']
                        except:
                            sku_no = None

                        try:
                            goods_name = item_lines[0]['goods_name']
                        except:
                            goods_name = None
                        try:
                            goods_main_image_url = item_lines[0]['goods_main_image_url']
                        except:
                            goods_main_image_url = None
                        try:
                            tracking_no = ship_list[0]['tracking_no']
                        except:
                            tracking_no = None

                        status_Approved = None
                        status_Dispatched = None
                        status_Completed = None
                        status_Refunded = None
                        status_Canceled = None
                        status_Closed = None
                        if state == 'Approved':
                            status_Approved = state + str(seq_no)
                        elif state == 'Dispatched':
                            status_Dispatched = state + str(seq_no)
                        elif state == 'Completed':
                            status_Completed = state + str(seq_no)
                        elif state == 'Refunded':
                            status_Refunded = state + str(seq_no)
                        elif state == 'Canceled':
                            status_Canceled = state + str(seq_no)
                        elif state == 'Closed':
                            status_Closed = state + str(seq_no)

                        try:
                            country = shipping_address['country_code']
                        except:
                            country = None

                        SKU_price = 0
                        SKU_freight = 0
                        try:
                            a = max(models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(
                                STAR_DATE__lte=created_at_data).values_list('STAR_DATE'))[0]
                        except:
                            a = min(models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).values_list(
                                'STAR_DATE'))[0]
                        try:
                            obj1 = models_top_hatter.logistics_statistic.objects.filter(USER_ID=USER_ID).filter(
                                STAR_DATE=a).values()  # 物流规则数据（匹配下单时间的物流规则）
                            if country == 'GBR':
                                普货每克 = float(obj1[0]['英国_每克_普货']) * float(obj1[0]['英国_折扣_普货'])
                                普货挂号 = float(obj1[0]['英国_挂号_普货']) * float(obj1[0]['英国_折扣_普货'])
                                带电每克 = float(obj1[0]['英国_每克_带电']) * float(obj1[0]['英国_折扣_带电'])
                                带电挂号 = float(obj1[0]['英国_挂号_带电']) * float(obj1[0]['英国_折扣_带电'])
                                特货每克 = float(obj1[0]['英国_每克_特货']) * float(obj1[0]['英国_折扣_特货'])
                                特货挂号 = float(obj1[0]['英国_挂号_特货']) * float(obj1[0]['英国_折扣_特货'])
                            elif country == 'CAN':
                                普货每克 = float(obj1[0]['加拿_每克_普货']) * float(obj1[0]['加拿_折扣_普货'])
                                普货挂号 = float(obj1[0]['加拿_挂号_普货']) * float(obj1[0]['加拿_折扣_普货'])
                                带电每克 = float(obj1[0]['加拿_每克_带电']) * float(obj1[0]['加拿_折扣_带电'])
                                带电挂号 = float(obj1[0]['加拿_挂号_带电']) * float(obj1[0]['加拿_折扣_带电'])
                                特货每克 = float(obj1[0]['加拿_每克_特货']) * float(obj1[0]['加拿_折扣_特货'])
                                特货挂号 = float(obj1[0]['加拿_挂号_特货']) * float(obj1[0]['加拿_折扣_特货'])
                            elif country == 'AUS':
                                普货每克 = float(obj1[0]['澳大_每克_普货']) * float(obj1[0]['澳大_折扣_普货'])
                                普货挂号 = float(obj1[0]['澳大_挂号_普货']) * float(obj1[0]['澳大_折扣_普货'])
                                带电每克 = float(obj1[0]['澳大_每克_带电']) * float(obj1[0]['澳大_折扣_带电'])
                                带电挂号 = float(obj1[0]['澳大_挂号_带电']) * float(obj1[0]['澳大_折扣_带电'])
                                特货每克 = float(obj1[0]['澳大_每克_特货']) * float(obj1[0]['澳大_折扣_特货'])
                                特货挂号 = float(obj1[0]['澳大_挂号_特货']) * float(obj1[0]['澳大_折扣_特货'])
                            else:
                                普货每克 = float(obj1[0]['美国_每克_普货']) * float(obj1[0]['美国_折扣_普货'])
                                普货挂号 = float(obj1[0]['美国_挂号_普货']) * float(obj1[0]['美国_折扣_普货'])
                                带电每克 = float(obj1[0]['美国_每克_带电']) * float(obj1[0]['美国_折扣_带电'])
                                带电挂号 = float(obj1[0]['美国_挂号_带电']) * float(obj1[0]['美国_折扣_带电'])
                                特货每克 = float(obj1[0]['美国_每克_特货']) * float(obj1[0]['美国_折扣_特货'])
                                特货挂号 = float(obj1[0]['美国_挂号_特货']) * float(obj1[0]['美国_折扣_特货'])

                            obj2 = models_top_hatter.Price_Freight.objects.filter(USER_ID=USER_ID).filter(
                                identifier=sku_no).values()  # 商品基本参数

                            if obj2[0]['SKU_price']:
                                price = obj2[0]['SKU_price']
                            else:
                                price = '0'

                            if obj2[0]['SKU_freight']:
                                freight = obj2[0]['SKU_freight']
                            else:
                                freight = '0'

                            if obj2[0]['SKU_weight']:
                                weight = obj2[0]['SKU_weight']
                            else:
                                weight = '0'

                            if obj2[0]['SKU_variety'] == '普货':
                                SKU_freight = (float(weight) * 普货每克) + 普货挂号
                            elif obj2[0]['SKU_variety'] == '带电':
                                SKU_freight = (float(weight) * 带电每克) + 带电挂号
                            elif obj2[0]['SKU_variety'] == '特货':
                                SKU_freight = (float(weight) * 特货每克) + 特货挂号
                            else:
                                SKU_freight = float(freight)

                            SKU_price = round(float(price), 2)
                            SKU_freight = round(SKU_freight, 2)
                        except Exception as e:
                            print('此商品无价格信息')

                        idenx = models_five_miles.orders_date_5miles.objects.filter(USER_ID=USER_ID).filter(
                            seq_no=seq_no)
                        if idenx:
                            try:
                                models_five_miles.orders_date_5miles.objects.filter(USER_ID=USER_ID).filter(
                                    seq_no=seq_no) \
                                    .update(store_name=store_name,
                                            order_id=order_id,
                                            seq_no=seq_no,
                                            state=state,
                                            shipping_fee=shipping_fee,
                                            amount=amount,
                                            total_amount=total_amount,
                                            created_at=created_at,
                                            paid_at=paid_at,
                                            buyer_name=buyer_name,
                                            approved_at=approved_at,

                                            item_lines=item_lines,
                                            shipping_address=shipping_address,
                                            ship_list=ship_list,

                                            created_at_data=created_at_data,
                                            paid_at_data=paid_at_data,
                                            approved_at_data=approved_at_data,

                                            sku_no=sku_no,
                                            goods_name=goods_name,
                                            goods_main_image_url=goods_main_image_url,
                                            tracking_no=tracking_no,
                                            country=country,

                                            status_Approved=status_Approved,
                                            status_Dispatched=status_Dispatched,
                                            status_Completed=status_Completed,
                                            status_Refunded=status_Refunded,
                                            status_Canceled=status_Canceled,
                                            status_Closed=status_Closed,

                                            SKU_price=SKU_price,
                                            SKU_freight=SKU_freight,
                                            )
                                print(str(PAGE) + store_name + '订单数据替换(1) success')
                            except Exception as e:
                                print(e)
                                print('替换 storedata faile')
                        else:
                            try:
                                twz = models_five_miles.orders_date_5miles.objects.create(
                                    USER_ID=USER_ID,
                                    store_name=store_name,
                                    order_id=order_id,
                                    seq_no=seq_no,
                                    state=state,
                                    shipping_fee=shipping_fee,
                                    amount=amount,
                                    total_amount=total_amount,
                                    created_at=created_at,
                                    paid_at=paid_at,
                                    buyer_name=buyer_name,
                                    approved_at=approved_at,

                                    item_lines=item_lines,
                                    shipping_address=shipping_address,
                                    ship_list=ship_list,

                                    created_at_data=created_at_data,
                                    paid_at_data=paid_at_data,
                                    approved_at_data=approved_at_data,

                                    sku_no=sku_no,
                                    goods_name=goods_name,
                                    goods_main_image_url=goods_main_image_url,
                                    tracking_no=tracking_no,
                                    country=country,

                                    status_Approved=status_Approved,
                                    status_Dispatched=status_Dispatched,
                                    status_Completed=status_Completed,
                                    status_Refunded=status_Refunded,
                                    status_Canceled=status_Canceled,
                                    status_Closed=status_Closed,

                                    SKU_price=SKU_price,
                                    SKU_freight=SKU_freight,
                                )
                                twz.save()
                                print(PAGE + store_name + '订单数据保存(1)-5M success')
                                # print(PAGE)
                            except Exception as e:
                                print(e)
                                print('保存 5M-storedata faile')
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
                print('not this 5M-storedata 数据')


# 获取后台5miles商品数据(商品数据4小时一次)
def get_5miles_pruducts_data():
    # 1 获取到数据
    for PAGE in range(1, 60):
        star_page = str(100 * (PAGE - 1))
        for i in models_five_miles.APIAccessToken_5miles.objects.values_list('id', flat=True):
            try:
                store_name = models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('store_name')[0][
                    0]
                store_APIToken = \
                    models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('store_APIToken')[0][0]
                USER_ID = models_five_miles.APIAccessToken_5miles.objects.filter(id=i).values_list('USER_ID')[0][0]

                headers = {'X-Api-Key': store_APIToken}
                subm = requests.get(
                    'https://hibiscus.5miles.com/api/v1/products/list.json?offset=' + star_page + '&limit=100',
                    headers=headers, timeout=50)
                print("status code:", subm.status_code)
                aa = subm.text
                reponse_dicts = json.loads(aa)
                reponse_dicts = reponse_dicts['result']['objects']

                # 2 保存到数据库
                try:
                    for reponse_dict in reponse_dicts:
                        products_id = int(reponse_dict['id'])  # 商品ID')
                        goods_no = reponse_dict['goods_no']  # 商品编号')
                        cat_id = reponse_dict['cat_id']  # 标题')
                        cat_name = reponse_dict['cat_name']  # 标题')
                        original_sale_price = reponse_dict['original_sale_price']  # 标题')
                        start_price = reponse_dict['start_price']  # 标题')
                        purchase_price = reponse_dict['purchase_price']  # 标题')
                        reserve_price = reponse_dict['reserve_price']  # 标题')
                        shipping_fee = reponse_dict['shipping_fee']  # 标题')
                        cost_price = str(reponse_dict['cost_price'])  # 标题')
                        name = reponse_dict['name']  # 标题')

                        description = reponse_dict['description']  # 描述')
                        main_image_url = reponse_dict['main_image_url']  # 主图')
                        weight = reponse_dict['weight']  # 重量')
                        min_delivery_days = str(reponse_dict['min_delivery_days'])  # 最小处理日期')
                        max_delivery_days = str(reponse_dict['max_delivery_days'])  # 最大处理日期')
                        delivery_address = reponse_dict['delivery_address']  # 发货地址')

                        image_set = reponse_dict['image_set']  # 图片详情')
                        sku_set = reponse_dict['sku_set']  # 变种详情')
                        detail_image_set = reponse_dict['detail_image_set']  # 图片描述详情')

                        # print(store_name)
                        # print(order_id)
                        # print(seq_no)
                        # print(state)
                        # print(shipping_fee)
                        # print(amount)
                        # print(total_amount)
                        # print(created_at)
                        # print(paid_at)
                        # print(buyer_name)
                        # print(approved_at)

                        idenx = models_five_miles.Products_5miles.objects.filter(USER_ID=USER_ID).filter(
                            goods_no=goods_no)
                        if idenx:
                            try:
                                models_five_miles.Products_5miles.objects.filter(USER_ID=USER_ID).filter(
                                    goods_no=goods_no) \
                                    .update(store_name=store_name,
                                            products_id=products_id,
                                            cat_id=cat_id,
                                            cat_name=cat_name,
                                            original_sale_price=original_sale_price,
                                            start_price=start_price,
                                            purchase_price=purchase_price,
                                            reserve_price=reserve_price,
                                            shipping_fee=shipping_fee,
                                            cost_price=cost_price,
                                            name=name,

                                            description=description,
                                            main_image_url=main_image_url,
                                            weight=weight,
                                            min_delivery_days=min_delivery_days,
                                            max_delivery_days=max_delivery_days,
                                            delivery_address=delivery_address,

                                            image_set=image_set,
                                            sku_set=sku_set,
                                            detail_image_set=detail_image_set,
                                            )
                                print(str(PAGE) + store_name + '商品数据-5M-success')
                            except Exception as e:
                                print(e)
                                print('替换 商品数据 faile')
                        else:
                            try:
                                twz = models_five_miles.Products_5miles.objects.create(
                                    USER_ID=USER_ID,
                                    store_name=store_name,
                                    products_id=products_id,
                                    cat_id=cat_id,
                                    goods_no=goods_no,
                                    cat_name=cat_name,
                                    original_sale_price=original_sale_price,
                                    start_price=start_price,
                                    purchase_price=purchase_price,
                                    reserve_price=reserve_price,
                                    shipping_fee=shipping_fee,
                                    cost_price=cost_price,
                                    name=name,

                                    description=description,
                                    main_image_url=main_image_url,
                                    weight=weight,
                                    min_delivery_days=min_delivery_days,
                                    max_delivery_days=max_delivery_days,
                                    delivery_address=delivery_address,

                                    image_set=image_set,
                                    sku_set=sku_set,
                                    detail_image_set=detail_image_set,
                                )
                                twz.save()
                                print(str(PAGE) + store_name + '商品数据-5M success')
                                # print(PAGE)
                            except Exception as e:
                                print(e)
                                print('保存 5M-商品数据 faile')
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
                print('not this 5M-商品数据 数据')


global start_num1, start_num1_2, start_num1_3, start_num1_4, start_num1_5, start_num1_6, start_num1_7, start_num1_8, start_num1_9, max_time  # 在使用前初次声明
start_num1 = 227143463
start_num1_1 = start_num1 + 1
start_num1_2 = start_num1 + 3
start_num1_3 = start_num1 + 5
start_num1_4 = start_num1 + 7
start_num1_5 = start_num1 + 9
start_num1_6 = start_num1 + 11
start_num1_7 = start_num1 + 13
start_num1_8 = start_num1 + 15
start_num1_9 = start_num1 + 17

sched = BackgroundScheduler()


# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='03', second='50')
# def my_task00():
#     global proxys,max_time
#     # aaa = str(datetime.datetime.now() - datetime.timedelta(days=15))[0:13]
#     # time_hours_local = datetime.datetime.strptime(aaa + ':00:00', '%Y-%m-%d %H:%M:%S')
#     # models.TopData.objects.filter(activated_at__lte=time_hours_local).delete()
#     # models.TopData.objects.filter(save_time__lte=time_hours_local).delete()
#     # max_time = max(models.TopData.objects.filter(~Q(activated_at=None)).values_list('activated_at'))[0]
#     if  proxys == []:
#         all_ip()
#         print(proxys)
# @sched.scheduled_job('cron', day_of_week='*', hour='17', minute='32', second='20')
def my_task01():
    global start_num1_1, proxies, max_time  # 在使用前初次声明
    a = 0
    while 1:
        time.sleep(2)
        now = datetime.datetime.now() - datetime.timedelta(hours=19)
        # status_code = myfunc1(start_num1_1, proxies[0])
        status_code = myfunc1(start_num1_1)
        if a > 5 or status_code is not False:
            try:
                status_code = datetime.datetime.strptime(status_code, '%Y-%m-%dT%H:%M:%S')
                if status_code > now and status_code is not None:
                    time.sleep(3000)
                    start_num1_1 = start_num1_1
                else:
                    start_num1_1 += 18
                    a = 0
            except Exception as e:
                print(e)
                start_num1_1 += 18
                a = 0
        else:
            start_num1_1 = start_num1_1
            a = a + 1
        print(start_num1_1, status_code)
# my_task01()

# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task02():
#     global start_num1_2,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_2, proxys[1])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_2  = start_num1_2
#                 else:
#                     start_num1_2 += 18
#                     A=0
#             except:
#                 start_num1_2 += 18
#                 A = 0
#         else :
#             start_num1_2  = start_num1_2
#             A = A+1
#         print(start_num1_2, status_code)
# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task03():
#     global start_num1_3,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_3, proxys[2])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_3  = start_num1_3
#                 else:
#                     start_num1_3 += 18
#                     A=0
#             except:
#                 start_num1_3 += 18
#                 A = 0
#         else :
#             start_num1_3  = start_num1_3
#             A = A+1
#         print(start_num1_3, status_code)
# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task04():
#     global start_num1_4,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_4, proxys[3])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_4  = start_num1_4
#                 else:
#                     start_num1_4 += 18
#                     A=0
#             except:
#                 start_num1_4 += 18
#                 A = 0
#         else :
#             start_num1_4  = start_num1_4
#             A = A+1
#         print(start_num1_4, status_code)
# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task05():
#     global start_num1_5,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_5, proxys[4])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_5  = start_num1_5
#                 else:
#                     start_num1_5 += 18
#                     A=0
#             except:
#                 start_num1_5 += 18
#                 A = 0
#         else :
#             start_num1_5  = start_num1_5
#             A = A+1
#         print(start_num1_5,status_code)
# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task06():
#     global start_num1_6,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_6, proxys[5])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_6  = start_num1_6
#                 else:
#                     start_num1_6 += 18
#                     A=0
#             except:
#                 start_num1_6 += 18
#                 A = 0
#         else :
#             start_num1_6  = start_num1_6
#             A = A+1
#         print(start_num1_6, status_code)
# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task07():
#     global start_num1_7,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_7, proxys[6])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_7  = start_num1_7
#                 else:
#                     start_num1_7 += 18
#                     A=0
#             except:
#                 start_num1_7 += 18
#                 A = 0
#         else :
#             start_num1_7  = start_num1_7
#             A = A+1
#         print(start_num1_7, status_code)
# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task08():
#     global start_num1_8,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_8, proxys[7])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_8  = start_num1_8
#                 else:
#                     start_num1_8 += 18
#                     A=0
#             except:
#                 start_num1_8 += 18
#                 A = 0
#         else :
#             start_num1_8  = start_num1_8
#             A = A+1
#         print(start_num1_8, status_code)
# @sched.scheduled_job('cron', day_of_week='*', hour='16', minute='04', second='50')
# def my_task09():
#     global start_num1_9,proxys,max_time  # 在使用前初次声明
#     A = 0
#     while 1:
#         sleep(2)
#         now = datetime.datetime.now() - datetime.timedelta(hours=19)
#         status_code = myfunc1(start_num1_9, proxys[8])
#         if A>5 or status_code != False:
#             try:
#                 status_code = datetime.datetime.strptime(status_code,'%Y-%m-%dT%H:%M:%S')
#                 if status_code > now and status_code != None:
#                     sleep(3000)
#                     start_num1_9  = start_num1_9
#                 else:
#                     start_num1_9 += 18
#                     A=0
#             except:
#                 start_num1_9 += 18
#                 A = 0
#         else :
#             start_num1_9  = start_num1_9
#             A = A+1
#         print(start_num1_9,status_code)


# 定时获取(后台订单数据30分钟一次)
# @sched.scheduled_job('cron',minute='*/30',id='my_task1')
# def my_task1():
#     get_store_data_1()
# # 定时获取(后台订单数据35分钟一次)
# @sched.scheduled_job('cron',minute='*/35',id='my_task2')
# def my_task2():
#     get_store_data_2()

# 定时获取(商品数据)
# @sched.scheduled_job('cron',minute='*/30',id='my_task3')
# def my_task3():
#     get_Pruducts()


# 定时统计TOP数据
# @sched.scheduled_job('cron',hour='*/1',id='my_task1')
def my_task1():
    myfunc_colocet()
my_task1()
# #
# # 定时30分钟获取销售数据(销售数据)
# @sched.scheduled_job('cron',minute='*/30',id='my_task2')
# def my_task2():
#     get_performance_data_hours_time()

# # 统计图表数据_全时段数量均价统计
# @sched.scheduled_job('cron',second='*/20',id='my_task2')
# def my_task2():
#     get_sales_amounts()


# # 定时获取页面资金数据
# @sched.scheduled_job('cron',minute='*/08',id='my_task1')
# def my_task1():
#     get_founds_data()
#     get_5miles_founds_data()
#
# # 定时获取页面一口价数据
# @sched.scheduled_job('cron',hour='*/1',id='my_task2')
# def my_task2():
#     get_buynow_data()

# # 定时5miles订单数据
# @sched.scheduled_job('cron',hour='*/1',id='my_task1')
# def my_task1():
#     get_5miles_orders_date()

# # 定时5miles商品数据
# @sched.scheduled_job('cron',hour='*/1',id='my_task2')
# def my_task2():
#     get_5miles_pruducts_data()

# 定时刷新议价数据
# @sched.scheduled_job('cron',minute='*/1',id='my_task1')
# def my_task1():
#     Refresh_bargaining_data('A')
# @sched.scheduled_job('cron', minute='*/1', id='my_task2')
# def my_task2():
#     Refresh_bargaining_data('G')
# @sched.scheduled_job('cron', minute='*/1', id='my_task3')
# def my_task3():
#     Refresh_bargaining_data('I')
# @sched.scheduled_job('cron', minute='*/1', id='my_task4')
# def my_task4():
#     Refresh_bargaining_data('J')
# @sched.scheduled_job('cron', minute='*/1', id='my_task5')
# def my_task5():
#     Refresh_bargaining_data('M')
# @sched.scheduled_job('cron', minute='*/1', id='my_task6')
# def my_task6():
#     Refresh_bargaining_data('P')
# @sched.scheduled_job('cron', minute='*/1', id='my_task7')
# def my_task7():
#     Refresh_bargaining_data('Q')

sched.start()
