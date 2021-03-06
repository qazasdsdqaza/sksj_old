# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-06-13 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('five_miles_app', '0008_auto_20200613_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders_date_5miles',
            name='country',
            field=models.CharField(max_length=200, null=True, verbose_name='买家国家'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='goods_main_image_url',
            field=models.CharField(max_length=200, null=True, verbose_name='商品主图'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='goods_name',
            field=models.CharField(max_length=200, null=True, verbose_name='商品名称'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='sku_no',
            field=models.CharField(max_length=200, null=True, verbose_name='SKU名字'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='status_Approved',
            field=models.CharField(max_length=200, null=True, verbose_name='订单状态1'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='status_Canceled',
            field=models.CharField(max_length=200, null=True, verbose_name='订单状态5'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='status_Closed',
            field=models.CharField(max_length=200, null=True, verbose_name='订单状态6'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='status_Completed',
            field=models.CharField(max_length=200, null=True, verbose_name='订单状态3'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='status_Dispatched',
            field=models.CharField(max_length=200, null=True, verbose_name='订单状态2'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='status_Refunded',
            field=models.CharField(max_length=200, null=True, verbose_name='订单状态4'),
        ),
        migrations.AddField(
            model_name='orders_date_5miles',
            name='tracking_no',
            field=models.CharField(max_length=200, null=True, verbose_name='运单号'),
        ),
    ]
