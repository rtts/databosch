# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-07 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('de_locatie', '0006_auto_20170807_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.Entiteit', verbose_name='partner'),
        ),
    ]
