# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-16 00:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0043_auto_20161215_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='idea',
            options={'ordering': ['number', 'mayor'], 'verbose_name': 'idee', 'verbose_name_plural': 'ideeën'},
        ),
    ]