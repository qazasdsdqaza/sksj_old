from django.db import models

# Create your models here.

# TOP店铺信息
class APIAccessToken(models.Model):
    """店铺密钥"""
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    username = models.CharField(null=True, max_length=50, verbose_name='用户名')
    store_name = models.CharField(null=True, max_length=50, verbose_name='店铺名称')
    seller_id = models.CharField(null=True, max_length=50, verbose_name='卖家ID')

    store_APIToken = models.CharField(null=True, max_length=100, verbose_name='API密钥')
    IP_address = models.CharField(null=True, max_length=100, verbose_name='店铺IP地址和端口')
    store_cookie = models.CharField(null=True, max_length=10000, verbose_name='店铺cookie')

    store_APIToken_status = models.IntegerField(default=0, verbose_name='API密钥_状态')
    IP_address_status = models.IntegerField(default=0, verbose_name='店铺IP地址和端口_状态')
    store_cookie_status = models.IntegerField(default=0, verbose_name='店铺cookie_状态')

    beizhu = models.CharField(null=True, max_length=10000, verbose_name='店铺详细备注')
    created_time = models.DateTimeField(null=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(null=True, verbose_name='更新时间')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')

    def __str__(self):
        return self.store_name
# IP 库

#orders _ 订单数据
class StoreSellData(models.Model):
    """店铺销售数据"""
    store_name = models.CharField(null=True,max_length=30, verbose_name='店铺名称')

    order_id = models.IntegerField(null=True, verbose_name='订单id号')
    status = models.CharField(null=True,max_length=200, verbose_name='订单状态')
    status_paid = models.CharField(null=True, max_length=200, verbose_name='付款状态')
    status_shipped = models.CharField(null=True, max_length=200, verbose_name='运输状态')
    status_refunded = models.CharField(null=True, max_length=200, verbose_name='退货状态')

    related_order_ids = models.CharField(null=True, max_length=200, verbose_name='关系订单')
    service_type = models.CharField(null=True, max_length=200, verbose_name='服务种类')

    carrier = models.CharField(null=True,max_length=200, verbose_name='运输公司')
    tracking_number = models.CharField(null=True,max_length=200, verbose_name='物流单号')
    fulfillment_partner = models.CharField(null=True,max_length=200, verbose_name='合作伙伴')
    product_name = models.CharField(null=True,max_length=1000, verbose_name='产品名字')
    product_identifier = models.CharField(null=True,max_length=200, verbose_name='产品标识')
    product_internal_id = models.IntegerField(null=True, verbose_name='产品ID')
    variation_identifier = models.CharField(null=True,max_length=200, verbose_name='变种产品标识')
    variation_internal_id = models.IntegerField(null=True, verbose_name='变种产品ID')
    customer_id = models.IntegerField(null=True, verbose_name='客户ID')
    customer_name = models.CharField(null=True,max_length=200, verbose_name='客户姓名')
    address1 = models.CharField(null=True,max_length=200, verbose_name='地址1')
    address2 = models.CharField(null=True,max_length=200, verbose_name='地址2')
    city = models.CharField(null=True,max_length=200, verbose_name='城市')
    state = models.CharField(null=True,max_length=200, verbose_name='州')
    postal_code = models.CharField(null=True,max_length=200, verbose_name='邮政编码')
    country = models.CharField(null=True,max_length=200, verbose_name='国家')
    available_refunds_buyer_fee = models.FloatField(null=True,verbose_name='买家可用金额')
    refund_amount = models.FloatField(null=True,verbose_name='退款金额')
    disbursement_amount = models.CharField(null=True,max_length=200, verbose_name='到手价')
    seller_fees_amount = models.FloatField(null=True,verbose_name='卖家支付金额')

    seller_fees_type_sfb = models.CharField(null=True,max_length=200, verbose_name='SFB花费')
    seller_fees_type_buy_nows = models.CharField(null=True, max_length=200, verbose_name='一口价')
    seller_fees_type_buy_nows_price = models.CharField(null=True, max_length=200, verbose_name='一口价价格')
    seller_fees_amount_sfb = models.FloatField(null=True,verbose_name='SFB费用')
    seller_fees_type_com = models.CharField(null=True, max_length=200, verbose_name='佣金')
    seller_fees_amount_com = models.FloatField(null=True,verbose_name='佣金费用')
    seller_fees_type_pro = models.CharField(null=True, max_length=200, verbose_name='手续费')
    seller_fees_amount_pro = models.FloatField(null=True,verbose_name='手续费费用')

    upsells_type_description1 = models.CharField(null=True, max_length=200, verbose_name='追销类型1')
    upsells_amount1 = models.CharField(null=True, max_length=200, verbose_name='追销类型1费用')
    upsells_description1 = models.CharField(null=True, max_length=500, verbose_name='追销类型1描述')
    upsells_type_description2 = models.CharField(null=True, max_length=200, verbose_name='追销类型2')
    upsells_amount2 = models.CharField(null=True, max_length=200, verbose_name='追销类型2费用')
    upsells_description2 = models.CharField(null=True, max_length=500, verbose_name='追销类型2描述')

    refunded_at = models.DateTimeField(null=True, verbose_name='退货时间')
    paid_at = models.DateTimeField(null=True, verbose_name='付款时间')
    created_at = models.DateTimeField(null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(null=True, verbose_name='更新时间')
    canceled_at = models.DateTimeField(null=True, verbose_name='取消订单时间')

    refunded_at_own = models.DateTimeField(null=True, verbose_name='自己退货时间')
    refunded_at_buyer = models.DateTimeField(null=True, verbose_name='买家退货时间')

    refund_amount_own = models.FloatField(null=True,verbose_name='自己退款金额')
    refund_amount_buyer = models.FloatField(null=True,verbose_name='自己退款金额')

    canceled_refund_amount = models.FloatField(null=True,verbose_name='canceled_退款金额')
    canceled_disbursement_amount = models.CharField(null=True,max_length=200, verbose_name='canceled_支付金额')
    canceled_seller_fees_amount = models.FloatField(null=True,verbose_name='canceled_卖家支付金额')

    save_time = models.DateTimeField(null=True,auto_now_add = True, verbose_name='创建数据时间')
    product_quantity = models.IntegerField(null=True, verbose_name='订单数量')

    data_time_created_at = models.DateField(null=True,max_length=30, verbose_name='创建订单数据生成日期')
    data_time_paid_at = models.DateField(null=True, max_length=30, verbose_name='付款订单数据生成日期')
    hours_time_created_at = models.CharField(null=True,max_length=200, verbose_name='创建订单数据生成时间段')

    SKU_price = models.FloatField(null=True, max_length=200, verbose_name='单价')
    SKU_parts_price = models.FloatField(null=True, max_length=200, verbose_name='配件单价')
    SKU_freight = models.FloatField(null=True, max_length=200, verbose_name='单个运费')
    SKU_parts_freight = models.FloatField(null=True, max_length=200, verbose_name='配件运费')
    SKU_buy_one_price = models.FloatField(null=True, max_length=200, verbose_name='买一得一进价')
    SKU_buy_one_freight = models.FloatField(null=True, max_length=200, verbose_name='买一得一运费')

    dxm_总 = models.CharField(null=True, max_length=200, verbose_name='店小秘物流状态1')
    dxm_未查到 = models.CharField(null=True,max_length=200, verbose_name='店小秘物流状态2')
    dxm_已签收 = models.CharField(null=True, max_length=200, verbose_name='店小秘物流状态3')
    dxm_有异常 = models.CharField(null=True, max_length=200, verbose_name='店小秘物流状态4')
    dxm_运输过久 = models.CharField(null=True, max_length=200, verbose_name='店小秘物流状态5')
    dxm_运输中 = models.CharField(null=True, max_length=200, verbose_name='店小秘物流状态6')

    ht_订单状态 = models.CharField(null=True, max_length=200, verbose_name='后台导入_订单状态')
    ht_物流状态 = models.CharField(null=True, max_length=200, verbose_name='后台导入_物流状态')

    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
#买家退货率
class closing_buyer(models.Model):
    """店铺密钥"""
    SKU = models.CharField(null=True, max_length=100, verbose_name='SKU')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    closing_buyer_1 = models.CharField(null=True, max_length=100, verbose_name='买家退货率')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')

#performs _ 3小时保存一次销售数据_actions
class Performance_hours_time(models.Model):
    """店铺销售数据"""
    store_name = models.CharField(null=True,max_length=30, verbose_name='店铺名称')
    time_local = models.DateField(null=True,max_length=30, verbose_name='数据日期')
    time_hours_local = models.DateTimeField(null=True, verbose_name='数据日期时间')
    time_hours_local_symbol = models.CharField(null=True, max_length=30, verbose_name='数据日期时间标志')
    TIME_SELECT = models.CharField(null=True, max_length=30, verbose_name='时间标识')

    identifier = models.CharField(null=True,max_length=200, verbose_name='SKU')
    cost_basis = models.CharField(null=True,max_length=200, verbose_name='基本花费')
    schedules = models.IntegerField(null=True, verbose_name='排单')
    orders = models.IntegerField(null=True, verbose_name='订单')
    revenue = models.FloatField(null=True, verbose_name='收入')
    fees = models.FloatField(null=True, verbose_name='收费')
    scheduling_fees = models.FloatField(null=True,max_length=200, verbose_name='安排费用')

    save_time = models.DateTimeField(null=True,auto_now_add = True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=1, verbose_name='用户id')

# 商品单价/运费
class Price_Freight(models.Model):
    identifier = models.CharField(null=True,max_length=200, verbose_name='SKU')
    standard_product_id = models.CharField(null=True, max_length=100, verbose_name='产品标准ID')
    SKU_price = models.CharField(null=True,max_length=200, verbose_name='单价')
    SKU_parts_price= models.CharField(null=True,max_length=200, verbose_name='配件单价')
    SKU_weight = models.CharField(null=True,max_length=200, verbose_name='单个重量')
    SKU_parts_weight = models.CharField(null=True, max_length=200, verbose_name='配件重量')
    SKU_variety = models.CharField(null=True, max_length=200, verbose_name='商品种类')
    HAI_SKU_freight = models.CharField(null=True,max_length=200, verbose_name='海运单个运费')

    Pingyou_min7_SKU_freight = models.CharField(null=True, max_length=200, verbose_name='小于7美元单价')
    Pingyou_max7_SKU_freight = models.CharField(null=True, max_length=200, verbose_name='大于7美元单价')
    top_colect = models.CharField(null=True, max_length=20, verbose_name='收藏')

    data_date = models.DateTimeField(null=True, auto_now_add=True, verbose_name='数据时间')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')

    def __str__(self):
        return self.identifier
#TOP店铺商品
class Products(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')
    status = models.CharField(null=True,max_length=200, verbose_name='商品状态')
    identifier = models.CharField(null=True,max_length=200, verbose_name='SKU')
    internal_id = models.IntegerField(null=True, verbose_name='商品ID')

    standard_product_id = models.IntegerField(null=True, verbose_name='商品标准ID') # 从平台数据获取，用于对接平台数据，本店同类型数据区分
    category = models.CharField(null=True,max_length=500, verbose_name='分类')
    title = models.CharField(null=True,max_length=500, verbose_name='标题')
    description = models.TextField(null=True, verbose_name='描述')
    condition = models.CharField(null=True,max_length=200, verbose_name='产品情况')
    brand = models.CharField(null=True,max_length=200, verbose_name='商标')
    material = models.CharField(null=True,max_length=200, verbose_name='材料')
    available_quantity = models.IntegerField(null=True, verbose_name='可售数量')
    variations = models.TextField(null=True, verbose_name='变种产品')#12

    retail_price = models.FloatField(null=True, verbose_name='零售价')
    cost_basis = models.FloatField(null=True, verbose_name='基础成本')
    minimum_bid_amount = models.FloatField(null=True, verbose_name='最低报价金额')
    max_daily_schedules = models.FloatField(null=True, verbose_name='最大每日排单量')
    scheduling_fee_bid = models.FloatField(null=True, verbose_name='SFB')
    reserve_price = models.FloatField(null=True, verbose_name='最低价格')
    shipping_price = models.FloatField(null=True, verbose_name='运费')
    shipping_origin = models.CharField(null=True,max_length=200, verbose_name='发货地')
    fulfillment_partner = models.FloatField(null=True, verbose_name='合作伙伴')
    weight = models.FloatField(null=True, verbose_name='重量')
    days_to_fulfill = models.FloatField(null=True, verbose_name='每天完成')
    days_to_deliver = models.FloatField(null=True, verbose_name='每天交付')#24

    expedited_shipping_price = models.FloatField(null=True, verbose_name='加快航运价格')
    expedited_days_to_deliver = models.FloatField(null=True, verbose_name='加快交货时间')
    buy_one_get_one_price = models.FloatField(null=True, verbose_name='买一送一价格')
    upsells = models.TextField(null=True, verbose_name='追销')
    primary_image = models.CharField(null=True,max_length=500, verbose_name='主图')
    extra_images = models.CharField(null=True,max_length=1000, verbose_name='额外图')
    all_images = models.TextField(null=True, verbose_name='所有图')
    ratings_count = models.FloatField(null=True, verbose_name='评论数')
    ratings_average = models.FloatField(null=True, verbose_name='平均评分')#33

    buy_now_price = models.FloatField(null=True, verbose_name='buy_now_price')
    campaign_name = models.CharField(null=True,max_length=30, verbose_name='campaign_name')#35

    created_at = models.DateTimeField(null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(null=True, verbose_name='更新时间')
    disabled_at = models.DateTimeField(null=True, verbose_name='取消售卖时间')

    user_collect = models.CharField(null=True, max_length=15, verbose_name='是否收藏')
    user_collect_reason = models.CharField(null=True, max_length=500, verbose_name='是否收藏')
    colloct_at = models.DateTimeField(null=True, verbose_name='收藏时间')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')

#一口价页面数据
class buynows_statistics(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')
    time_local = models.DateField(null=True,max_length=30, verbose_name='数据日期')
    time_hours_local = models.DateTimeField(null=True, verbose_name='数据日期时间')
    time_hours_local_symbol = models.CharField(null=True, max_length=30, verbose_name='数据日期时间标志')
    TIME_SELECT = models.CharField(null=True, max_length=30, verbose_name='时间标识')

    Impressions = models.CharField(null=True,max_length=200, verbose_name='展示数')
    Views = models.CharField(null=True,max_length=200, verbose_name='浏览数')
    Orders = models.CharField(null=True,max_length=200, verbose_name='订单数')
    Fees = models.CharField(null=True,max_length=200, verbose_name='费用')
    CPM = models.CharField(null=True,max_length=200, verbose_name='CPM')
    Cost_per_Order = models.CharField(null=True, max_length=200, verbose_name='单花费')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
class buynows_oders(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')
    time_local = models.DateField(null=True,max_length=30, verbose_name='数据日期')
    time_hours_local = models.DateTimeField(null=True, verbose_name='数据日期时间')
    time_hours_local_symbol = models.CharField(null=True, max_length=30, verbose_name='数据日期时间标志')
    TIME_SELECT = models.CharField(null=True, max_length=30, verbose_name='时间标识')

    identifier = models.CharField(null=True,max_length=200, verbose_name='SKU')
    img_buynows = models.CharField(null=True,max_length=200, verbose_name='主图')
    describe = models.CharField(null=True,max_length=200, verbose_name='描述')
    Impressions = models.CharField(null=True,max_length=500, verbose_name='展示数')
    Views = models.TextField(null=True, verbose_name='浏览数')
    Orders = models.CharField(null=True,max_length=200, verbose_name='订单数')
    Fees = models.CharField(null=True,max_length=200, verbose_name='费用')
    CPM = models.CharField(null=True,max_length=200, verbose_name='CPM')
    Cost_per_Order = models.CharField(null=True, max_length=200, verbose_name='单花费')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
#Home页TODO数据
class TODO(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')
    name = models.CharField(null=True,max_length=500, verbose_name='名称')
    data = models.CharField(null=True,max_length=500, verbose_name='数据')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')

#店铺资金
class Founds(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    Upcoming = models.CharField(null=True,max_length=200, verbose_name='即将到来')
    Pending= models.CharField(null=True,max_length=200, verbose_name='有待')
    Time_Date = models.DateField(null=True, max_length=30, verbose_name='数据生成日期')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    def __str__(self):
        return self.store_name
#店铺回款标志
class Count_logo(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')
    Count_logo = models.CharField(null=True,max_length=200, verbose_name='下次回款标志')
    Count_logo_time = models.DateField(null=True,max_length=30, verbose_name='下次回款日期')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')

    def __str__(self):
        return self.store_name

#店铺物流规则
class logistics_statistic(models.Model):
    STAR_DATE = models.DateField( null=True, verbose_name='保存开始日期')
    END_DATE = models.DateField(null=True, verbose_name='保存结束日期')

    美国_每克_普货 = models.CharField(null=True, max_length=200, verbose_name='美国_每克_普货')
    美国_每克_带电 = models.CharField(null=True, max_length=200, verbose_name='美国_每克_带电')
    美国_每克_特货 = models.CharField(null=True, max_length=200, verbose_name='美国_每克_特货')
    美国_挂号_普货 = models.CharField(null=True, max_length=200, verbose_name='美国_挂号_普货')
    美国_挂号_带电 = models.CharField(null=True, max_length=200, verbose_name='美国_挂号_带电')
    美国_挂号_特货 = models.CharField(null=True, max_length=200, verbose_name='美国_挂号_特货')
    美国_销售比 =   models.CharField(null=True, max_length=200, verbose_name='美国_销售比 =')
    美国_折扣_普货 = models.CharField(null=True, max_length=200, verbose_name='美国_折扣_普货')
    美国_折扣_带电 = models.CharField(null=True, max_length=200, verbose_name='美国_折扣_带电')
    美国_折扣_特货 = models.CharField(null=True, max_length=200, verbose_name='美国_折扣_特货')

    英国_每克_普货 = models.CharField(null=True, max_length=200, verbose_name=' 英国_每克_普货')
    英国_每克_带电 = models.CharField(null=True, max_length=200, verbose_name=' 英国_每克_带电')
    英国_每克_特货 = models.CharField(null=True, max_length=200, verbose_name=' 英国_每克_特货')
    英国_挂号_普货 = models.CharField(null=True, max_length=200, verbose_name=' 英国_挂号_普货')
    英国_挂号_带电 = models.CharField(null=True, max_length=200, verbose_name=' 英国_挂号_带电')
    英国_挂号_特货 = models.CharField(null=True, max_length=200, verbose_name=' 英国_挂号_特货')
    英国_销售比  =  models.CharField(null=True, max_length=200, verbose_name=' 英国_销售比')
    英国_折扣_普货 = models.CharField(null=True, max_length=200, verbose_name=' 英国_折扣_普货')
    英国_折扣_带电 = models.CharField(null=True, max_length=200, verbose_name=' 英国_折扣_带电')
    英国_折扣_特货 = models.CharField(null=True, max_length=200, verbose_name=' 英国_折扣_特货')

    加拿_每克_普货 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_每克_普货')
    加拿_每克_带电 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_每克_带电')
    加拿_每克_特货 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_每克_特货')
    加拿_挂号_普货 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_挂号_普货')
    加拿_挂号_带电 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_挂号_带电')
    加拿_挂号_特货 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_挂号_特货')
    加拿_销售比 =   models.CharField(null=True, max_length=200, verbose_name=' 加拿_销售比')
    加拿_折扣_普货 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_折扣_普货')
    加拿_折扣_带电 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_折扣_带电')
    加拿_折扣_特货 = models.CharField(null=True, max_length=200, verbose_name=' 加拿_折扣_特货')

    澳大_每克_普货 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_每克_普货')
    澳大_每克_带电 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_每克_带电')
    澳大_每克_特货 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_每克_特货')
    澳大_挂号_普货 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_挂号_普货')
    澳大_挂号_带电 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_挂号_带电')
    澳大_挂号_特货 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_挂号_特货')
    澳大_销售比 =   models.CharField(null=True, max_length=200, verbose_name=' 澳大_销售比')
    澳大_折扣_普货 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_折扣_普货')
    澳大_折扣_带电 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_折扣_带电')
    澳大_折扣_特货 = models.CharField(null=True, max_length=200, verbose_name=' 澳大_折扣_特货')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')

    def __str__(self):
        return self.store_namelogistics_statistic

#店铺物流规则
class campaign_list(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')

    name = models.CharField(null=True, max_length=30, verbose_name='campaign名称')
    type = models.CharField(null=True, max_length=30, verbose_name='类型')
    status = models.CharField(null=True, max_length=30, verbose_name='状态')
    daily_budget = models.FloatField(null=True, verbose_name='daily_budget')
    bid_amount = models.FloatField(null=True, verbose_name='bid_amount')
    daily_budget_per_product = models.FloatField(null=True, verbose_name='daily_budget_per_product')
    lifetime_budget = models.FloatField(null=True, verbose_name='lifetime_budget')
    lifetime_budget_per_product = models.FloatField(null=True, verbose_name='lifetime_budget_per_product')
    hourly_schedule = models.CharField(null=True, max_length=100, verbose_name='hourly_schedule')

    update_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='更新数据时间')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
