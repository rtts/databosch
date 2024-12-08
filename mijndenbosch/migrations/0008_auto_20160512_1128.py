# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0007_auto_20160512_1121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bijeenkomst',
            options={'ordering': ['datum'], 'verbose_name_plural': 'bijeenkomsten'},
        ),
        migrations.AlterModelOptions(
            name='persoon',
            options={'ordering': ['achternaam'], 'verbose_name_plural': 'personen'},
        ),
        migrations.AlterModelOptions(
            name='taak',
            options={'ordering': ['pk'], 'verbose_name_plural': 'taken'},
        ),
        migrations.RemoveField(
            model_name='persoon',
            name='naam',
        ),
        migrations.AddField(
            model_name='persoon',
            name='achternaam',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='persoon',
            name='voornaam',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]