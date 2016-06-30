# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-27 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0031_auto_20160627_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagGroep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['naam'],
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='groep',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.TagGroep'),
        ),
    ]