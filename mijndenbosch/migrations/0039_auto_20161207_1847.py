# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-07 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mijndenbosch', '0038_auto_20161207_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bijeenkomst',
            name='burgermeester',
            field=models.CharField(blank=True, help_text='NIET MEER GEBRUIKEN. De burgermeesters staan nu in hun eigen tabel.', max_length=255, verbose_name='naam burgermeester'),
        ),
        migrations.AlterField(
            model_name='bijeenkomst',
            name='foto',
            field=models.ImageField(blank=True, help_text='NIET MEER GEBRUIKEN. De burgermeestersfoto staat in de burgermeesterstabel', upload_to=''),
        ),
        migrations.AlterField(
            model_name='bijeenkomst',
            name='naam',
            field=models.CharField(blank=True, help_text='NIET MEER GEBRUIKEN. De naam van het netwerk is nu de titel van de entiteit', max_length=255, verbose_name='naam netwerk'),
        ),
        migrations.AlterField(
            model_name='bijeenkomst',
            name='netwerkhouder',
            field=models.ForeignKey(blank=True, help_text='NIET MEER GEBRUIKEN. De netwerkhouder is nu de persoon die als "netwerkhouder" participeert in de entiteit', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bijeenkomsten', to='maakdenbosch.Persoon'),
        ),
    ]
