# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-13 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0041_bijeenkomst_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='nieuwsbericht',
            name='foto',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
