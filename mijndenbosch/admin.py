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
    list_display = ['title', 'word', 'show_mayor', 'show_person', 'show_entity']

    def show_mayor(self, idea):
        return mark_safe('<a href="../mayor/{}/change/">{}</a>'.format(idea.mayor.pk, idea.mayor))
    show_mayor.short_description = 'burgermeester'
    show_mayor.admin_order_field = 'mayor'

    def show_person(self, idea):
        if idea.mayor.person:
            return mark_safe('<a href="../../maakdenbosch/persoon/{}/change/">{}</a>'.format(idea.mayor.person.pk, idea.mayor.person))
        else:
            return '-'
    show_person.short_description = 'door persoon'
    show_person.admin_order_field = 'mayor__person'

    def show_entity(self, idea):
        if idea.mayor.meeting and idea.mayor.meeting.entity:
            return mark_safe('<a href="../../maakdenbosch/persoon/{}/change/">{}</a>'.format(idea.mayor.meeting.entity.pk, idea.mayor.meeting.entity))
        else:
            return '-'
    show_entity.short_description = 'door entiteit'
    show_entity.admin_order_field = 'mayor__meeting__entity'


@admin.register(Mayor)
class MayorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'show_person', 'visible']
    inlines = [IdeaInline]

    def show_person(self, mayor):
        if mayor.person:
            return mark_safe('<a href="../../maakdenbosch/persoon/{}/change/">{}</a>'.format(mayor.person.pk, mayor.person))
        else:
            return '-'
    show_person.short_description = 'door persoon'

@admin.register(Bijeenkomst)
class BijeenkomstAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__str__', 'show_entity', 'show_netwerkhouder', 'datum', 'locatie', 'show_url', 'show_personen')
    list_filter = ('datum', )
    readonly_fields = ['naam', 'netwerkhouder', 'burgermeester', 'foto']
    #actions = ['export_xls']
    inlines = (DeelnameInline, SpeerpuntInline)

    def show_url(self, obj):
        if obj.besloten:
            return '(besloten)'
        if obj.slug:
            return mark_safe('<a href="http://mijndenbosch.nl/{slug}/">/{slug}</a>'.format(slug=obj.slug))
        else:
            return mark_safe('<a href="http://mijndenbosch.nl/bijeenkomst/{pk}/">/bijeenkomst/{pk}</a>'.format(pk=obj.pk))
    show_url.short_description = 'URL'

    def show_entity(self, obj):
        if obj.entity:
            return mark_safe('<a href="../../maakdenbosch/entiteit/{}/change/">{}</a>'.format(obj.entity.pk, obj.entity.titel))
        else:
            return '-'
    show_entity.short_description = 'entiteit'

    def show_netwerkhouder(self, obj):
        if obj.entity:
            role, created = Rol.objects.get_or_create(naam='netwerkhouder')
            netwerkhouder = Persoon.objects.filter(entiteit_participaties__entiteit=obj.entity, entiteit_participaties__rol=role).first()
            if netwerkhouder:
                return mark_safe('<a href="../../maakdenbosch/persoon/{pk}/change/">{naam}</a>'.format(pk=netwerkhouder.pk, naam=netwerkhouder))
            else:
                return '-'
        elif obj.netwerkhouder:
            return mark_safe('<a href="../../maakdenbosch/persoon/{pk}/change/">{naam}</a>'.format(pk=obj.netwerkhouder.pk, naam=obj.netwerkhouder))
        else:
            return '-'
    show_netwerkhouder.short_description = 'netwerkhouder'

    def show_personen(self, bijeenkomst):
        return ', '.join(['{} ({})'.format(deelname.persoon, deelname.taak) for deelname in bijeenkomst.deelnames.all()])
    show_personen.short_description = 'betrokkenen'

    # def export_xls(self, request, queryset):
    #     import xlwt
    #     response = HttpResponse(content_type='application/ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename=bijeenkomsten.xls'
    #     wb = xlwt.Workbook(encoding='utf-8')
    #     ws = wb.add_sheet("Bijeenkomsten")

    #     row_num = 0

    #     columns = [
    #         ('URL', 8000),
    #         ('Naam Netwerk', 8000),
    #         ('Netwerkhouder', 8000),
    #         ('Datum', 8000),
    #         ('Naam locatie', 8000),
    #         ('Betrokkenen', 16000),
    #         ('Speerpunten', 16000),
    #     ]

    #     font_style = xlwt.XFStyle()
    #     font_style.font.bold = True

    #     for col_num in range(len(columns)):
    #         ws.write(row_num, col_num, columns[col_num][0], font_style)
    #         # set column width
    #         ws.col(col_num).width = columns[col_num][1]

    #     font_style = xlwt.XFStyle()
    #     font_style.alignment.wrap = 1

    #     for obj in queryset:
    #         row_num += 1
    #         row = [
    #             'http://mijndenbosch.nl/bijeenkomst/' + str(obj.pk) + '/',
    #             obj.naam,
    #             str(obj.netwerkhouder),
    #             str(obj.datum) + ' ' + str(obj.tijd),
    #             '{} ({})'.format(obj.locatie, obj.adres),
    #             self.show_personen(obj),
    #             self.show_speerpunten(obj),
    #             ]
    #         for col_num in range(len(row)):
    #             ws.write(row_num, col_num, row[col_num], font_style)

    #     wb.save(response)
    #     return response
    # export_xls.short_description = 'Excel Export'

@admin.register(Nieuwsbericht)
class NieuwsberichtAdmin(admin.ModelAdmin):
    list_display = ('titel', 'datum')
