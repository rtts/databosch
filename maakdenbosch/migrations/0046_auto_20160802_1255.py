# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-02 10:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0045_auto_20160802_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entiteitparticipatie',
            name='entiteit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participaties', to='maakdenbosch.Entiteit'),
        ),
    ]
