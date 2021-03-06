# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-30 09:55
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0017_auto_20160520_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webtekst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plek', models.IntegerField(choices=[(1, 'Homepage 1'), (2, 'Homepage 2'), (10, 'Aboutpage 1'), (11, 'Aboutpage 2'), (12, 'Aboutpage 3'), (20, 'Aanmelden puntenlijst 1'), (21, 'Aanmelden puntenlijst 2'), (22, 'Aanmelden puntenlijst 3'), (23, 'Aanmelden puntenlijst 4'), (30, 'Aanmelden stap 3'), (31, 'Aanmelden stap 4'), (40, 'Burgermeesters galerij'), (50, 'Initiatieven pagina')], unique=True)),
                ('tekst', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'personen',
                'ordering': ['plek'],
            },
        ),
        migrations.AlterModelOptions(
            name='bijeenkomst',
            options={'ordering': ['-datum', '-pk'], 'verbose_name_plural': 'bijeenkomsten'},
        ),
    ]
