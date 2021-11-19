from django.conf.urls import url
from . import views

urlpatterns = [
                url(r'^All_orders_profitStatistics/$', views.All_orders_profitStatistics, name='All_orders_profitStatistics'),
                url(r'^Auction_orders_profitStatistics/$', views.Auction_orders_profitStatistics, name='Auction_orders_profitStatistics'),
                url(r'^Buynow_orders_profitStatistics/$', views.Buynow_orders_profitStatistics, name='Buynow_orders_profitStatistics'),
                url(r'^Auction_orders_profitStatistics_now/$', views.Auction_orders_profitStatistics_now, name='Auction_orders_profitStatistics_now'),
                url(r'^Buynow_page_orders/$', views.Buynow_page_orders, name='Buynow_page_orders'),
                url(r'^Refund_orders/$', views.Refund_orders, name='Refund_orders'),
                url(r'^orders_detail/$', views.orders_detail, name='orders_detail'),
                url(r'^orders_to_show/$', views.orders_to_show, name='orders_to_show'),

                url(r'^Top_all_products/$', views.Top_all_products, name='Top_all_products'),
                url(r'^Top_products_update/$', views.Top_products_update, name='Top_products_update'),
                url(r'^TOP_campaign_list/$', views.TOP_campaign_list, name='TOP_campaign_list'),
                url(r'^uploading_csv/$', views.uploading_csv, name='uploading_csv'),

                url(r'^Top_founds/$', views.Top_founds, name='Top_founds'),

                url(r'^TOP_store_msg/$', views.TOP_store_msg, name='TOP_store_msg'),
                url(r'^Top_download/$', views.Top_download, name='Top_download'),



]
