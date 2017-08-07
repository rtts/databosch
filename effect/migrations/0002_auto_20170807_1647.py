# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-07 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='afbeelding')),
                ('hyperlink', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='section',
            name='color',
            field=models.PositiveIntegerField(choices=[(1, 'Wit'), (2, 'Oranje'), (3, 'Groen')], default=1, verbose_name='kleur'),
        ),
        migrations.AddField(
            model_name='section',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Normaal'), (2, 'Video'), (3, 'Nieuws'), (4, 'Projecten'), (5, 'Partners'), (6, 'Minisectie')], default=1, verbose_name='soort sectie'),
        ),
    ]
