# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-11 15:23
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0011_program_ticketlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='inhoud'),
        ),
        migrations.AlterField(
            model_name='config',
            name='parameter',
            field=models.PositiveIntegerField(choices=[(10, 'Footer HTML')]),
        ),
    ]