# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-15 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('five_miles_app', '0005_auto_20200515_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='store_cookie_5miles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=30, null=True, verbose_name='店铺名称')),
                ('store_cookie', models.CharField(max_length=10000, null=True, verbose_name='店铺cookie')),
            ],
        ),
    ]
