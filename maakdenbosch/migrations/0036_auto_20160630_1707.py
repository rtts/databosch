# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-30 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def migrate_doelgroepen(*args, **kwargs):
    from maakdenbosch.models import Project, Organisatie, Tag, TagGroep, Doelgroep
    print('Migrating doelgroepen to TagGroep "Doelgroepen"')
    (g, _) = TagGroep.objects.get_or_create(naam='Doelgroepen')
    for p in Project.objects.all():
        for d in p.doelgroepen.all():
            (t, _) = Tag.objects.get_or_create(naam=d.naam, groep=g)
            p.tags.add(t)
    for o in Organisatie.objects.all():
        for d in p.doelgroepen.all():
            (t, _) = Tag.objects.get_or_create(naam=d.naam, groep=g)
            o.tags.add(t)
    Doelgroep.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0035_auto_20160627_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='groep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='maakdenbosch.TagGroep'),
        ),
        migrations.RunPython(migrate_doelgroepen),
    ]
