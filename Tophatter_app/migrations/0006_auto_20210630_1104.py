# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-06-30 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tophatter_app', '0005_campaign_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign_list',
            name='name',
            field=models.CharField(max_length=30, null=True, verbose_name='campaign名称'),
        ),
        migrations.AlterField(
            model_name='campaign_list',
            name='status',
            field=models.CharField(max_length=30, null=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='campaign_list',
            name='type',
            field=models.CharField(max_length=30, null=True, verbose_name='类型'),
        ),
    ]