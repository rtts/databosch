# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-07 14:15
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('de_locatie', '0002_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='datum')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='afbeelding')),
                ('contents', ckeditor.fields.RichTextField(blank=True, verbose_name='inhoud')),
            ],
            options={
                'verbose_name_plural': 'Nieuwsberichten',
                'ordering': ['-date'],
                'verbose_name': 'Nieuwsbericht',
            },
        ),
    ]
