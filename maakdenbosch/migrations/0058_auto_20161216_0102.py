# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-16 00:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0057_auto_20161208_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entiteit',
            name='slug',
            field=models.SlugField(blank=True, help_text='Dit netwerk is te bezoeken op mijndenbosch.nl/netwerk/[watjijhierinvult]/', null=True, unique=True, verbose_name='url'),
        ),
    ]
