# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-07 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0036_auto_20161207_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bijeenkomst',
            name='naam',
            field=models.CharField(blank=True, max_length=255, verbose_name='naam netwerk'),
        ),
        migrations.AlterField(
            model_name='bijeenkomst',
            name='slug',
            field=models.SlugField(blank=True, help_text='Deze bijeenkomst is te bezoeken op mijndenbosch.nl/[watjijhierinvult]/', verbose_name='url'),
        ),
    ]