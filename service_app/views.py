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
#更新日志
def time_line_updata(request):
    user_app.change_info(request, 'time_line_updata')
    if not request.session.get('username'):
        return redirect(reverse('user_app:login'))
    USER = models_user_app.User.objects.filter(username=request.session.get('username')).values('USER_ID', 'PRIVILEGE')
    USER_ID = USER[0]['USER_ID']
    PRIVILEGE = USER[0]['PRIVILEGE']
    if int(PRIVILEGE) >5:
        return render(request, '../../user_app/templates/404.html')

    if request.method == "GET" or request.method == "POST":
        return render(request, 'service/time_line_updata.html')

