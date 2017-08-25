# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0008_auto_20170825_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
                ('logo', models.ImageField(upload_to='')),
                ('url', models.URLField()),
            ],
        ),
    ]
