from django.db import models
import datetime,time
#用户数据
class User(models.Model):
    USER_ID = models.IntegerField(verbose_name='用户id')
    username = models.CharField(max_length=30, verbose_name='用户名')
    password = models.CharField(max_length=30, verbose_name='登录密码')
    cellphone = models.CharField(max_length=30, verbose_name='注册手机号')
    # 注册完了，后台核对信息，进行审核开通(1:开通  0:未开通)
    checks = models.CharField(max_length=30, verbose_name='审核状态')
    # 注册账号的默认等级是最低等级
    #{等级划分：0：超级管理员，可以进行账号管理，流量监控等。
    #           1：一级用户，具备网站的所有功能
    #           2：具备后台的所有功能，但只开通TOP后台管理
    #           3：只具备整平台数据分析功能，不具备后台管理（开通默认）
    PRIVILEGE = models.CharField(max_length=30, verbose_name='权限等级')


    head_portraits = models.CharField(default='',max_length=300, verbose_name='头像')
    nickname = models.CharField(default='',max_length=30, verbose_name='昵称')
    gender = models.CharField(default='',max_length=10, verbose_name='性别')
    mailbox = models.CharField(default='',max_length=100, verbose_name='邮箱')
    remarks = models.CharField(default='',max_length=500, verbose_name='备注')
    class Meta:
        db_table = 'user_tb'
        verbose_name = '注册用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class User_logintime(models.Model):
    username = models.CharField(null=True, max_length=100, verbose_name='用户名')
    IP = models.CharField(null=True, max_length=100, verbose_name='用户IP')
    login_status = models.CharField(null=True, max_length=100, verbose_name='登录状态')
    save_time = models.DateTimeField(null=True,auto_now_add = True, verbose_name='创建数据时间')
    class Meta:
        verbose_name = '登录统计'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class User_name(models.Model): #访问网站的ip地址和次数
    username=models.CharField(verbose_name='用户名',max_length=30)    #用户名
    count=models.IntegerField(verbose_name='访问次数',default=0) #该用户访问次数
    class Meta:
        verbose_name = '用户访问总次数统计'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class User_page_name(models.Model): #访问网站的不同页面不同时间和次数
    username=models.CharField(verbose_name='用户名',max_length=30)    #用户名
    day = models.DateField(verbose_name='日期') #日期
    page_name = models.CharField(verbose_name='网页名', max_length=300)  # 网页名
    count=models.IntegerField(verbose_name='访问次数',default=0) #该用户访问次数
    last_time = models.DateTimeField(null=True,  verbose_name='最后访问数据时间')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    class Meta:
        verbose_name = '详细访问信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class VisitNumber(models.Model):#网站总访问次数
    count=models.IntegerField(verbose_name='网站访问总次数',default=0) #网站访问总次数
    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.count)

class DayNumber(models.Model):#单日访问量统计
    day=models.DateField(verbose_name='日期')
    count=models.IntegerField(verbose_name='网站访问次数',default=0) #网站访问总次数
    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.day)








