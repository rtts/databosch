from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'geassioceerde_persoon']
    def geassioceerde_persoon(self, user):
        print ("persoon van {}: '{}'".format(user.username, user.persoon))
        return mark_safe('<a href="{}">{}</a>'.format(reverse('admin:maakdenbosch_persoon_change', args=[user.persoon.pk]), user.persoon))

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

@admin.register(Webtekst)
class WebtekstAdmin(admin.ModelAdmin):
    list_display = ('plek', 'tekst_truncated')
    def tekst_truncated(self, webtekst):
        s = strip_tags(webtekst.tekst)
        if len(s) > 250:
            s = s[:250] + '...'
        return s
    tekst_truncated.short_description = 'tekst'

class IdeaInline(admin.StackedInline):
    model = Idea
    extra = 0

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ['title', 'word', 'show_mayor', 'show_person']

    def show_mayor(self, idea):
        return mark_safe('<a href="../mayor/{}/change/">{}</a>'.format(idea.mayor.pk, idea.mayor))
    show_mayor.short_description = 'burgermeester'
    show_mayor.admin_order_field = 'mayor'

    def show_person(self, idea):
        return mark_safe('<a href="../../maakdenbosch/persoon/{}/change/">{}</a>'.format(idea.mayor.person.pk, idea.mayor.person))
    show_person.short_description = 'door persoon'
    show_person.admin_order_field = 'mayor__person'


@admin.register(Mayor)
class MayorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'show_person']
    inlines = [IdeaInline]

    def show_person(self, mayor):
        return mark_safe('<a href="../../maakdenbosch/persoon/{}/change/">{}</a>'.format(mayor.person.pk, mayor.person))
    show_person.short_description = 'door persoon'

@admin.register(Bijeenkomst)
class BijeenkomstAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__str__', 'netwerkhouder', 'datum', 'locatie', 'show_personen', 'show_speerpunten')
    list_filter = ('datum', )
    actions = ['export_xls']
    inlines = (DeelnameInline, SpeerpuntInline)
    def show_personen(self, bijeenkomst):
        return ', '.join(['{} ({})'.format(deelname.persoon, deelname.taak) for deelname in bijeenkomst.deelnames.all()])
    show_personen.short_description = 'betrokkenen'
    def show_speerpunten(self, bijeenkomst):
        return ', '.join([speerpunt.beschrijving for speerpunt in bijeenkomst.speerpunten.all()])
    show_speerpunten.short_description = 'speerpunten'

    def export_xls(self, request, queryset):
        import xlwt
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=bijeenkomsten.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Bijeenkomsten")

        row_num = 0

        columns = [
            ('URL', 8000),
            ('Naam Netwerk', 8000),
            ('Netwerkhouder', 8000),
            ('Datum', 8000),
            ('Naam locatie', 8000),
            ('Betrokkenen', 16000),
            ('Speerpunten', 16000),
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        for obj in queryset:
            row_num += 1
            row = [
                'http://mijndenbosch.nl/bijeenkomst/' + str(obj.pk) + '/',
                obj.naam,
                str(obj.netwerkhouder),
                str(obj.datum) + ' ' + str(obj.tijd),
                '{} ({})'.format(obj.locatie, obj.adres),
                self.show_personen(obj),
                self.show_speerpunten(obj),
                ]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    export_xls.short_description = 'Excel Export'

@admin.register(Speerpunt)
class SpeerpuntAdmin(admin.ModelAdmin):
    list_display = ('nummer', 'beschrijving', 'toelichting_truncated', 'bijeenkomst', 'show_ideeen')
    list_display_links = ['beschrijving']
    list_editable = ['nummer']
    list_filter = ('bijeenkomst', )
    inlines = (IdeeInline, )

    def toelichting_truncated(self, speerpunt):
        s = strip_tags(speerpunt.toelichting)
        if len(s) > 500:
            s = s[:500] + '...'
        return s
    toelichting_truncated.short_description = 'toelichting'

    def show_ideeen(self, speerpunt):
        return ', '.join([str(idee.beschrijving) for idee in speerpunt.ideeen.all()])
    show_ideeen.short_description = 'ideeën'

@admin.register(Idee)
class IdeeAdmin(admin.ModelAdmin):
    list_display = ('nummer', 'beschrijving', 'toelichting_truncated', 'show_bijeenkomst', 'show_speerpunt', 'show_personen')
    list_display_links = ['beschrijving']
    list_filter = ['speerpunt__bijeenkomst', 'speerpunt']
    inlines = [OndersteuningInline]

    def show_bijeenkomst(self, idee):
        return idee.speerpunt.bijeenkomst
    show_bijeenkomst.short_description = 'bijeenkomst'

    def show_speerpunt(self, idee):
        return idee.speerpunt.beschrijving
    show_speerpunt.short_description = 'speerpunt'

    def toelichting_truncated(self, idee):
        s = strip_tags(idee.toelichting)
        if len(s) > 500:
            s = s[:500] + '...'
        return s
    toelichting_truncated.short_description = 'toelichting'

    def show_personen(self, idee):
        return ', '.join(["{} ({})".format(str(ond.persoon), ond.rol) for ond in idee.ondersteuningen.all()])
    show_personen.short_description = 'betrokkenen'

@admin.register(Nieuwsbericht)
class NieuwsberichtAdmin(admin.ModelAdmin):
    list_display = ('titel', 'datum')
