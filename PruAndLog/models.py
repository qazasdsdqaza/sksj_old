from django.db import models

# Create your models here.
#商品库
class Products_All_Own(models.Model):
    product_name = models.CharField(unique=True,null=True,max_length=200, verbose_name='产品名称')
    internal_id = models.IntegerField(null=True, verbose_name='商品ID')

    category = models.CharField(null=True,max_length=500, verbose_name='分类')
    title = models.CharField(null=True,max_length=500, verbose_name='标题')
    description = models.TextField(null=True, verbose_name='描述')
    condition = models.CharField(null=True,max_length=200, verbose_name='产品情况')
    brand = models.CharField(null=True,max_length=200, verbose_name='商标')
    material = models.CharField(null=True,max_length=200, verbose_name='材料')
    available_quantity = models.CharField(null=True,max_length=100, verbose_name='可售数量')
    color = models.CharField(null=True,max_length=500, verbose_name='颜色')
    size = models.CharField(null=True,max_length=500, verbose_name='尺寸')#11

    retail_price = models.CharField(null=True,max_length=100, verbose_name='零售价')
    cost_basis = models.CharField(null=True,max_length=100, verbose_name='目标价')
    minimum_bid_amount = models.CharField(null=True,max_length=100, verbose_name='起拍价')
    max_daily_schedules = models.CharField(null=True,max_length=100, verbose_name='最大每日排单量')
    scheduling_fee_bid = models.CharField(null=True,max_length=100, verbose_name='SFB')
    reserve_price = models.CharField(null=True,max_length=100, verbose_name='底价')
    shipping_price = models.CharField(null=True,max_length=100, verbose_name='运费')
    shipping_origin = models.CharField(null=True,max_length=200, verbose_name='发货地')
    fulfillment_partner = models.CharField(null=True,max_length=100, verbose_name='合作伙伴')
    weight = models.CharField(null=True,max_length=100, verbose_name='重量')
    days_to_fulfill = models.CharField(null=True,max_length=100, verbose_name='完成交付时间')
    days_to_deliver = models.CharField(null=True,max_length=100, verbose_name='处理时间')#23

    expedited_shipping_price = models.CharField(null=True,max_length=100, verbose_name='加快航运价格')
    expedited_days_to_deliver = models.CharField(null=True,max_length=100, verbose_name='加快交货时间')
    buy_one_get_one_available = models.CharField(null=True, max_length=50, verbose_name='买一送一')
    accessory_price = models.CharField(null=True,max_length=100, verbose_name='配件价格')
    accessory_description = models.CharField(null=True, max_length=200, verbose_name='配件描述')
    primary_image = models.CharField(null=True,max_length=500, verbose_name='主图')
    all_images = models.TextField(null=True, verbose_name='所有图')
    ratings_count = models.CharField(null=True,max_length=100, verbose_name='评论数')
    ratings_average = models.FloatField(null=True, verbose_name='平均评分')#32

    buy_now_price = models.CharField(null=True,max_length=100, verbose_name='一口价')
    campaign_name = models.CharField(null=True,max_length=30, verbose_name='campaign_name')

    created_at = models.DateTimeField(null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(null=True, verbose_name='更新时间')
    disabled_at = models.DateTimeField(null=True, verbose_name='取消售卖时间')

    user_collect = models.CharField(null=True, max_length=500, verbose_name='是否收藏')
    user_collect_reason = models.CharField(null=True, max_length=500, verbose_name='是否收藏')
    colloct_at = models.DateTimeField(null=True, verbose_name='收藏时间')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')

    standard_product_id = models.IntegerField(unique=True, null=True, verbose_name='商品标准ID')  # 从平台数据获取，用于对接平台数据，本店同类型数据区分
    lots_id = models.CharField(null=True, max_length=40, verbose_name='标准搜索ID')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')

    cat_name = models.CharField(null=True, max_length=200, verbose_name='5M分类') #45
    主图序号 = models.CharField(null=True, max_length=10, verbose_name='主图序号')  # 46

#汇率
class get_exchange_rate(models.Model):
    汇率名 = models.CharField(null=True,max_length=200, verbose_name='汇率名')
    exchange_rate_0 = models.FloatField(null=True, verbose_name='汇率0原始')
    exchange_rate = models.FloatField(null=True, verbose_name='汇率')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')

#汇率
class warehouse_show_data(models.Model):
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    发货仓库 = models.CharField(null=True,max_length=200, verbose_name='发货仓库')
    发货数 = models.FloatField(null=True, verbose_name='发货数')
    物流商数 = models.FloatField(null=True, verbose_name='物流商数')
    date_time = models.DateField(null=True, verbose_name='更新数据时间')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')


#基本参数
class key_parameter(models.Model):
    打包成本 =       models.FloatField(null=True, verbose_name='打包成本')
    汇损 =           models.FloatField(null=True, verbose_name='汇损')
    预估买家退货率 = models.FloatField(null=True, verbose_name='预估买家退货率')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')


