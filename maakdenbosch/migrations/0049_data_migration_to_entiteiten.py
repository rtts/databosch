# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-02 11:37
from __future__ import unicode_literals

from django.db import migrations

def entitize(obj, naam, soort, klass):
    ent = klass(
        soort = soort,
        titel = naam,
        logo = obj.logo,
        tagline = obj.tagline,
        beschrijving = obj.beschrijving,
        emailadres = obj.emailadres,
        locatie_naam = obj.locatie_naam,
        bezoekadres = obj.bezoekadres,
        opgericht = obj.opgericht,
        gewijzigd = obj.gewijzigd,
        aangemaakt = obj.aangemaakt,
    )
    ent.save()
    ent.tags.set(obj.tags.all())
    return ent

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Project = apps.get_model('maakdenbosch', 'Project')
    Organisatie = apps.get_model('maakdenbosch', 'Organisatie')
    Participatie = apps.get_model('maakdenbosch', 'Participatie')
    Persoon = apps.get_model('maakdenbosch', 'Persoon')
    Entiteit = apps.get_model('maakdenbosch', 'Entiteit')
    Entiteitsoort = apps.get_model('maakdenbosch', 'Entiteitsoort')
    EntiteitRelatie = apps.get_model('maakdenbosch', 'EntiteitRelatie')
    Relatiesoort = apps.get_model('maakdenbosch', 'Relatiesoort')
    EntiteitHyperlink = apps.get_model('maakdenbosch', 'EntiteitHyperlink')
    EntiteitFoto = apps.get_model('maakdenbosch', 'EntiteitFoto')
    SiteEntiteit = apps.get_model('maakdenbosch', 'SiteEntiteit')
    EntiteitParticipatie = apps.get_model('maakdenbosch', 'EntiteitParticipatie')

    projectsoort, _ = Entiteitsoort.objects.get_or_create(naam='project')
    organisatiesoort, _ = Entiteitsoort.objects.get_or_create(naam='organisatie')

    for obj in Project.objects.all():
        ent = entitize(obj, obj.titel, projectsoort, Entiteit)

        for h in obj.hyperlinks.all():
            EntiteitHyperlink(
                type = h.type,
                url = h.url,
                entiteit = ent,
            ).save()

        for f in obj.projectfoto_set.all():
            EntiteitFoto(
                bestand = f.bestand,
                entiteit = ent,
            ).save()

        for s in obj.siteprojects.all():
            SiteEntiteit(
                site = s.site,
                entiteit = ent,
                tagline = s.tagline,
                beschrijving = s.beschrijving,
                actief = s.actief,
            ).save()

    for obj in Organisatie.objects.all():
        ent = entitize(obj, obj.naam, organisatiesoort, Entiteit)

        for h in obj.hyperlinks.all():
            EntiteitHyperlink(
                type = h.type,
                url = h.url,
                entiteit = ent,
            ).save()

        for f in obj.organisatiefoto_set.all():
            EntiteitFoto(
                bestand = f.bestand,
                entiteit = ent,
            ).save()

        for s in obj.site_organisaties.all():
            SiteEntiteit(
                site = s.site,
                entiteit = ent,
                tagline = s.tagline,
                beschrijving = s.beschrijving,
                actief = s.actief,
            ).save()

    for p in Participatie.objects.all():
        if p.persoon and p.organisatie:
            ent = Entiteit.objects.filter(titel=p.organisatie.naam, soort=organisatiesoort).first()
            EntiteitParticipatie(
                rol = p.rol,
                persoon = p.persoon,
                email = p.email,
                entiteit = ent,
            ).save()
        elif p.persoon and p.project:
            try:
                ent = Entiteit.objects.filter(titel=p.project.titel, soort=projectsoort).first()
            except:
                raise ValueError(p.project.titel)
            EntiteitParticipatie(
                rol = p.rol,
                persoon = p.persoon,
                email = p.email,
                entiteit = ent,
            ).save()
        elif p.project and p.organisatie:
            van_ent = Entiteit.objects.filter(titel=p.organisatie.naam, soort=organisatiesoort).first()
            naar_ent = Entiteit.objects.filter(titel=p.project.titel, soort=projectsoort).first()
            soort, _ = Relatiesoort.objects.get_or_create(naam=p.rol.naam)
            EntiteitRelatie(
                soort = soort,
                van_entiteit = van_ent,
                naar_entiteit = naar_ent,
            ).save()
        elif p.project and p.email:
            persoon = Persoon(email=p.email)
            persoon.save()
            ent = Entiteit.objects.filter(titel=p.project.titel, soort=projectsoort).first()
            EntiteitParticipatie(
                rol = p.rol,
                persoon = persoon,
                entiteit = ent,
            ).save()
        elif p.organisatie and p.email:
            persoon = Persoon(email=p.email)
            persoon.save()
            ent = Entiteit.objects.filter(titel=p.organisatie.naam, soort=organisatiesoort).first()
            EntiteitParticipatie(
                rol = p.rol,
                persoon = persoon,
                entiteit = ent,
            ).save()
        else:
            raise ValueError(
                '''Well, honestly, this is just not possible. Participaties always have two of the following three foreign keys populated: persoon, project, organisatie. Right now, we've encountered a Participatie object that doesn't follow this rule:
rol = "{}"
persoon = "{}"
project = "{}"
organisatie = "{}"
'''.format(str(p.rol), str(p.persoon), str(p.project), str(p.organisatie)))

class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0048_auto_20160802_1337'),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
