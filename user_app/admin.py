
from django.contrib import admin

from user_app.models import User,User_logintime,User_name,User_page_name,VisitNumber,DayNumber

admin.site.register(User)
admin.site.register(User_logintime)
admin.site.register(User_name)
admin.site.register(User_page_name)
admin.site.register(VisitNumber)
admin.site.register(DayNumber)