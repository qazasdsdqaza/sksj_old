from django.db import models

# Create your models here.
# 5miles_店铺密匙
class APIAccessToken_5miles(models.Model):
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

#5miles_资金数据_
class funds_5miles_date(models.Model):

    店铺名 = models.CharField(null=True, max_length=200, verbose_name=' 店铺名')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    可提现 = models.CharField(null=True, max_length=200, verbose_name=' 可提现')
    待确认 = models.CharField(null=True, max_length=200, verbose_name=' 待确认')
    提现中 = models.CharField(null=True, max_length=200, verbose_name=' 提现中')
    Time_Date = models.DateField(null=True, max_length=30, verbose_name='数据生成日期')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')


# 5miles_订单数据
class orders_date_5miles(models.Model):
    """店铺销售数据"""
    store_name = models.CharField(null=True,max_length=30, verbose_name='店铺名称')

    order_id = models.CharField(null=True,max_length=500, verbose_name='订单id')
    seq_no = models.CharField(null=True,max_length=200, verbose_name='订单编号')
    state = models.CharField(null=True, max_length=200, verbose_name='订单状态')
    shipping_fee = models.FloatField(null=True,verbose_name='运费金额')
    amount = models.FloatField(null=True,verbose_name='成交金额')
    total_amount = models.FloatField(null=True, verbose_name='总金额')
    created_at = models.CharField(null=True,max_length=200, verbose_name='订单创建时间')
    paid_at = models.CharField(null=True,max_length=200, verbose_name='订单付款时间')
    buyer_name = models.CharField(null=True,max_length=100, verbose_name='买家名称')

    item_lines = models.CharField(null=True,max_length=5000, verbose_name='订单信息')
    shipping_address = models.CharField(null=True, max_length=5000, verbose_name='发货地址')
    ship_list = models.CharField(null=True, max_length=5000, verbose_name='物流信息')
    approved_at = models.CharField(null=True, max_length=100, verbose_name='确认时间')

    sku_no = models.CharField(null=True, max_length=200, verbose_name='SKU名字')
    goods_name = models.CharField(null=True, max_length=200, verbose_name='商品名称')
    goods_main_image_url = models.CharField(null=True, max_length=200, verbose_name='商品主图')
    tracking_no = models.CharField(null=True, max_length=200, verbose_name='运单号')
    country = models.CharField(null=True, max_length=200, verbose_name='买家国家')

    status_Approved = models.CharField(null=True, max_length=200, verbose_name='订单状态1')
    status_Dispatched = models.CharField(null=True, max_length=200, verbose_name='订单状态2')
    status_Completed = models.CharField(null=True, max_length=200, verbose_name='订单状态3')
    status_Refunded = models.CharField(null=True, max_length=200, verbose_name='订单状态4')
    status_Canceled = models.CharField(null=True, max_length=200, verbose_name='订单状态5')
    status_Closed = models.CharField(null=True, max_length=200, verbose_name='订单状态6')

    created_at_data = models.DateField(null=True, verbose_name='创建日期')
    paid_at_data = models.DateField(null=True, verbose_name='付款日期')
    approved_at_data = models.DateField(null=True, verbose_name='确认日期')

    SKU_price = models.FloatField(null=True, max_length=200, verbose_name='单价')
    SKU_parts_price = models.FloatField(null=True, max_length=200, verbose_name='配件单价')
    SKU_freight = models.FloatField(null=True, max_length=200, verbose_name='单个运费')
    SKU_parts_freight = models.FloatField(null=True, max_length=200, verbose_name='配件运费')
    SKU_buy_one_freight = models.FloatField(null=True, max_length=200, verbose_name='买一得一运费')

    save_time = models.DateTimeField(null=True,auto_now_add = True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')

#店铺商品
class Products_5miles(models.Model):
    store_name = models.CharField(null=True, max_length=30, verbose_name='店铺名称')

    products_id = models.IntegerField(null=True, verbose_name='商品ID')
    goods_no = models.CharField(null=True,max_length=200, verbose_name='商品编号')
    cat_id = models.CharField(null=True,max_length=200, verbose_name='分类号')
    cat_name = models.CharField(null=True, max_length=200, verbose_name='分类')
    original_sale_price = models.CharField(null=True, max_length=200, verbose_name='原价格')
    start_price = models.CharField(null=True, max_length=200, verbose_name='起拍价')
    purchase_price = models.CharField(null=True, max_length=200, verbose_name='购买价格') #8
    reserve_price = models.CharField(null=True, max_length=200, verbose_name='保留价格')
    shipping_fee = models.CharField(null=True, max_length=200, verbose_name='运费')
    cost_price = models.CharField(null=True, max_length=200, verbose_name='成本价格')
    name = models.CharField(null=True, max_length=200, verbose_name='名称')

    description = models.TextField(null=True, verbose_name='描述')#13
    main_image_url = models.CharField(null=True,max_length=200, verbose_name='主图')
    weight = models.CharField(null=True, max_length=200, verbose_name='重量')
    min_delivery_days = models.CharField(null=True, max_length=200, verbose_name='最小处理日期')
    max_delivery_days = models.CharField(null=True, max_length=200, verbose_name='最大处理日期')
    delivery_address = models.CharField(null=True, max_length=200, verbose_name='发货地址')

    image_set = models.CharField(null=True, max_length=4000, verbose_name='图片详情')
    sku_set = models.CharField(null=True, max_length=4000, verbose_name='变种详情')
    detail_image_set = models.CharField(null=True, max_length=4000, verbose_name='图片描述详情')

    user_collect = models.CharField(null=True, max_length=15, verbose_name='是否收藏')
    user_collect_reason = models.CharField(null=True, max_length=500, verbose_name='收藏理由')
    colloct_at = models.DateTimeField(null=True, verbose_name='收藏时间')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')