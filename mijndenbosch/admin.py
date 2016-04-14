from django.contrib import admin
from .models import *

class SpeerpuntInline(admin.StackedInline):
    model = Speerpunt
    extra = 0

@admin.register(Bijeenkomst)
class BijeenkomstAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'datum', 'adres', 'organisator', 'show_speerpunten')
    list_filter = ('datum', )
    inlines = (SpeerpuntInline, )
    def show_speerpunten(self, bijeenkomst):
        return ', '.join([str(speerpunt) for speerpunt in bijeenkomst.speerpunten.all()])
    show_speerpunten.short_description = 'speerpunten'

class IdeeInline(admin.StackedInline):
    model = Idee
    extra = 0

@admin.register(Speerpunt)
class SpeerpuntAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'beschrijving', 'bijeenkomst', 'show_ideeen')
    list_filter = ('bijeenkomst', )
    inlines = (IdeeInline, )
    def show_ideeen(self, speerpunt):
        return ', '.join([str(idee) for idee in speerpunt.ideeen.all()])
    show_ideeen.short_description = 'ideeën'

@admin.register(Idee)
class IdeeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'speerpunt', 'show_deelnemers')
    list_filter = ('speerpunt', 'speerpunt__bijeenkomst' )
    def show_deelnemers(self, idee):
        return ', '.join([str(user) for user in idee.deelnemers.all()])
    show_deelnemers.short_description = 'deelnemers'
