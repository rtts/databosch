# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-15 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0042_nieuwsbericht_foto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='idea',
            options={'ordering': ['number', 'mayor'], 'verbose_name': 'speerpunt', 'verbose_name_plural': 'speerpunten'},
        ),
        migrations.AddField(
            model_name='mayor',
            name='visible',
            field=models.BooleanField(default=False, help_text='BurgeRmeesters die door anonieme bezoekers worden aangemeld zijn standaard niet zichtbaar op Mijndenbosch.nl', verbose_name='zichtbaar op de website'),
        ),
    ]