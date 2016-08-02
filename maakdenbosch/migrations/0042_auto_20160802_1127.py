# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-02 09:27
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('maakdenbosch', '0041_organisatiefoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entiteit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, upload_to='')),
                ('tagline', models.TextField(blank=True)),
                ('beschrijving', ckeditor.fields.RichTextField(blank=True)),
                ('emailadres', models.EmailField(blank=True, max_length=254)),
                ('telefoonnummer', models.CharField(blank=True, max_length=255)),
                ('locatie_naam', models.CharField(blank=True, max_length=255)),
                ('bezoekadres', models.TextField(blank=True)),
                ('opgericht', models.DateField(blank=True, null=True)),
                ('gewijzigd', models.DateTimeField(auto_now=True)),
                ('aangemaakt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'entiteiten',
                'ordering': ['titel'],
            },
        ),
        migrations.CreateModel(
            name='EntiteitHyperlink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('entiteit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hyperlinks', to='maakdenbosch.Entiteit')),
            ],
            options={
                'verbose_name': 'hyperlink',
            },
        ),
        migrations.CreateModel(
            name='EntiteitParticipatie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('entiteit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entiteit_participaties', to='maakdenbosch.Entiteit')),
                ('persoon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entiteit_participaties', to='maakdenbosch.Persoon')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.Rol')),
            ],
        ),
        migrations.CreateModel(
            name='EntiteitRelatie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naar_entiteit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='naar_entiteiten', to='maakdenbosch.Entiteit')),
            ],
        ),
        migrations.CreateModel(
            name='Entiteitsoort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'entiteitsoorten',
                'ordering': ['naam'],
            },
        ),
        migrations.CreateModel(
            name='Relatiesoort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'relatiesoorten',
                'ordering': ['naam'],
            },
        ),
        migrations.CreateModel(
            name='SiteEntiteit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.TextField(blank=True)),
                ('beschrijving', ckeditor.fields.RichTextField(blank=True)),
                ('actief', models.BooleanField(default=True)),
                ('entiteit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_entiteiten', to='maakdenbosch.Entiteit')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_entiteiten', to='sites.Site')),
            ],
            options={
                'verbose_name': 'site-specifieke beschrijving',
                'verbose_name_plural': 'site-specifieke beschrijvingen',
            },
        ),
        migrations.AlterModelOptions(
            name='linktype',
            options={'ordering': ['type']},
        ),
        migrations.AddField(
            model_name='entiteitrelatie',
            name='soort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.Relatiesoort'),
        ),
        migrations.AddField(
            model_name='entiteitrelatie',
            name='van_entiteit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='van_entiteiten', to='maakdenbosch.Entiteit'),
        ),
        migrations.AddField(
            model_name='entiteithyperlink',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.LinkType'),
        ),
        migrations.AddField(
            model_name='entiteit',
            name='sites',
            field=models.ManyToManyField(related_name='entiteiten', through='maakdenbosch.SiteEntiteit', to='sites.Site'),
        ),
        migrations.AddField(
            model_name='entiteit',
            name='soort',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.Entiteitsoort'),
        ),
        migrations.AddField(
            model_name='entiteit',
            name='tags',
            field=models.ManyToManyField(blank=True, to='maakdenbosch.Tag'),
        ),
    ]
