from django.conf.urls import url
from . import views

urlpatterns = [
                url(r'^Products_All_Own/$', views.Products_All_Own, name='Products_All_Own'),
                url(r'^owm_products_update/$', views.owm_products_update, name='owm_products_update'),
                url(r'^warehouse_show/$', views.warehouse_show, name='warehouse_show'),

                url(r'^key_parameter/$', views.key_parameter, name='key_parameter'),
                url(r'^logistics_statistic/$', views.logistics_statistic, name='logistics_statistic'),
                url(r'^exchange_rate_show/$', views.exchange_rate_show, name='exchange_rate_show'),
                ]
