# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_id',
            field=models.CharField(default=b'', max_length=40),
        ),
    ]