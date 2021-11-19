from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^information_aggregation/$', views.information_aggregation, name='information_aggregation'),
    url(r'^TOP_statistics/$', views.TOP_statistics, name='TOP_statistics'),
    url(r'^TOP_goodslist/$', views.TOP_goodslist, name='TOP_goodslist'),
    url(r'^TOP_seller/$', views.TOP_seller, name='TOP_seller'),
    url(r'^TOP_show/$', views.TOP_show, name='TOP_show')
]
