# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0003_project_lange_beschrijving'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisatie',
            name='doelgroepen',
            field=models.ManyToManyField(blank=True, to='maakdenbosch.Doelgroep'),
        ),
        migrations.AddField(
            model_name='organisatie',
            name='logo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='organisatie',
            name='tags',
            field=models.ManyToManyField(blank=True, to='maakdenbosch.Tag'),
        ),
    ]
