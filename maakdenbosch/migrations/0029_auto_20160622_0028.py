# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-21 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0028_auto_20160621_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisatie',
            name='tagline',
            field=models.TextField(blank=True),
        ),
    ]
