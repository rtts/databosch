# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-21 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0020_auto_20160621_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='hyperlink',
            name='type',
        ),
        migrations.RemoveField(
            model_name='organisatiehyperlink',
            name='type',
        ),
    ]