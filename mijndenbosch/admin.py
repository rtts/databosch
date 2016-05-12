from django.contrib import admin
from .models import *

class SpeerpuntInline(admin.StackedInline):
    model = Speerpunt
    extra = 1

class IdeeInline(admin.StackedInline):
    model = Idee
    extra = 1

class DeelnameInline(admin.StackedInline):
    model = Deelname
    extra = 1

class OndersteuningInline(admin.StackedInline):
    model = Ondersteuning
    extra = 1

@admin.register(Taak)
class TaakAdmin(admin.ModelAdmin):
    pass

@admin.register(Deelname)
class DeelnameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'taak', 'persoon', 'bijeenkomst')
    list_filter = ('taak', 'persoon', 'bijeenkomst')

@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    list_display = ('voornaam', 'achternaam', 'email', 'geassocieerde_gebruiker')
    list_filter = ['deelnames__bijeenkomst']
    def geassocieerde_gebruiker(self, persoon):
        return persoon.user or '[geen]'

@admin.register(Bijeenkomst)
class BijeenkomstAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'netwerkhouder', 'datum', 'locatie', 'show_personen', 'show_speerpunten')
    list_filter = ('datum', )
    inlines = (DeelnameInline, SpeerpuntInline)
    def show_personen(self, bijeenkomst):
        return ', '.join(['{} ({})'.format(deelname.persoon, deelname.taak) for deelname in bijeenkomst.deelnames.all()])
    show_personen.short_description = 'betrokkenen'
    def show_speerpunten(self, bijeenkomst):
        return ', '.join([str(speerpunt) for speerpunt in bijeenkomst.speerpunten.all()])
    show_speerpunten.short_description = 'speerpunten'

@admin.register(Speerpunt)
class SpeerpuntAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'beschrijving_truncated', 'bijeenkomst', 'show_ideeen')
    list_filter = ('bijeenkomst', )
    inlines = (IdeeInline, )

    def beschrijving_truncated(self, speerpunt):
        s = strip_tags(speerpunt.beschrijving)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    beschrijving_truncated.short_description = 'beschrijving'

    def show_ideeen(self, speerpunt):
        return ', '.join([str(idee) for idee in speerpunt.ideeen.all()])
    show_ideeen.short_description = 'ideeën'

@admin.register(Idee)
class IdeeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'beschrijving', 'toelichting_truncated', 'speerpunt', 'show_personen')
    list_filter = ('speerpunt', 'speerpunt__bijeenkomst' )
    inlines = [OndersteuningInline]

    def toelichting_truncated(self, idee):
        s = strip_tags(idee.toelichting)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    toelichting_truncated.short_description = 'toelichting'

    def show_personen(self, idee):
        return ', '.join([str(deelname.persoon) for deelname in idee.deelnames.all()])
    show_personen.short_description = 'betrokkenen'

@admin.register(Nieuwsbericht)
class NieuwsberichtAdmin(admin.ModelAdmin):
    list_display = ('titel', 'datum')
