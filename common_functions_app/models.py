from django.db import models


# 平台总数据
class TopData(models.Model):
    """项目数据"""
    top_id = models.CharField(unique=True, null=True, max_length=40, verbose_name='搜索ID')
    lots_id = models.CharField(null=True, max_length=40, verbose_name='标准搜索ID')
    product_parent_id = models.IntegerField(null=True, verbose_name='产品父ID')
    standard_product_id = models.IntegerField(null=True, verbose_name='产品标准ID')
    user_id = models.IntegerField(null=True, verbose_name='用户ID')
    buyer_id = models.IntegerField(null=True, verbose_name='买家ID')
    default_variation_id = models.IntegerField(null=True, verbose_name='缺省变种ID')
    title = models.TextField(null=True, verbose_name='产品标题')
    taxonomy_values_0 = models.CharField(null=True, max_length=40, verbose_name='产品分类0')
    taxonomy_values_1 = models.CharField(null=True, max_length=40, verbose_name='产品分类1')
    taxonomy_values_2 = models.CharField(null=True, max_length=40, verbose_name='产品分类2')
    taxonomy_values_3 = models.CharField(null=True, max_length=40, verbose_name='产品分类3')
    facets = models.TextField(null=True, verbose_name='产品详细参数')
    description = models.TextField(null=True, verbose_name='产品描述')
    #
    new_guarantee = models.TextField(null=True, verbose_name='销售担保')
    image_urls_0 = models.URLField(null=True, verbose_name='产品详细图片0')
    image_urls_1 = models.URLField(null=True, verbose_name='产品详细图片1')
    image_urls_2 = models.URLField(null=True, verbose_name='产品详细图片2')
    image_urls_3 = models.URLField(null=True, verbose_name='产品详细图片3')
    image_urls_4 = models.URLField(null=True, verbose_name='产品详细图片4')
    image_urls_5 = models.URLField(null=True, verbose_name='产品详细图片5')
    main_image_width = models.IntegerField(null=True, verbose_name='头像图片宽度')
    main_image_height = models.IntegerField(null=True, verbose_name='头像图片长度')
    main_image = models.URLField(null=True, verbose_name='头像图片')
    currency = models.CharField(null=True, max_length=10, verbose_name='货币')
    buy_now_price = models.CharField(null=True, max_length=10, verbose_name='一口价')
    buy_now_price_local = models.IntegerField(null=True, verbose_name='当地一口价')
    buy_now_price_with_symbol = models.CharField(null=True, max_length=10, verbose_name='一口价标志')
    retail_price = models.CharField(null=True, max_length=10, verbose_name='零售价')
    #
    retail_price_local = models.FloatField(null=True, verbose_name='当地零售价')
    retail_price_with_symbol = models.CharField(null=True, max_length=10, verbose_name='零售价标志')
    retail_price_with_partial_symbol = models.CharField(null=True, max_length=10, verbose_name='当地零售价标志')
    buy_now_discount = models.FloatField(null=True, verbose_name='一口价折扣')
    starting_bid_amount = models.IntegerField(null=True, verbose_name='起拍数量')
    starting_bid_amount_local = models.IntegerField(null=True, verbose_name='当地起拍数量')
    starting_bid_amount_with_symbol = models.CharField(null=True, max_length=10, verbose_name='起拍标志')
    hammer_price = models.CharField(null=True, max_length=10, verbose_name='成交价')
    hammer_price_local = models.FloatField(null=True, verbose_name='本地成交价')
    hammer_price_with_symbol = models.CharField(null=True, max_length=10, verbose_name='成交价标志')

    shipping_price = models.CharField(null=True, max_length=10, verbose_name='运费')
    shipping_price_local = models.FloatField(null=True, verbose_name='本地运费')
    shipping_price_with_symbol = models.CharField(null=True, max_length=10, verbose_name='运费标志')
    alternate_title = models.TextField(null=True, verbose_name='替代商品标题')
    product_brand = models.CharField(null=True, max_length=50, verbose_name='产品商标')
    product_model = models.CharField(null=True, max_length=10, verbose_name='产品样式')
    alert = models.CharField(null=True, max_length=100, verbose_name='通告')
    hide_reminder = models.CharField(null=True, max_length=100, verbose_name='隐藏的提醒')
    alerts_count = models.IntegerField(null=True, verbose_name='通告次数')
    seller_name = models.CharField(null=True, max_length=50, verbose_name='卖家姓名')

    seller_positive_feedback_count = models.IntegerField(null=True, verbose_name='卖方积极反馈计数')
    seller_lots_sold = models.IntegerField(null=True, verbose_name='卖家总共卖出数量')
    calculate_ratings_count = models.IntegerField(null=True, verbose_name='评价数量')
    ratings_count_string = models.CharField(null=True, max_length=15, verbose_name='评价数量标识')
    ratings_average_string = models.CharField(null=True, max_length=15, verbose_name='平均评分标识')
    ratings_count = models.FloatField(null=True, verbose_name='评价数量')
    ratings_average = models.FloatField(null=True, verbose_name='平均评分')
    sizing_ratings = models.FloatField(null=True, verbose_name='分级评级')
    recent_ratings = models.TextField(null=True, verbose_name='最近评价详情')
    view_all_ratings = models.CharField(null=True, max_length=15, verbose_name='查看所有的评价')

    ships_to_user_country = models.CharField(null=True, max_length=15, verbose_name='运往用户所在国')
    shipping_description_local = models.CharField(null=True, max_length=100, verbose_name='快递描述')
    variations = models.TextField(null=True, verbose_name='变种商品')
    lot_upsells = models.TextField(null=True, verbose_name='更多销售')
    generic_sections = models.TextField(null=True, verbose_name='通用部分')
    analytics = models.TextField(null=True, verbose_name='分析')
    note = models.CharField(null=True, max_length=15, verbose_name='记录')
    buyer_prompt = models.CharField(null=True, max_length=15, verbose_name='买家提示')
    activated_at = models.DateTimeField(null=True, verbose_name='产品激活时间')
    bidding_started_at = models.DateTimeField(null=True, verbose_name='起拍时间')
    bidding_ended_at = models.DateTimeField(null=True, verbose_name='结束拍卖时间')

    bidding_started_at_data = models.DateField(null=True, verbose_name='产品起拍日期')
    activated_at_data = models.DateField(null=True, verbose_name='产品激活日期')
    product_sum = models.CharField(null=True, max_length=30, verbose_name='订单数量')
    buy_now_orders = models.CharField(null=True, max_length=30, verbose_name='一口价订单')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    # 新增字段
    image_urls = models.TextField(null=True, verbose_name='所有图片')
    product_video_url = models.TextField(null=True, verbose_name='视频链接')
    name_your_price = models.CharField(null=True, max_length=255, verbose_name='议价字段')
    order_type = models.IntegerField(null=True, blank=True, default=9, verbose_name='订单类型')
    cn_user_id = models.CharField(null=True, max_length=30, verbose_name='卖家ID')
    cn_seller_name = models.CharField(null=True, max_length=50, verbose_name='卖家备注名')


class Data_TopData(models.Model):
    """项目数据"""
    lots_id = models.CharField(null=True, max_length=40, verbose_name='标准搜索ID')
    product_parent_id = models.IntegerField(null=True, verbose_name='产品父ID')
    standard_product_id = models.IntegerField(null=True, verbose_name='产品标准ID')
    user_id = models.IntegerField(null=True, verbose_name='用户ID')
    buyer_id = models.IntegerField(null=True, verbose_name='买家ID')
    default_variation_id = models.IntegerField(null=True, verbose_name='缺省变种ID')
    title = models.TextField(null=True, verbose_name='产品标题')
    taxonomy_values_0 = models.CharField(null=True, max_length=40, verbose_name='产品分类0')
    taxonomy_values_1 = models.CharField(null=True, max_length=40, verbose_name='产品分类1')
    taxonomy_values_2 = models.CharField(null=True, max_length=40, verbose_name='产品分类2')
    taxonomy_values_3 = models.CharField(null=True, max_length=40, verbose_name='产品分类3')
    facets = models.TextField(null=True, verbose_name='产品详细参数')
    description = models.TextField(null=True, verbose_name='产品描述')  # 13
    #
    image_urls_0 = models.URLField(null=True, verbose_name='产品详细图片0')
    image_urls_1 = models.URLField(null=True, verbose_name='产品详细图片1')
    image_urls_2 = models.URLField(null=True, verbose_name='产品详细图片2')
    image_urls_3 = models.URLField(null=True, verbose_name='产品详细图片3')
    image_urls_4 = models.URLField(null=True, verbose_name='产品详细图片4')
    image_urls_5 = models.URLField(null=True, verbose_name='产品详细图片5')
    buy_now_price = models.CharField(null=True, max_length=10, verbose_name='一口价')
    retail_price = models.CharField(null=True, max_length=10, verbose_name='零售价')  # 21
    #
    starting_bid_amount = models.IntegerField(null=True, verbose_name='起拍价')
    hammer_price_local = models.FloatField(null=True, verbose_name='本地成交价')
    shipping_price_local = models.FloatField(null=True, verbose_name='本地运费')

    alerts_count = models.IntegerField(null=True, verbose_name='通告次数')
    seller_name = models.CharField(null=True, max_length=50, verbose_name='卖家姓名')
    ratings_count = models.FloatField(null=True, verbose_name='评价数量')
    ratings_average = models.FloatField(null=True, verbose_name='平均评分')
    lot_upsells = models.TextField(null=True, verbose_name='更多销售')  # 29

    bidding_started_at_data = models.DateTimeField(null=True, verbose_name='产品起拍日期')
    activated_at_data = models.DateTimeField(null=True, verbose_name='产品激活日期')
    total_orders = models.IntegerField(null=True, verbose_name='总展示数量')
    valid_orders = models.IntegerField(null=True, verbose_name='成交订单数量')
    bid_orders = models.IntegerField(null=True, verbose_name='竞拍价订单')
    buy_now_orders = models.IntegerField(null=True, verbose_name='一口价订单')  # 35

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')
    # 新增字段
    hammer_order_count = models.IntegerField(null=True, verbose_name='成交数')
    hammer_order_rate = models.CharField(null=True, blank=True, max_length=10, verbose_name='成交率')
    combined_order_count = models.IntegerField(default=0, null=True, verbose_name='合单数')
    combined_order_rate = models.IntegerField(default=0, null=True, verbose_name='合单率')
    buy_now_shipping_price = models.DecimalField(default=0, null=True, blank=True, max_digits=9, decimal_places=1,
                                                 verbose_name='一口价含运费')
    action_price = models.DecimalField(default=0, max_digits=9, decimal_places=1, verbose_name='拍卖成交价')
    image_urls = models.TextField(null=True, blank=True, verbose_name='图片列表')
    product_video_url = models.TextField(null=True, verbose_name='视频链接')
    order_type = models.IntegerField(null=True, blank=True, verbose_name='订单类型')
    module_groupings = models.CharField(null=True, blank=True, max_length=255, verbose_name='V2分类')
    cn_seller_name = models.CharField(null=True, blank=True, max_length=64, verbose_name='备注')
    purchase_url = models.CharField(null=True, blank=True, max_length=255, verbose_name='采购链接')
    profits = models.CharField(null=True, blank=True, max_length=10, verbose_name='退款率')
    cn_user_id = models.CharField(null=True, blank=True, max_length=64, verbose_name='卖家备注')
    site_id = models.CharField(null=True, blank=True, max_length=64, verbose_name='本站ID')
    activated_at = models.DateTimeField(null=True, verbose_name='订单激活日期')


# 一个月数据（搜索一个月内的时间，搜索该表，为了加快搜索时间）
class Data_TopData_month(models.Model):
    """项目数据"""
    lots_id = models.CharField(null=True, max_length=40, verbose_name='标准搜索ID')
    product_parent_id = models.IntegerField(null=True, verbose_name='产品父ID')
    standard_product_id = models.IntegerField(null=True, verbose_name='产品标准ID')
    user_id = models.IntegerField(null=True, verbose_name='用户ID')
    buyer_id = models.IntegerField(null=True, verbose_name='买家ID')
    default_variation_id = models.IntegerField(null=True, verbose_name='缺省变种ID')
    title = models.TextField(null=True, verbose_name='产品标题')
    taxonomy_values_0 = models.CharField(null=True, max_length=40, verbose_name='产品分类0')
    taxonomy_values_1 = models.CharField(null=True, max_length=40, verbose_name='产品分类1')
    taxonomy_values_2 = models.CharField(null=True, max_length=40, verbose_name='产品分类2')
    taxonomy_values_3 = models.CharField(null=True, max_length=40, verbose_name='产品分类3')
    facets = models.TextField(null=True, verbose_name='产品详细参数')
    description = models.TextField(null=True, verbose_name='产品描述')  # 13
    #
    image_urls_0 = models.URLField(null=True, verbose_name='产品详细图片0')
    image_urls_1 = models.URLField(null=True, verbose_name='产品详细图片1')
    image_urls_2 = models.URLField(null=True, verbose_name='产品详细图片2')
    image_urls_3 = models.URLField(null=True, verbose_name='产品详细图片3')
    image_urls_4 = models.URLField(null=True, verbose_name='产品详细图片4')
    image_urls_5 = models.URLField(null=True, verbose_name='产品详细图片5')
    buy_now_price = models.CharField(null=True, max_length=10, verbose_name='一口价')
    retail_price = models.CharField(null=True, max_length=10, verbose_name='零售价')  # 21
    #
    starting_bid_amount = models.IntegerField(null=True, verbose_name='起拍价')
    hammer_price_local = models.FloatField(null=True, verbose_name='本地成交价')
    shipping_price_local = models.FloatField(null=True, verbose_name='本地运费')

    alerts_count = models.IntegerField(null=True, verbose_name='通告次数')
    seller_name = models.CharField(null=True, max_length=50, verbose_name='卖家姓名')
    ratings_count = models.FloatField(null=True, verbose_name='评价数量')
    ratings_average = models.FloatField(null=True, verbose_name='平均评分')
    lot_upsells = models.TextField(null=True, verbose_name='更多销售')  # 29

    bidding_started_at_data = models.DateTimeField(null=True, verbose_name='产品起拍日期')
    activated_at_data = models.DateTimeField(null=True, verbose_name='产品激活日期')
    total_orders = models.IntegerField(null=True, verbose_name='总展示数量')
    valid_orders = models.IntegerField(null=True, verbose_name='成交订单数量')
    bid_oders = models.IntegerField(null=True, verbose_name='竞拍价订单')
    buy_now_oders = models.IntegerField(null=True, verbose_name='一口价订单')  # 35

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')


# 卖家备注名
class CN_seller_name(models.Model):
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    username = models.CharField(default='', max_length=30, verbose_name='用户名')
    CN_user_id = models.CharField(null=True, max_length=30, verbose_name='卖家ID')
    CN_seller_name = models.CharField(null=True, max_length=50, verbose_name='卖家备注名')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')


# 编辑商品名称和品类
class own_product_edit(models.Model):
    USER_ID = models.IntegerField(default=0, verbose_name='用户id')
    username = models.CharField(default='', max_length=30, verbose_name='用户名')
    own_all_standard_product_id = models.CharField(null=True, max_length=30, verbose_name='商品标准ID')
    own_all_product_name = models.CharField(null=True, max_length=100, verbose_name='备注商品名称')
    own_all_product_taxonomy = models.CharField(null=True, max_length=100, verbose_name='备注商品品类')
    own_all_product_price = models.CharField(null=True, max_length=50, verbose_name='备注商品进价')
    own_all_product_weight = models.CharField(null=True, max_length=50, verbose_name='备注商品重量')
    own_all_product_1688addrass = models.CharField(null=True, max_length=500, verbose_name='备注商品1688地址')
    own_all_product_ave_sfb = models.CharField(null=True, max_length=50, verbose_name='备注商品均SFB')
    own_all_product_beizhu = models.CharField(null=True, max_length=1000, verbose_name='备注商品详细信息')
    own_all_product_colloct = models.CharField(null=True, max_length=10, verbose_name='收藏商品')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')


# 数据统计表格
# 销售数量成交价表格
class Table_Sales_amounts(models.Model):
    STAR_DATE = models.DateField(unique=True, null=True, verbose_name='日期')

    product_sum = models.CharField(null=True, max_length=200, verbose_name='总数量')
    bid_oders = models.CharField(null=True, max_length=200, verbose_name='拍卖价数量')
    buy_now_oders = models.CharField(null=True, max_length=200, verbose_name='一口价数量')
    avg_amount = models.CharField(null=True, max_length=200, verbose_name='平均成交价')
    bid_avg_amount = models.CharField(null=True, max_length=200, verbose_name='拍卖价平均成交价')
    buy_now_avg_amount = models.CharField(null=True, max_length=200, verbose_name='一口价平均成交价')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')

    def __str__(self):
        return self.store_name


# 卖家销量表格
class Table_Seller_TOP(models.Model):
    STAR_DATE = models.DateField(unique=True, null=True, verbose_name='日期')
    TIME_KEY = models.CharField(null=True, max_length=200, verbose_name='时间标志')

    seller_name = models.CharField(null=True, max_length=200, verbose_name='卖家名字')
    user_id = models.CharField(null=True, max_length=200, verbose_name='卖家ID')
    product_sum = models.CharField(null=True, max_length=200, verbose_name='总数量')
    avg_amount = models.CharField(null=True, max_length=200, verbose_name='均成交价')
    product_number = models.CharField(null=True, max_length=200, verbose_name='商品种类数量')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')

    def __str__(self):
        return self.store_name


# 标准商品销量表格
class Table_Product_TOP(models.Model):
    STAR_DATE = models.DateField(unique=True, null=True, verbose_name='日期')
    TIME_KEY = models.CharField(null=True, max_length=200, verbose_name='时间标志')

    standard_product_id = models.CharField(null=True, max_length=200, verbose_name='商品ID')
    image_urls_0 = models.CharField(null=True, max_length=200, verbose_name='商品主图')
    product_sum = models.CharField(null=True, max_length=200, verbose_name='总数量')
    avg_amount = models.CharField(null=True, max_length=200, verbose_name='均成交价')
    seller_number = models.CharField(null=True, max_length=200, verbose_name='商品种类数量')

    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='更新数据时间')

    def __str__(self):
        return self.store_name


# 品类情况表格
class The_taxonomy_amount(models.Model):
    STAR_DATE = models.DateField(unique=True, null=True, verbose_name='保存开始日期')
    time_range = models.CharField(null=True, max_length=200, verbose_name='统计时间段标志')
    taxonomy_values = models.CharField(null=True, max_length=200, verbose_name='品类')
    product_sum = models.CharField(null=True, max_length=200, verbose_name='总数量')
    bid_oders = models.CharField(null=True, max_length=200, verbose_name='拍卖价数量')
    buy_now_oders = models.CharField(null=True, max_length=200, verbose_name='一口价数量')
    save_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建数据时间')

    def __str__(self):
        return self.store_name
