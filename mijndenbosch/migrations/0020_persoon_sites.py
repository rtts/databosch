# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('mijndenbosch', '0019_auto_20160607_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='persoon',
            name='sites',
            field=models.ManyToManyField(related_name='personen', to='sites.Site'),
        ),
    ]
