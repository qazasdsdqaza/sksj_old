from django.conf.urls import url
from . import views

urlpatterns = [
                url(r'^time_line_updata/$', views.time_line_updata, name='time_line_updata'),
                ]
