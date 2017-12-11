# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-11 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0012_auto_20171211_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='content',
            field=models.TextField(blank=True, verbose_name='inhoud'),
        ),
        migrations.AlterField(
            model_name='config',
            name='parameter',
            field=models.PositiveIntegerField(choices=[(10, 'Footer HTML')], unique=True),
        ),
    ]
