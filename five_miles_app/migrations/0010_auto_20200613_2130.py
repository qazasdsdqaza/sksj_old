# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-06-13 21:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('five_miles_app', '0009_auto_20200613_2113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders_date_5miles',
            old_name='orders_id',
            new_name='order_id',
        ),
        migrations.RemoveField(
            model_name='orders_date_5miles',
            name='fulfillment_partner',
        ),
    ]
