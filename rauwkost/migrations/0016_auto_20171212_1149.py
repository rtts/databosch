# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-12 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0015_auto_20171211_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='afbeelding'),
        ),
        migrations.AlterField(
            model_name='config',
            name='parameter',
            field=models.PositiveIntegerField(choices=[(10, 'Footer HTML'), (20, 'Pagina header')], unique=True),
        ),
    ]
