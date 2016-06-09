# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 14:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0008_auto_20160607_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='korte_beschrijving',
        ),
        migrations.AlterField(
            model_name='siteproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siteprojects', to='maakdenbosch.Project'),
        ),
        migrations.AlterField(
            model_name='siteproject',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siteprojects', to='sites.Site'),
        ),
    ]
