# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 12:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('magazines', '0006_auto_20161103_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='subscription_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 3, 12, 45, 17, 172000, tzinfo=utc)),
        ),
    ]
