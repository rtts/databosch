# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-02 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0043_auto_20160802_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='entiteit',
            name='participaties',
            field=models.ManyToManyField(related_name='entiteiten', through='maakdenbosch.EntiteitParticipatie', to='maakdenbosch.Persoon'),
        ),
    ]
