# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 14:06
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bijeenkomst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255, verbose_name='naam netwerk')),
                ('datum', models.DateField(blank=True, null=True)),
                ('tijd', models.TimeField(blank=True, null=True)),
                ('locatie', models.CharField(blank=True, max_length=255, verbose_name='naam locatie')),
                ('adres', models.TextField(blank=True, verbose_name='adres locatie')),
                ('besloten', models.BooleanField(default=False, verbose_name='dit is een besloten bijeenkomst')),
            ],
            options={
                'verbose_name_plural': 'bijeenkomsten',
                'ordering': ['naam'],
            },
        ),
        migrations.CreateModel(
            name='Idee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beschrijving', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'ideeën',
                'ordering': ['beschrijving'],
            },
        ),
        migrations.CreateModel(
            name='Nieuwsbericht',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField()),
                ('titel', models.CharField(max_length=255)),
                ('inhoud', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'nieuwsberichten',
                'ordering': ['-datum'],
            },
        ),
        migrations.CreateModel(
            name='Persoon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefoonnummer', models.CharField(blank=True, max_length=32)),
                ('beschrijving', ckeditor.fields.RichTextField(blank=True)),
                ('profielfoto', models.ImageField(blank=True, upload_to='')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'personen',
            },
        ),
        migrations.CreateModel(
            name='Speerpunt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('woord', models.CharField(max_length=32, verbose_name='In één woord')),
                ('beschrijving', ckeditor.fields.RichTextField(blank=True)),
                ('bijeenkomst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speerpunten', to='mijndenbosch.Bijeenkomst')),
            ],
            options={
                'verbose_name_plural': 'speerpunten',
                'ordering': ['woord'],
            },
        ),
        migrations.CreateModel(
            name='Taak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
                ('bijeenkomst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken', to='mijndenbosch.Bijeenkomst')),
                ('persoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken', to='mijndenbosch.Persoon')),
            ],
            options={
                'verbose_name_plural': 'taken',
                'ordering': ['naam'],
            },
        ),
        migrations.AddField(
            model_name='idee',
            name='initiatiefnemers',
            field=models.ManyToManyField(blank=True, related_name='initiatiefnemer_van', to='mijndenbosch.Persoon'),
        ),
        migrations.AddField(
            model_name='idee',
            name='kartrekker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kartrekker_van', to='mijndenbosch.Persoon'),
        ),
        migrations.AddField(
            model_name='idee',
            name='speerpunt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ideeen', to='mijndenbosch.Speerpunt'),
        ),
        migrations.AddField(
            model_name='bijeenkomst',
            name='deelnemers',
            field=models.ManyToManyField(blank=True, related_name='deelnemer_at', to='mijndenbosch.Persoon'),
        ),
        migrations.AddField(
            model_name='bijeenkomst',
            name='netwerkhouder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bijeenkomsten', to='mijndenbosch.Persoon'),
        ),
    ]