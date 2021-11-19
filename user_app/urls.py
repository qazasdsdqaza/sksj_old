from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^index/user/login/$', views.LoginView.as_view(), name='login'),
    url(r'^index/user/logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^index/user/smscode/$', views.smscode, name='短信验证码'),
    url(r'^index/user/reg/$', views.reg, name='reg'),
    url(r'^index/user/forget/$', views.forget, name='forget'),
    url(r'^index/$', views.index, name='index'),

    url(r'^index/set/user/info/$', views.info, name='info'),
    url(r'^index/set/user/password/$', views.password, name='password'),
]

# www.xxx.com/goodslist
# www.xxx.com/goodslist/1
