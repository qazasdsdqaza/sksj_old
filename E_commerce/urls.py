"""E_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^common_functions/', include('common_functions_app.urls', namespace="common_functions_app")),
    url(r'^Tophatter/', include('Tophatter_app.urls', namespace="Tophatter_app")),
    url(r'^five_miles/', include('five_miles_app.urls', namespace="five_miles_app")),
    url(r'^get_date/', include('get_date_app.urls', namespace="get_date_app")),
    url(r'^PruAndLog/', include('PruAndLog.urls', namespace="PruAndLog")),
    url(r'^service/', include('service_app.urls', namespace="service_app")),
    url(r'^', include('user_app.urls', namespace='user_app')),
]
