# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0025_auto_20160621_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webtekst',
            name='plek',
            field=models.IntegerField(choices=[(1, 'Homepage 1'), (2, 'Homepage 2'), (10, 'Aboutpage 1'), (11, 'Aboutpage 2'), (12, 'Aboutpage 3'), (20, 'Aanmelden puntenlijst 1'), (21, 'Aanmelden puntenlijst 2'), (22, 'Aanmelden puntenlijst 3'), (23, 'Aanmelden puntenlijst 4'), (30, 'Aanmelden stap 3'), (31, 'Aanmelden stap 4'), (40, 'Burgermeesters galerij'), (50, 'Initiatieven pagina'), (100, 'Email na het aanmelden')], unique=True),
        ),
    ]
