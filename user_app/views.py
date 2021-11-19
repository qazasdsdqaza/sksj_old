import json
import datetime
from json import JSONDecodeError
import time
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View
from user_app import models
from Tophatter_app import models as models_Tophatter_app
from PruAndLog import models as models_PruAndLog
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
import re
import jwt
from E_commerce import settings
global smscode  # 汇率,手机验证码


# 登录
class LoginView(View):
    def post(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取用户真实IP地址
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']

        data = {
            'code': 1,  # 默认登录不成功
            'data': None
        }
        py_dict = json.loads(request.body.decode())
        username = py_dict['username']
        password = py_dict['password']
        user = models.User.objects.filter(username=username)
        if user:
            user = user.filter(password=password).values('checks')
        else:
            data['code'] = 1
            data['message'] = '该账号未注册！'
            # 保存登录信息
            models.User_logintime.objects.create(username=username, IP=str(user_ip), login_status='None').save()
            return JsonResponse(data)
        if user:
            if user[0]['checks'] == '1':
                user_info = models.User.objects.filter(username=username).first()
                format_time = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H-%M-%S')
                time_stamp = int(time.mktime(time.strptime(format_time, '%Y-%m-%d %H-%M-%S')))
                payload = {
                    'exp': time_stamp,
                    'data': {'username': username}
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
                data['code'] = 20000
                data['message'] = '登录成功'
                data['data'] = {
                    'avatar': user_info.head_portraits,
                    'name': user_info.nickname,
                    'token': token
                }
                request.session['username'] = username
                request.session['is_login'] = True
                request.session.set_expiry(0)
                # 保存登录信息
                models.User_logintime.objects.create(username=username, IP=str(user_ip), login_status='Ture').save()
            elif user[0]['checks'] == '0':
                data['code'] = 1
                data['message'] = '账号未审核，请联系管理员审核开通账号。'
                # 保存登录信息
                models.User_logintime.objects.create(username=username, IP=str(user_ip), login_status='None').save()
            else:
                data['code'] = 1
                data['message'] = '登录失败'
                # 保存登录信息
                models.User_logintime.objects.create(username=username, IP=str(user_ip), login_status='None').save()
            return JsonResponse(data)
        else:
            data['code'] = 1
            data['message'] = '密码错误！'
            # 保存登录信息
            models.User_logintime.objects.create(username=username, IP=str(user_ip), login_status='None').save()
        return JsonResponse(data)
    """ 以下注释掉为原代码部分 """
    # def get(self, request):
    #     if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取用户真实IP地址
    #         user_ip = request.META['HTTP_X_FORWARDED_FOR']
    #     else:
    #         user_ip = request.META['REMOTE_ADDR']
    # 
    #     form = forms.LoginForm(request.GET)
    #     data = {
    #         'code': 1,  # 默认登录不成功
    #         'msg': None,
    #         'data': None
    #     }
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = models.User.objects.filter(username=username)
    #         if user:
    #             user = user.filter(password=password).values('checks')
    #         else:
    #             data['code'] = 1
    #             data['msg'] = '该账号未注册！'
    #             models.User_logintime.objects.create(username=username, IP=str(user_ip),
    #                                                  login_status='None').save()  # 保存登录信息
    #             return HttpResponse(json.dumps(data))
    #         if user:
    #             if user[0]['checks'] == '1':
    #                 data['code'] = 0
    #                 data['msg'] = '登录成功'
    #                 request.session['username'] = username
    #                 request.session['is_login'] = True
    #                 request.session.set_expiry(0)
    #                 models.User_logintime.objects.create(username=username, IP=str(user_ip),
    #                                                      login_status='Ture').save()  # 保存登录信息
    #             elif user[0]['checks'] == '0':
    #                 data['code'] = 1
    #                 data['msg'] = '账号未审核，请联系管理员审核开通账号。'
    #                 models.User_logintime.objects.create(username=username, IP=str(user_ip),
    #                                                      login_status='None').save()  # 保存登录信息
    #             else:
    #                 data['code'] = 1
    #                 data['msg'] = '登录失败'
    #                 models.User_logintime.objects.create(username=username, IP=str(user_ip),
    #                                                      login_status='None').save()  # 保存登录信息
    #             return HttpResponse(json.dumps(data))
    #         else:
    #             data['code'] = 1
    #             data['msg'] = '密码错误！'
    #             models.User_logintime.objects.create(username=username, IP=str(user_ip),
    #                                                  login_status='None').save()  # 保存登录信息
    #             return HttpResponse(json.dumps(data))
    # 
    #     return render(request, 'index/user/login.html')


# 退出登录
class LogoutView(View):
    """ 以下注释部分为原代码 """
    # def get(self, request):
    #     if not request.session.get('username'):
    #         return redirect(reverse('user_app:login'))
    #     request.session.flush()
    #     return redirect(reverse('user_app:login'))

    """ 新增代码部分 """

    def post(self, request):
        data = {'code': 20000, 'message': '退出成功', 'data': ''}
        token = request.META.get('HTTP_X_TOKEN')
        if token:
            return JsonResponse(data)
        data['code'] = 400
        data['message'] = '请登录后重试'
        return JsonResponse(data)


# 验证手机号
def smscode(request):
    if request.method == "GET":
        # 发送短信验证码
        data1 = {'code': 1}  # 默认登录不成功
        phone = request.GET.get('phone', '')  # 发送手机号验证码时的手机
        if phone:
            print(phone)

            data1 = {'code': 0}  # 发送成功（添加发送时的验证码到对应的地方）
        return HttpResponse(json.dumps(data1))


# 注册新用户
@csrf_exempt
def reg(request):
    if request.method == "POST":
        """ 原代码部分注释掉 """
        # # 新用户注册，只是提交审核，终审需要后台确认
        # data2 = {'code': 1, 'data': '123456'}  # 默认注册不成功
        # username = request.GET.get('nickname', '')  # 用户名
        # password = request.GET.get('password', '')  # 登录密码
        # cellphone = request.GET.get('cellphone', '')  # 手机号
        # vercode = request.GET.get('vercode', '')  # 手机号验证码
        # checks = 0  # 后台审核(0:待审核 ，1:审核通过)
        # PRIVILEGE = 4  # 权限等级(0-5:权限逐级下降)
        #
        # USER_ID_max = models.User.objects.values('USER_ID').aggregate(Max('USER_ID'))
        # USER_ID_max = USER_ID_max['USER_ID__max']
        #
        # if models.User.objects.filter(username=username).first():
        #     data2 = {'code': 0, 'data': '该用户名已注册'}
        #     return HttpResponse(json.dumps(data2))
        # if models.User.objects.filter(cellphone=cellphone).first():
        #     data2 = {'code': 0, 'data': '该手机号已注册'}
        #     return HttpResponse(json.dumps(data2))
        #
        # print(username, password, cellphone, vercode, )
        # print('注册')
        #
        # # 此处增加短信验证码校验
        #
        # if username and password and cellphone:  # and vercode 暂时屏蔽手机验证码
        #     try:
        #         models.User.objects.create(USER_ID=USER_ID_max + 1,
        #                                    username=username,
        #                                    password=password,
        #                                    cellphone=cellphone,
        #                                    checks=checks,
        #                                    PRIVILEGE=PRIVILEGE).save()
        #         data2 = {'code': 0, 'data': '注册成功，正在跳转登录界面...'}
        #     except Exception as e:
        #         data2 = {'code': 1, 'data': '注册失败：' + str(e)}
        #
        #     return HttpResponse(json.dumps(data2))
        # return render(request, 'index/user/reg.html')

        # 新用户注册，只是提交审核，终审需要后台确认
        """ 以下为新增代码部分 """
        data = {'code': 1, 'message': ''}  # 默认注册不成功
        try:
            py_dict = json.loads(request.body.decode())
        except JSONDecodeError:
            data['message'] = '请填写完所有内容后重试'
            return JsonResponse(data)
        username = py_dict.get('username')  # 用户名
        pwd = py_dict.get('password')  # 密码
        pwd2 = py_dict.get('password2')
        cellphone = py_dict.get('cellphone')  # 手机号
        checks = 0  # 后台审核(0:待审核 ，1:审核通过)
        privilege = 4  # 权限等级(0-5:权限逐级下降)
        user_id_max = models.User.objects.values('USER_ID').aggregate(Max('USER_ID'))['USER_ID__max']
        if not user_id_max:
            user_id_max = 0

        if not username:
            data['message'] = '用户名不能为空'
            return JsonResponse(data)
        if not pwd:
            data['message'] = '密码不能为空'
            return JsonResponse(data)
        if len(pwd) < 6:
            data['message'] = '密码不能低于6位'
            return JsonResponse(data)
        if not pwd2:
            data['message'] = '确认密码不能为空'
            return JsonResponse(data)
        if pwd != pwd2:
            data['message'] = '两次密码不一致'
            return JsonResponse(data)
        if not cellphone:
            data['message'] = '手机号不能为空'
            return JsonResponse(data)
        if not re.match(r'^((1[3,5,8,7,9][0-9])|(14[5,7])|(17[0,6,7,8])|(19[7]))\d{8}$', str(cellphone)):
            data['message'] = '请输入正确格式的手机号'
            return JsonResponse(data)
        if models.User.objects.filter(username=username).first():
            data['message'] = '该用户名已注册'
            return JsonResponse(data)
        if models.User.objects.filter(cellphone=cellphone).first():
            data['message'] = '该手机号已注册'
            return JsonResponse(data)
        models.User.objects.create(USER_ID=user_id_max + 1, username=username,
                                   password=pwd, cellphone=cellphone,
                                   checks=checks, PRIVILEGE=privilege)
        data['code'] = 20000
        data['message'] = '注册成功'
        return JsonResponse(data)
    else:
        return JsonResponse({"code": 405, "message": "请使用POST方式注册"})


# 密码找回
def forget(request):
    if request.method == "GET":
        data = {'code': 1, 'data': '验证不通过'}  # 默认登录不成功
        data1 = {'resetpass': ''}
        cellphone = request.GET.get('cellphone', '')  # 手机号
        vercode = request.GET.get('vercode', '')  # 手机号验证码
        password = request.GET.get('password', '')  # 新密码
        print(cellphone, vercode, password)

        # 此处增加短信验证码校验
        if vercode == '1':
            data = {'code': 0, 'data': '短信验证码错误'}
            return HttpResponse(json.dumps(data))

        if cellphone and password:
            if models.User.objects.filter(cellphone=cellphone).first():
                models.User.objects.filter(cellphone=cellphone).update(password=password)
                data = {'code': 0, 'data': '修改密码成功，正在跳转登录界面...'}
                return HttpResponse(json.dumps(data))
            else:
                data = {'code': 0, 'data': '该手机号未注册'}
                return HttpResponse(json.dumps(data))
    return render(request, 'index/user/forget.html')


# 各项信息设置
# 基本资料
@csrf_exempt
def info(request):
    if request.method == "GET" or request.method == "POST":
        if not request.session.get('username'):
            return redirect(reverse('user_app:login'))
        username = request.session.get('username')
        if request.method == "POST":
            myfile = request.FILES['file']
            fs = FileSystemStorage(location='/shengkongshuju/')
            filename = fs.save('./static/user_files_directory/head_portraits/' + myfile.name, myfile)
            if myfile:
                try:
                    head_portraits_url = 'http://sksj.shop/' + filename[2:]
                    models.User.objects.filter(username=username).update(head_portraits=head_portraits_url)
                    data = {'status': 0, 'url': head_portraits_url}
                    return HttpResponse(json.dumps(data))
                except Exception as e:
                    data = {'status': 1, 'msg': '上传失败:' + str(e)}
                    return HttpResponse(json.dumps(data))

        username_re = request.GET.get('username', '')  # 用户名
        cellphone_re = request.GET.get('cellphone', '')  # 手机
        nickname_re = request.GET.get('nickname', '')  # 昵称
        gender_re = request.GET.get('sex', '')  # 性别
        email_re = request.GET.get('email', '')  # 邮箱
        remarks_re = request.GET.get('remarks', '')  # 备注
        if username_re and cellphone_re:
            try:
                models.User.objects.filter(username=username_re).update(
                    nickname=nickname_re,
                    gender=gender_re,
                    mailbox=email_re,
                    remarks=remarks_re)
                data1 = {'code': 0, 'data': '更新成功'}
                return HttpResponse(json.dumps(data1))
            except Exception as e:
                data1 = {'code': 0, 'data': '更新失败：' + str(e)}
                return HttpResponse(json.dumps(data1))

        objs = models.User.objects.filter(username=username).values()
        context = {'我的角色': objs[0]['PRIVILEGE'],
                   '用户名': objs[0]['username'],
                   '昵称': objs[0]['nickname'],
                   '性别': objs[0]['gender'],
                   '头像': objs[0]['head_portraits'],
                   '手机': objs[0]['cellphone'],
                   '邮箱': objs[0]['mailbox'],
                   '备注': objs[0]['remarks'],
                   }
        return render(request, 'index/set/user/info.html', context)


# 修改密码
def password(request):
    if request.method == "GET":
        if not request.session.get('username'):
            return redirect(reverse('user_app:login'))

        username = request.session.get('username')
        oldPassword = request.GET.get('oldPassword', '')  # 旧密码
        repassword = request.GET.get('repassword', '')  # 新密码
        if oldPassword and repassword:
            OLDPASSWORD = models.User.objects.filter(username=username).values('password')
            print(OLDPASSWORD[0]['password'], oldPassword)
            try:
                if OLDPASSWORD[0]['password'] == oldPassword:
                    models.User.objects.filter(username=username).update(password=repassword)
                    data = {'code': 0, 'data': '更新密码成功'}
                    return HttpResponse(json.dumps(data))
                else:
                    data = {'code': 0, 'data': '原始密码填写错误'}
                    return HttpResponse(json.dumps(data))
            except Exception as e:
                data = {'code': 0, 'data': '系统错误:' + str(e)}
                return HttpResponse(json.dumps(data))

        return render(request, 'index/set/user/password.html')


# 主页
def index(request):
    if request.method == "GET":
        if not request.session.get('username'):
            return redirect(reverse('user_app:login'))
        try:
            exchange_rate = models_PruAndLog.get_exchange_rate.objects.values('exchange_rate').last()['exchange_rate']
        except:
            exchange_rate = 6.3000

        计_产品进价 = request.GET.get('计_产品进价', '')
        计_产品重量 = request.GET.get('计_产品重量', '')
        计_均SFB = request.GET.get('计_均SFB', '')
        计_成交率 = request.GET.get('计_成交率', '')
        计_预估退货率 = request.GET.get('计_预估退货率', '')
        计_当前汇率 = request.GET.get('计_当前汇率', '')
        计_物流商选择 = request.GET.get('计_物流商选择', '')
        计_输入运费 = request.GET.get('计_输入运费', '')
        计_一口价利润 = request.GET.get('计_一口价利润', '')
        计_拍卖利润率 = request.GET.get('计_拍卖利润率', '')
        # print('计_产品进价:'+计_产品进价)
        if 计_产品进价 != '':
            change_info(request, '计算器')
            拍卖总成本 = 0
            拍卖保底价 = 0
            一口价总成本 = 0
            建议一口价 = 0
            拍卖利润 = 0
            一口价利润 = 0
            a = max(models_Tophatter_app.logistics_statistic.objects.values_list('STAR_DATE'))[0]
            Its = models_Tophatter_app.logistics_statistic.objects.filter(STAR_DATE=a).values()  # 物流规则数据（匹配下单时间的物流规则）
            普货每克 = (float(Its[0]['美国_每克_普货']) * float(Its[0]['美国_折扣_普货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_每克_普货']) * float(Its[0]['英国_折扣_普货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_每克_普货']) * float(Its[0]['加拿_折扣_普货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_每克_普货']) * float(Its[0]['澳大_折扣_普货']) * float(Its[0]['澳大_销售比']) / 100)
            普货挂号 = (float(Its[0]['美国_挂号_普货']) * float(Its[0]['美国_折扣_普货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_挂号_普货']) * float(Its[0]['英国_折扣_普货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_挂号_普货']) * float(Its[0]['加拿_折扣_普货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_挂号_普货']) * float(Its[0]['澳大_折扣_普货']) * float(Its[0]['澳大_销售比']) / 100)

            带电每克 = (float(Its[0]['美国_每克_带电']) * float(Its[0]['美国_折扣_带电']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_每克_带电']) * float(Its[0]['英国_折扣_带电']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_每克_带电']) * float(Its[0]['加拿_折扣_带电']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_每克_带电']) * float(Its[0]['澳大_折扣_带电']) * float(Its[0]['澳大_销售比']) / 100)
            带电挂号 = (float(Its[0]['美国_挂号_带电']) * float(Its[0]['美国_折扣_带电']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_挂号_带电']) * float(Its[0]['英国_折扣_带电']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_挂号_带电']) * float(Its[0]['加拿_折扣_带电']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_挂号_带电']) * float(Its[0]['澳大_折扣_带电']) * float(Its[0]['澳大_销售比']) / 100)

            特货每克 = (float(Its[0]['美国_每克_特货']) * float(Its[0]['美国_折扣_特货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_每克_特货']) * float(Its[0]['英国_折扣_特货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_每克_特货']) * float(Its[0]['加拿_折扣_特货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_每克_特货']) * float(Its[0]['澳大_折扣_特货']) * float(Its[0]['澳大_销售比']) / 100)
            特货挂号 = (float(Its[0]['美国_挂号_特货']) * float(Its[0]['美国_折扣_特货']) * float(Its[0]['美国_销售比']) / 100) + \
                   (float(Its[0]['英国_挂号_特货']) * float(Its[0]['英国_折扣_特货']) * float(Its[0]['英国_销售比']) / 100) + \
                   (float(Its[0]['加拿_挂号_特货']) * float(Its[0]['加拿_折扣_特货']) * float(Its[0]['加拿_销售比']) / 100) + \
                   (float(Its[0]['澳大_挂号_特货']) * float(Its[0]['澳大_折扣_特货']) * float(Its[0]['澳大_销售比']) / 100)

            if 计_物流商选择 == '普货':
                if 计_产品重量:
                    运费 = round(((float(计_产品重量) * 普货每克) + 普货挂号), 2)
                else:
                    运费 = 0
            elif 计_物流商选择 == '带电':
                if 计_产品重量:
                    运费 = round(((float(计_产品重量) * 带电每克) + 带电挂号), 2)
                else:
                    运费 = 0
            elif 计_物流商选择 == '特货':
                if 计_产品重量:
                    运费 = round((((计_产品重量) * 特货每克) + 特货挂号), 2)
                else:
                    运费 = 0
            elif 计_物流商选择 == '海运':
                运费 = round(float(计_输入运费), 2)
            else:
                运费 = 0

            if 计_预估退货率 and 计_成交率 and 计_均SFB:
                拍卖总成本 = float(计_产品进价) + 运费
                拍卖保底价 = ((((拍卖总成本 * (1 + (float(计_拍卖利润率) / 100)) / float(计_当前汇率)) + 1.3) / 0.881) / (
                        (100 - float(计_预估退货率)) / 100)) + (
                                (2 - (float(计_成交率) / 100)) * float(计_均SFB))  # 拍卖保本价
                拍卖利润 = 拍卖总成本 * (float(计_拍卖利润率) / 100)

            if 计_预估退货率:
                一口价总成本 = float(计_产品进价) + 运费 + float('0') * float(计_当前汇率)
                建议一口价 = (((一口价总成本 * (1 + (float(计_一口价利润) / 100)) / float(计_当前汇率)) + 1.3) / 0.881) / (
                        (100 - float(计_预估退货率)) / 100)  # 建议一口价
                一口价利润 = 一口价总成本 * (float(计_一口价利润) / 100)

            运费 = round(运费, 2)
            拍卖总成本 = round(拍卖总成本, 2)
            拍卖保底价 = round(拍卖保底价, 2)
            一口价总成本 = round(一口价总成本, 2)
            建议一口价 = round(建议一口价, 2)
            拍卖利润 = round(拍卖利润, 2)
            一口价利润 = round(一口价利润, 2)

            data_msg_e = {'msg_e_1': str(运费),
                          'msg_e_2': str(拍卖总成本),
                          'msg_e_3': str(拍卖保底价),
                          'msg_e_4': str(一口价总成本),
                          'msg_e_5': str(建议一口价),
                          'msg_e_6': str(拍卖利润),
                          'msg_e_7': str(一口价利润),
                          }

            # print(data_msg_e)
            return HttpResponse(json.dumps(data_msg_e))

        username = request.session.get('username')
        USER = models.User.objects.filter(username=username).values('USER_ID', 'PRIVILEGE')
        USER_ID = USER[0]['USER_ID']
        PRIVILEGE = USER[0]['PRIVILEGE']
        PRIVILEGE = int(PRIVILEGE)
        head_portraits = models.User.objects.filter(username=username).values()[0]['head_portraits']
        context = {
            'USER_ID': USER_ID,
            'username': username,
            'PRIVILEGE': PRIVILEGE,
            'head_portraits': head_portraits,
            'exchange_rate': exchange_rate,
        }
        return render(request, 'index.html', context)


# 记录用户访问记录
def change_info(request, pagename, user):  # 修改网站访问量和访问ip等信息
    # user = request.session.get('username')
    date = datetime.datetime.now().date()
    # 每一次访问，网站总访问次数加一
    count_nums = models.VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = models.VisitNumber()
        count_nums.count = 1
    count_nums.save()

    # 记录访问用户和每个用户访问的次数
    user_exist = models.User_name.objects.filter(username=str(user))
    if user_exist:  # 判断是否存在该用户
        uobj = user_exist[0]
        uobj.count += 1
    else:
        uobj = models.User_name()
        uobj.username = user
        uobj.count = 1
    uobj.save()

    # 记录访问用户详细访问信息
    today_page = models.User_page_name.objects.filter(day=date)
    if today_page:  # 判断是否是新的一天
        user_exist_page = models.User_page_name.objects.filter(day=date, username=str(user))
        if user_exist_page:  # 判断是否存在该用户
            pagename_exist = models.User_page_name.objects.filter(day=date, username=str(user), page_name=str(pagename))
            if pagename_exist:  # 判断是否存在该页面
                temp_page = pagename_exist[0]
                temp_page.count += 1
                temp_page.last_time = datetime.datetime.now()
            else:
                temp_page = models.User_page_name()
                temp_page.day = date
                temp_page.username = user
                temp_page.page_name = pagename
                temp_page.count = 1
                temp_page.last_time = datetime.datetime.now()
        else:
            temp_page = models.User_page_name()
            temp_page.day = date
            temp_page.username = user
            temp_page.page_name = pagename
            temp_page.count = 1
            temp_page.last_time = datetime.datetime.now()
    else:
        temp_page = models.User_page_name()
        temp_page.day = date
        temp_page.username = user
        temp_page.page_name = pagename
        temp_page.count = 1
        temp_page.last_time = datetime.datetime.now()
    temp_page.save()

    # 增加今日访问次数
    today = models.DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = models.DayNumber()
        temp.day = date
        temp.count = 1
    temp.save()
