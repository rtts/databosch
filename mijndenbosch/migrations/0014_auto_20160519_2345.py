# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0013_auto_20160519_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speerpunt',
            name='beschrijving',
            field=models.CharField(max_length=255),
        ),
    ]
