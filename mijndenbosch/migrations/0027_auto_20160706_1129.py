# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-06 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0026_auto_20160623_1432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='idee',
            options={'ordering': ['nummer', 'speerpunt'], 'verbose_name_plural': 'ideeën'},
        ),
        migrations.AlterModelOptions(
            name='speerpunt',
            options={'ordering': ['nummer', 'bijeenkomst'], 'verbose_name_plural': 'speerpunten'},
        ),
        migrations.AddField(
            model_name='idee',
            name='nummer',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='speerpunt',
            name='nummer',
            field=models.PositiveIntegerField(default=0),
        ),
    ]