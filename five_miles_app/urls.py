from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^FiveMiles_All_orders_profitStatistics/$', views.FiveMiles_All_orders_profitStatistics, name='FiveMiles_All_orders_profitStatistics'),
    url(r'^FiveMiles_all_products/$', views.FiveMiles_all_products, name='FiveMiles_all_products'),
    url(r'^FiveMiles_products_update/$', views.FiveMiles_products_update, name='FiveMiles_products_update'),

    url(r'^FiveMiles_store_msg/$', views.FiveMiles_store_msg, name='FiveMiles_store_msg'),
    url(r'^FiveMiles_founds/$', views.FiveMiles_founds, name='FiveMiles_founds'),
]
