# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-22 13:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0056_auto_20161122_1435'),
        ('mijndenbosch', '0030_auto_20160810_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, verbose_name='nummer')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('description', models.TextField(verbose_name='beschrijving')),
                ('word', models.CharField(max_length=255, verbose_name='in één woord')),
            ],
            options={
                'ordering': ['number', 'mayor'],
            },
        ),
        migrations.CreateModel(
            name='Mayor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
                ('photo', models.ImageField(upload_to='', verbose_name='foto')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mayors', to='maakdenbosch.Persoon', verbose_name='persoon')),
            ],
        ),
        migrations.AddField(
            model_name='idea',
            name='mayor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ideas', to='mijndenbosch.Mayor'),
        ),
    ]