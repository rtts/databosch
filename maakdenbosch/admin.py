from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from .models import *
from mijndenbosch.models import Persoon

# @admin.register(Persoon)
# class PersoonAdmin(admin.ModelAdmin):
#     list_display = ('naam', 'actief_als')
#     list_filter = ('participaties__rol', )

#     def actief_als(self, user):
#         return ', '.join(['{} bij {}'.format(p.rol, p.project) for p in user.participaties.all()])

@admin.register(Participatie)
class ParticipatieAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'rol', 'persoon', 'organisatie', 'project')
    list_filter = ('rol', 'persoon', 'organisatie', 'project')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    pass

class InlineParticipatie(admin.StackedInline):
    model = Participatie
    extra = 1

class InlineHyperlink(admin.StackedInline):
    model = Hyperlink
    extra = 1

class InlineFoto(admin.StackedInline):
    model = Foto
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
#    list_display = ('__str__', 'omschrijving_truncated', 'show_tags', 'show_doelgroepen', 'betrokkenen')
#    list_filter = ('tags', 'doelgroepen', 'participaties__persoon', )
    list_display = ('__str__', 'omschrijving_truncated', 'show_tags', 'show_doelgroepen', 'betrokken_personen', 'betrokken_organisaties')
    list_filter = ('tags', 'doelgroepen', )
    inlines = [InlineParticipatie, InlineHyperlink, InlineFoto]

    def omschrijving_truncated(self, project):
        s = strip_tags(project.korte_beschrijving)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    omschrijving_truncated.short_description = 'korte beschrijving'

    def show_tags(self, project):
        print(project.tags.all())
        return ', '.join([tag.naam for tag in project.tags.all()])
    show_tags.short_description = 'tags'

    def show_doelgroepen(self, project):
        print(project.doelgroepen.all())
        return ', '.join([doelgroep.naam for doelgroep in project.doelgroepen.all()])
    show_doelgroepen.short_description = 'doelgroepen'

    def betrokken_personen(self, project):
        participaties = project.participaties.filter(persoon__isnull=False)
        return ', '.join(['{} ({})'.format(p.persoon, p.rol) for p in participaties])

    def betrokken_organisaties(self, project):
        participaties = project.participaties.filter(organisatie__isnull=False)
        return ', '.join(['{} ({})'.format(p.organisatie, p.rol) for p in participaties])

@admin.register(Organisatie)
class OrganisatieAdmin(admin.ModelAdmin):
    list_display = ['naam', 'beschrijving_truncated', 'show_tags', 'show_doelgroepen']
    list_filter = ['tags', 'doelgroepen']
    inlines = [InlineParticipatie]

    def beschrijving_truncated(self, org):
        s = strip_tags(org.korte_beschrijving)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    beschrijving_truncated.short_description = 'korte beschrijving'

    def show_tags(self, org):
        return ', '.join([tag.naam for tag in org.tags.all()])
    show_tags.short_description = 'tags'

    def show_doelgroepen(self, org):
        return ', '.join([doelgroep.naam for doelgroep in org.doelgroepen.all()])
    show_doelgroepen.short_description = 'doelgroepen'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Doelgroep)
class DoelgroepAdmin(admin.ModelAdmin):
    pass
