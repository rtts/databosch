# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-27 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0034_auto_20160627_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='groep',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.TagGroep'),
            preserve_default=False,
        ),
    ]
