# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-06-29 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PruAndLog', '0008_warehouse_show_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse_show_data',
            name='date_time',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='创建数据时间'),
        ),
    ]