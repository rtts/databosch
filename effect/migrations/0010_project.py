# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 12:23
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0009_partner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='datum')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='foto')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='inhoud')),
            ],
            options={
                'verbose_name_plural': 'Projecten',
                'ordering': ['date'],
            },
        ),
    ]
