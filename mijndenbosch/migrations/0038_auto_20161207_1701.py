# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-07 16:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0037_auto_20161207_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bijeenkomst',
            name='netwerkhouder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bijeenkomsten', to='maakdenbosch.Persoon'),
        ),
    ]