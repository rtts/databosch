# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-15 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0020_project_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255, verbose_name='onndertitel'),
        ),
    ]
