# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-06-25 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PruAndLog', '0006_auto_20210625_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='key_parameter',
            name='USER_ID',
            field=models.IntegerField(default=0, verbose_name='用户id'),
        ),
    ]