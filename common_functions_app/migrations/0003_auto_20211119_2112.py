# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-11-19 21:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_functions_app', '0002_auto_20211119_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data_topdata',
            name='bid_order_count',
        ),
        migrations.RemoveField(
            model_name='data_topdata',
            name='buy_now_order_count',
        ),
        migrations.RemoveField(
            model_name='data_topdata',
            name='buy_now_rate',
        ),
        migrations.RemoveField(
            model_name='data_topdata',
            name='hammer_price',
        ),
    ]
