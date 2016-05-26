# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 08:06
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0004_auto_20160512_1006'),
        ('maakdenbosch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisatie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
                ('emailadres', models.EmailField(blank=True, max_length=254)),
                ('bezoekadres', models.TextField(blank=True)),
                ('beschrijving', ckeditor.fields.RichTextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participatie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisatie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participaties', to='maakdenbosch.Organisatie')),
                ('persoon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participaties', to='mijndenbosch.Persoon')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name_plural': 'rollen',
            },
        ),
        migrations.RenameField(
            model_name='project',
            old_name='omschrijving',
            new_name='korte_beschrijving',
        ),
        migrations.AddField(
            model_name='participatie',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participaties', to='maakdenbosch.Project'),
        ),
        migrations.AddField(
            model_name='participatie',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.Rol'),
        ),
    ]