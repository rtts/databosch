# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-07 17:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0039_auto_20161207_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bijeenkomst',
            name='slug',
        ),
    ]
