# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 10:21
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0006_socialmedia_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='datum')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('slug', models.SlugField()),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='inhoud')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Nieuwsbericht',
                'verbose_name_plural': 'Nieuwsberichten',
            },
        ),
    ]