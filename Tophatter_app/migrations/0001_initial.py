# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-04-29 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIAccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
                ('username', models.CharField(max_length=50, null=True, verbose_name='用户名')),
                ('store_name', models.CharField(max_length=50, null=True, verbose_name='店铺名称')),
                ('seller_id', models.CharField(max_length=50, null=True, verbose_name='卖家ID')),
                ('store_APIToken', models.CharField(max_length=100, null=True, verbose_name='API密钥')),
                ('IP_address', models.CharField(max_length=100, null=True, verbose_name='店铺IP地址和端口')),
                ('store_cookie', models.CharField(max_length=10000, null=True, verbose_name='店铺cookie')),
                ('store_APIToken_status', models.IntegerField(default=0, verbose_name='API密钥_状态')),
                ('IP_address_status', models.IntegerField(default=0, verbose_name='店铺IP地址和端口_状态')),
                ('store_cookie_status', models.IntegerField(default=0, verbose_name='店铺cookie_状态')),
                ('beizhu', models.CharField(max_length=10000, null=True, verbose_name='店铺详细备注')),
                ('created_time', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(null=True, verbose_name='更新时间')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
            ],
        ),
        migrations.CreateModel(
            name='buynows_oders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('time_local', models.DateField(max_length=30, null=True, verbose_name='数据日期')),
                ('time_hours_local', models.DateTimeField(null=True, verbose_name='数据日期时间')),
                ('time_hours_local_symbol', models.CharField(max_length=30, null=True, verbose_name='数据日期时间标志')),
                ('TIME_SELECT', models.CharField(max_length=30, null=True, verbose_name='时间标识')),
                ('identifier', models.CharField(max_length=200, null=True, verbose_name='SKU')),
                ('img_buynows', models.CharField(max_length=200, null=True, verbose_name='主图')),
                ('describe', models.CharField(max_length=200, null=True, verbose_name='描述')),
                ('Impressions', models.CharField(max_length=500, null=True, verbose_name='展示数')),
                ('Views', models.TextField(null=True, verbose_name='浏览数')),
                ('Orders', models.CharField(max_length=200, null=True, verbose_name='订单数')),
                ('Fees', models.CharField(max_length=200, null=True, verbose_name='费用')),
                ('CPM', models.CharField(max_length=200, null=True, verbose_name='CPM')),
                ('Cost_per_Order', models.CharField(max_length=200, null=True, verbose_name='单花费')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='buynows_statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('time_local', models.DateField(max_length=30, null=True, verbose_name='数据日期')),
                ('time_hours_local', models.DateTimeField(null=True, verbose_name='数据日期时间')),
                ('time_hours_local_symbol', models.CharField(max_length=30, null=True, verbose_name='数据日期时间标志')),
                ('TIME_SELECT', models.CharField(max_length=30, null=True, verbose_name='时间标识')),
                ('Impressions', models.CharField(max_length=200, null=True, verbose_name='展示数')),
                ('Views', models.CharField(max_length=200, null=True, verbose_name='浏览数')),
                ('Orders', models.CharField(max_length=200, null=True, verbose_name='订单数')),
                ('Fees', models.CharField(max_length=200, null=True, verbose_name='费用')),
                ('CPM', models.CharField(max_length=200, null=True, verbose_name='CPM')),
                ('Cost_per_Order', models.CharField(max_length=200, null=True, verbose_name='单花费')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='closing_buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SKU', models.CharField(max_length=100, null=True, verbose_name='SKU')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
                ('closing_buyer_1', models.CharField(max_length=100, null=True, verbose_name='买家退货率')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
            ],
        ),
        migrations.CreateModel(
            name='Count_logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('Count_logo', models.CharField(max_length=200, null=True, verbose_name='下次回款标志')),
                ('Count_logo_time', models.DateField(max_length=30, null=True, verbose_name='下次回款日期')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Founds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('A_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('A_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('B_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('B_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('C_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('C_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('D_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('D_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('E_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('E_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('F_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('F_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('G_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('G_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('H_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('H_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('I_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('I_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('J_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('J_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('K_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('K_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('L_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('L_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('M_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('M_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('N_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('N_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('O_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('O_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('P_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('P_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('Q_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('Q_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('R_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('R_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('S_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('S_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('T_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('T_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('U_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('U_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('V_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('V_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('W_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('W_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('X_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('X_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('Y_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('Y_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('Z_Upcoming', models.CharField(max_length=200, null=True, verbose_name='即将到来')),
                ('Z_Pending', models.CharField(max_length=200, null=True, verbose_name='有待')),
                ('unpatented', models.CharField(max_length=200, null=True, verbose_name='现有资金')),
                ('Time_Date', models.DateField(max_length=30, null=True, verbose_name='数据生成日期')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='logistics_statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('STAR_DATE', models.DateField(null=True, unique=True, verbose_name='保存开始日期')),
                ('END_DATE', models.DateField(null=True, verbose_name='保存结束日期')),
                ('美国_每克_普货', models.CharField(max_length=200, null=True, verbose_name='美国_每克_普货')),
                ('美国_每克_带电', models.CharField(max_length=200, null=True, verbose_name='美国_每克_带电')),
                ('美国_每克_特货', models.CharField(max_length=200, null=True, verbose_name='美国_每克_特货')),
                ('美国_挂号_普货', models.CharField(max_length=200, null=True, verbose_name='美国_挂号_普货')),
                ('美国_挂号_带电', models.CharField(max_length=200, null=True, verbose_name='美国_挂号_带电')),
                ('美国_挂号_特货', models.CharField(max_length=200, null=True, verbose_name='美国_挂号_特货')),
                ('美国_销售比', models.CharField(max_length=200, null=True, verbose_name='美国_销售比 =')),
                ('美国_折扣_普货', models.CharField(max_length=200, null=True, verbose_name='美国_折扣_普货')),
                ('美国_折扣_带电', models.CharField(max_length=200, null=True, verbose_name='美国_折扣_带电')),
                ('美国_折扣_特货', models.CharField(max_length=200, null=True, verbose_name='美国_折扣_特货')),
                ('英国_每克_普货', models.CharField(max_length=200, null=True, verbose_name=' 英国_每克_普货')),
                ('英国_每克_带电', models.CharField(max_length=200, null=True, verbose_name=' 英国_每克_带电')),
                ('英国_每克_特货', models.CharField(max_length=200, null=True, verbose_name=' 英国_每克_特货')),
                ('英国_挂号_普货', models.CharField(max_length=200, null=True, verbose_name=' 英国_挂号_普货')),
                ('英国_挂号_带电', models.CharField(max_length=200, null=True, verbose_name=' 英国_挂号_带电')),
                ('英国_挂号_特货', models.CharField(max_length=200, null=True, verbose_name=' 英国_挂号_特货')),
                ('英国_销售比', models.CharField(max_length=200, null=True, verbose_name=' 英国_销售比')),
                ('英国_折扣_普货', models.CharField(max_length=200, null=True, verbose_name=' 英国_折扣_普货')),
                ('英国_折扣_带电', models.CharField(max_length=200, null=True, verbose_name=' 英国_折扣_带电')),
                ('英国_折扣_特货', models.CharField(max_length=200, null=True, verbose_name=' 英国_折扣_特货')),
                ('加拿_每克_普货', models.CharField(max_length=200, null=True, verbose_name=' 加拿_每克_普货')),
                ('加拿_每克_带电', models.CharField(max_length=200, null=True, verbose_name=' 加拿_每克_带电')),
                ('加拿_每克_特货', models.CharField(max_length=200, null=True, verbose_name=' 加拿_每克_特货')),
                ('加拿_挂号_普货', models.CharField(max_length=200, null=True, verbose_name=' 加拿_挂号_普货')),
                ('加拿_挂号_带电', models.CharField(max_length=200, null=True, verbose_name=' 加拿_挂号_带电')),
                ('加拿_挂号_特货', models.CharField(max_length=200, null=True, verbose_name=' 加拿_挂号_特货')),
                ('加拿_销售比', models.CharField(max_length=200, null=True, verbose_name=' 加拿_销售比')),
                ('加拿_折扣_普货', models.CharField(max_length=200, null=True, verbose_name=' 加拿_折扣_普货')),
                ('加拿_折扣_带电', models.CharField(max_length=200, null=True, verbose_name=' 加拿_折扣_带电')),
                ('加拿_折扣_特货', models.CharField(max_length=200, null=True, verbose_name=' 加拿_折扣_特货')),
                ('澳大_每克_普货', models.CharField(max_length=200, null=True, verbose_name=' 澳大_每克_普货')),
                ('澳大_每克_带电', models.CharField(max_length=200, null=True, verbose_name=' 澳大_每克_带电')),
                ('澳大_每克_特货', models.CharField(max_length=200, null=True, verbose_name=' 澳大_每克_特货')),
                ('澳大_挂号_普货', models.CharField(max_length=200, null=True, verbose_name=' 澳大_挂号_普货')),
                ('澳大_挂号_带电', models.CharField(max_length=200, null=True, verbose_name=' 澳大_挂号_带电')),
                ('澳大_挂号_特货', models.CharField(max_length=200, null=True, verbose_name=' 澳大_挂号_特货')),
                ('澳大_销售比', models.CharField(max_length=200, null=True, verbose_name=' 澳大_销售比')),
                ('澳大_折扣_普货', models.CharField(max_length=200, null=True, verbose_name=' 澳大_折扣_普货')),
                ('澳大_折扣_带电', models.CharField(max_length=200, null=True, verbose_name=' 澳大_折扣_带电')),
                ('澳大_折扣_特货', models.CharField(max_length=200, null=True, verbose_name=' 澳大_折扣_特货')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Performance_hours_time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('time_local', models.DateField(max_length=30, null=True, verbose_name='数据日期')),
                ('time_hours_local', models.DateTimeField(null=True, verbose_name='数据日期时间')),
                ('time_hours_local_symbol', models.CharField(max_length=30, null=True, verbose_name='数据日期时间标志')),
                ('TIME_SELECT', models.CharField(max_length=30, null=True, verbose_name='时间标识')),
                ('identifier', models.CharField(max_length=200, null=True, verbose_name='SKU')),
                ('cost_basis', models.CharField(max_length=200, null=True, verbose_name='基本花费')),
                ('schedules', models.IntegerField(null=True, verbose_name='排单')),
                ('orders', models.IntegerField(null=True, verbose_name='订单')),
                ('revenue', models.FloatField(null=True, verbose_name='收入')),
                ('fees', models.FloatField(null=True, verbose_name='收费')),
                ('scheduling_fees', models.FloatField(max_length=200, null=True, verbose_name='安排费用')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=1, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Price_Freight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=200, null=True, verbose_name='SKU')),
                ('standard_product_id', models.CharField(max_length=100, null=True, verbose_name='产品标准ID')),
                ('SKU_price', models.CharField(max_length=200, null=True, verbose_name='单价')),
                ('SKU_parts_price', models.CharField(max_length=200, null=True, verbose_name='配件单价')),
                ('SKU_weight', models.CharField(max_length=200, null=True, verbose_name='单个重量')),
                ('SKU_parts_weight', models.CharField(max_length=200, null=True, verbose_name='配件重量')),
                ('SKU_variety', models.CharField(max_length=200, null=True, verbose_name='商品种类')),
                ('HAI_SKU_freight', models.CharField(max_length=200, null=True, verbose_name='海运单个运费')),
                ('Pingyou_min7_SKU_freight', models.CharField(max_length=200, null=True, verbose_name='小于7美元单价')),
                ('Pingyou_max7_SKU_freight', models.CharField(max_length=200, null=True, verbose_name='大于7美元单价')),
                ('top_colect', models.CharField(max_length=20, null=True, verbose_name='收藏')),
                ('data_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据时间')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('status', models.CharField(max_length=200, null=True, verbose_name='商品状态')),
                ('identifier', models.CharField(max_length=200, null=True, verbose_name='SKU')),
                ('internal_id', models.IntegerField(null=True, verbose_name='商品ID')),
                ('standard_product_id', models.IntegerField(null=True, verbose_name='商品标准ID')),
                ('category', models.CharField(max_length=500, null=True, verbose_name='分类')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='标题')),
                ('description', models.TextField(null=True, verbose_name='描述')),
                ('condition', models.CharField(max_length=200, null=True, verbose_name='产品情况')),
                ('brand', models.CharField(max_length=200, null=True, verbose_name='商标')),
                ('material', models.CharField(max_length=200, null=True, verbose_name='材料')),
                ('available_quantity', models.IntegerField(null=True, verbose_name='可售数量')),
                ('variations', models.TextField(null=True, verbose_name='变种产品')),
                ('retail_price', models.FloatField(null=True, verbose_name='零售价')),
                ('cost_basis', models.FloatField(null=True, verbose_name='基础成本')),
                ('minimum_bid_amount', models.FloatField(null=True, verbose_name='最低报价金额')),
                ('max_daily_schedules', models.FloatField(null=True, verbose_name='最大每日排单量')),
                ('scheduling_fee_bid', models.FloatField(null=True, verbose_name='SFB')),
                ('reserve_price', models.FloatField(null=True, verbose_name='最低价格')),
                ('shipping_price', models.FloatField(null=True, verbose_name='运费')),
                ('shipping_origin', models.CharField(max_length=200, null=True, verbose_name='发货地')),
                ('fulfillment_partner', models.FloatField(null=True, verbose_name='合作伙伴')),
                ('weight', models.FloatField(null=True, verbose_name='重量')),
                ('days_to_fulfill', models.FloatField(null=True, verbose_name='每天完成')),
                ('days_to_deliver', models.FloatField(null=True, verbose_name='每天交付')),
                ('expedited_shipping_price', models.FloatField(null=True, verbose_name='加快航运价格')),
                ('expedited_days_to_deliver', models.FloatField(null=True, verbose_name='加快交货时间')),
                ('buy_one_get_one_price', models.FloatField(null=True, verbose_name='买一送一价格')),
                ('upsells', models.TextField(null=True, verbose_name='追销')),
                ('primary_image', models.CharField(max_length=500, null=True, verbose_name='主图')),
                ('extra_images', models.CharField(max_length=1000, null=True, verbose_name='额外图')),
                ('all_images', models.TextField(null=True, verbose_name='所有图')),
                ('ratings_count', models.FloatField(null=True, verbose_name='评论数')),
                ('ratings_average', models.FloatField(null=True, verbose_name='平均评分')),
                ('buy_now_price', models.FloatField(null=True, verbose_name='buy_now_price')),
                ('campaign_name', models.CharField(max_length=30, null=True, verbose_name='campaign_name')),
                ('created_at', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(null=True, verbose_name='更新时间')),
                ('disabled_at', models.DateTimeField(null=True, verbose_name='取消售卖时间')),
                ('user_collect', models.CharField(max_length=15, null=True, verbose_name='是否收藏')),
                ('user_collect_reason', models.CharField(max_length=500, null=True, verbose_name='是否收藏')),
                ('colloct_at', models.DateTimeField(null=True, verbose_name='收藏时间')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Products_All_Yaoqianshu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, null=True, unique=True, verbose_name='产品名称')),
                ('internal_id', models.IntegerField(null=True, verbose_name='商品ID')),
                ('category', models.CharField(max_length=500, null=True, verbose_name='分类')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='标题')),
                ('description', models.TextField(null=True, verbose_name='描述')),
                ('condition', models.CharField(max_length=200, null=True, verbose_name='产品情况')),
                ('brand', models.CharField(max_length=200, null=True, verbose_name='商标')),
                ('material', models.CharField(max_length=200, null=True, verbose_name='材料')),
                ('available_quantity', models.CharField(max_length=100, null=True, verbose_name='可售数量')),
                ('color', models.CharField(max_length=500, null=True, verbose_name='颜色')),
                ('size', models.CharField(max_length=500, null=True, verbose_name='尺寸')),
                ('retail_price', models.CharField(max_length=100, null=True, verbose_name='零售价')),
                ('cost_basis', models.CharField(max_length=100, null=True, verbose_name='目标价')),
                ('minimum_bid_amount', models.CharField(max_length=100, null=True, verbose_name='起拍价')),
                ('max_daily_schedules', models.CharField(max_length=100, null=True, verbose_name='最大每日排单量')),
                ('scheduling_fee_bid', models.CharField(max_length=100, null=True, verbose_name='SFB')),
                ('reserve_price', models.CharField(max_length=100, null=True, verbose_name='底价')),
                ('shipping_price', models.CharField(max_length=100, null=True, verbose_name='运费')),
                ('shipping_origin', models.CharField(max_length=200, null=True, verbose_name='发货地')),
                ('fulfillment_partner', models.CharField(max_length=100, null=True, verbose_name='合作伙伴')),
                ('weight', models.CharField(max_length=100, null=True, verbose_name='重量')),
                ('days_to_fulfill', models.CharField(max_length=100, null=True, verbose_name='完成交付时间')),
                ('days_to_deliver', models.CharField(max_length=100, null=True, verbose_name='处理时间')),
                ('expedited_shipping_price', models.CharField(max_length=100, null=True, verbose_name='加快航运价格')),
                ('expedited_days_to_deliver', models.CharField(max_length=100, null=True, verbose_name='加快交货时间')),
                ('buy_one_get_one_available', models.CharField(max_length=50, null=True, verbose_name='买一送一')),
                ('accessory_price', models.CharField(max_length=100, null=True, verbose_name='配件价格')),
                ('accessory_description', models.CharField(max_length=200, null=True, verbose_name='配件描述')),
                ('primary_image', models.CharField(max_length=500, null=True, verbose_name='主图')),
                ('all_images', models.TextField(null=True, verbose_name='所有图')),
                ('ratings_count', models.CharField(max_length=100, null=True, verbose_name='评论数')),
                ('ratings_average', models.FloatField(null=True, verbose_name='平均评分')),
                ('buy_now_price', models.CharField(max_length=100, null=True, verbose_name='一口价')),
                ('campaign_name', models.CharField(max_length=30, null=True, verbose_name='campaign_name')),
                ('created_at', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(null=True, verbose_name='更新时间')),
                ('disabled_at', models.DateTimeField(null=True, verbose_name='取消售卖时间')),
                ('user_collect', models.CharField(max_length=15, null=True, verbose_name='是否收藏')),
                ('user_collect_reason', models.CharField(max_length=500, null=True, verbose_name='是否收藏')),
                ('colloct_at', models.DateTimeField(null=True, verbose_name='收藏时间')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('standard_product_id', models.IntegerField(null=True, unique=True, verbose_name='商品标准ID')),
                ('lots_id', models.CharField(max_length=40, null=True, verbose_name='标准搜索ID')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='StoreSellData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('order_id', models.IntegerField(null=True, verbose_name='订单id号')),
                ('status', models.CharField(max_length=200, null=True, verbose_name='订单状态')),
                ('status_paid', models.CharField(max_length=200, null=True, verbose_name='付款状态')),
                ('status_shipped', models.CharField(max_length=200, null=True, verbose_name='运输状态')),
                ('status_refunded', models.CharField(max_length=200, null=True, verbose_name='退货状态')),
                ('related_order_ids', models.CharField(max_length=200, null=True, verbose_name='关系订单')),
                ('service_type', models.CharField(max_length=200, null=True, verbose_name='服务种类')),
                ('carrier', models.CharField(max_length=200, null=True, verbose_name='运输公司')),
                ('tracking_number', models.CharField(max_length=200, null=True, verbose_name='物流单号')),
                ('fulfillment_partner', models.CharField(max_length=200, null=True, verbose_name='合作伙伴')),
                ('product_name', models.CharField(max_length=1000, null=True, verbose_name='产品名字')),
                ('product_identifier', models.CharField(max_length=200, null=True, verbose_name='产品标识')),
                ('product_internal_id', models.IntegerField(null=True, verbose_name='产品ID')),
                ('variation_identifier', models.CharField(max_length=200, null=True, verbose_name='变种产品标识')),
                ('variation_internal_id', models.IntegerField(null=True, verbose_name='变种产品ID')),
                ('customer_id', models.IntegerField(null=True, verbose_name='客户ID')),
                ('customer_name', models.CharField(max_length=200, null=True, verbose_name='客户姓名')),
                ('address1', models.CharField(max_length=200, null=True, verbose_name='地址1')),
                ('address2', models.CharField(max_length=200, null=True, verbose_name='地址2')),
                ('city', models.CharField(max_length=200, null=True, verbose_name='城市')),
                ('state', models.CharField(max_length=200, null=True, verbose_name='州')),
                ('postal_code', models.CharField(max_length=200, null=True, verbose_name='邮政编码')),
                ('country', models.CharField(max_length=200, null=True, verbose_name='国家')),
                ('available_refunds_buyer_fee', models.FloatField(null=True, verbose_name='买家可用金额')),
                ('refund_amount', models.FloatField(null=True, verbose_name='退款金额')),
                ('disbursement_amount', models.CharField(max_length=200, null=True, verbose_name='到手价')),
                ('seller_fees_amount', models.FloatField(null=True, verbose_name='卖家支付金额')),
                ('seller_fees_type_sfb', models.CharField(max_length=200, null=True, verbose_name='SFB花费')),
                ('seller_fees_type_buy_nows', models.CharField(max_length=200, null=True, verbose_name='一口价')),
                ('seller_fees_type_buy_nows_price', models.CharField(max_length=200, null=True, verbose_name='一口价价格')),
                ('seller_fees_amount_sfb', models.FloatField(null=True, verbose_name='SFB费用')),
                ('seller_fees_type_com', models.CharField(max_length=200, null=True, verbose_name='佣金')),
                ('seller_fees_amount_com', models.FloatField(null=True, verbose_name='佣金费用')),
                ('seller_fees_type_pro', models.CharField(max_length=200, null=True, verbose_name='手续费')),
                ('seller_fees_amount_pro', models.FloatField(null=True, verbose_name='手续费费用')),
                ('upsells_type_description1', models.CharField(max_length=200, null=True, verbose_name='追销类型1')),
                ('upsells_amount1', models.CharField(max_length=200, null=True, verbose_name='追销类型1费用')),
                ('upsells_description1', models.CharField(max_length=500, null=True, verbose_name='追销类型1描述')),
                ('upsells_type_description2', models.CharField(max_length=200, null=True, verbose_name='追销类型2')),
                ('upsells_amount2', models.CharField(max_length=200, null=True, verbose_name='追销类型2费用')),
                ('upsells_description2', models.CharField(max_length=500, null=True, verbose_name='追销类型2描述')),
                ('refunded_at', models.DateTimeField(null=True, verbose_name='退货时间')),
                ('paid_at', models.DateTimeField(null=True, verbose_name='付款时间')),
                ('created_at', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(null=True, verbose_name='更新时间')),
                ('canceled_at', models.DateTimeField(null=True, verbose_name='取消订单时间')),
                ('refunded_at_own', models.DateTimeField(null=True, verbose_name='自己退货时间')),
                ('refunded_at_buyer', models.DateTimeField(null=True, verbose_name='买家退货时间')),
                ('refund_amount_own', models.FloatField(null=True, verbose_name='自己退款金额')),
                ('refund_amount_buyer', models.FloatField(null=True, verbose_name='自己退款金额')),
                ('canceled_refund_amount', models.FloatField(null=True, verbose_name='canceled_退款金额')),
                ('canceled_disbursement_amount', models.CharField(max_length=200, null=True, verbose_name='canceled_支付金额')),
                ('canceled_seller_fees_amount', models.FloatField(null=True, verbose_name='canceled_卖家支付金额')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('product_quantity', models.IntegerField(null=True, verbose_name='订单数量')),
                ('data_time_created_at', models.DateField(max_length=30, null=True, verbose_name='创建订单数据生成日期')),
                ('data_time_paid_at', models.DateField(max_length=30, null=True, verbose_name='付款订单数据生成日期')),
                ('hours_time_created_at', models.CharField(max_length=200, null=True, verbose_name='创建订单数据生成时间段')),
                ('SKU_price', models.FloatField(max_length=200, null=True, verbose_name='单价')),
                ('SKU_parts_price', models.FloatField(max_length=200, null=True, verbose_name='配件单价')),
                ('SKU_freight', models.FloatField(max_length=200, null=True, verbose_name='单个运费')),
                ('SKU_parts_freight', models.FloatField(max_length=200, null=True, verbose_name='配件运费')),
                ('SKU_buy_one_price', models.FloatField(max_length=200, null=True, verbose_name='买一得一进价')),
                ('SKU_buy_one_freight', models.FloatField(max_length=200, null=True, verbose_name='买一得一运费')),
                ('dxm_总', models.CharField(max_length=200, null=True, verbose_name='店小秘物流状态1')),
                ('dxm_未查到', models.CharField(max_length=200, null=True, verbose_name='店小秘物流状态2')),
                ('dxm_已签收', models.CharField(max_length=200, null=True, verbose_name='店小秘物流状态3')),
                ('dxm_有异常', models.CharField(max_length=200, null=True, verbose_name='店小秘物流状态4')),
                ('dxm_运输过久', models.CharField(max_length=200, null=True, verbose_name='店小秘物流状态5')),
                ('dxm_运输中', models.CharField(max_length=200, null=True, verbose_name='店小秘物流状态6')),
                ('ht_订单状态', models.CharField(max_length=200, null=True, verbose_name='后台导入_订单状态')),
                ('ht_物流状态', models.CharField(max_length=200, null=True, verbose_name='后台导入_物流状态')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='TODO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('name', models.CharField(max_length=500, null=True, verbose_name='名称')),
                ('data', models.CharField(max_length=500, null=True, verbose_name='数据')),
                ('save_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建数据时间')),
                ('USER_ID', models.IntegerField(default=0, verbose_name='用户id')),
            ],
        ),
    ]
