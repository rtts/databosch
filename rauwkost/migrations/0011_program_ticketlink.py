# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-11 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0010_auto_20171211_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='ticketlink',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
