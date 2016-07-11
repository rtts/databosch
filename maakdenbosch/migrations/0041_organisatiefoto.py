# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-11 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0040_auto_20160711_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisatieFoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bestand', models.ImageField(upload_to='')),
                ('organisatie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.Organisatie')),
            ],
            options={
                'verbose_name_plural': 'foto’s',
            },
        ),
    ]
