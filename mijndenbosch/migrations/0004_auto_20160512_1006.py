# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0003_auto_20160509_1753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bijeenkomst',
            options={'ordering': ['naam'], 'verbose_name': 'netwerk', 'verbose_name_plural': 'netwerken'},
        ),
        migrations.AlterField(
            model_name='taak',
            name='bijeenkomst',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken', to='mijndenbosch.Bijeenkomst', verbose_name='netwerk'),
        ),
    ]
