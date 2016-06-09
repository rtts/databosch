from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
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

class InlineSiteProject(admin.StackedInline):
    model = SiteProject
    extra = 1

class InlineSiteOrganisatie(admin.StackedInline):
    model = SiteOrganisatie
    extra = 1

class InlineParticipatie(admin.StackedInline):
    model = Participatie
    extra = 1

class InlineHyperlink(admin.StackedInline):
    model = Hyperlink
    extra = 1

class InlineOrganisatieHyperlink(admin.StackedInline):
    model = OrganisatieHyperlink
    extra = 1

class InlineFoto(admin.StackedInline):
    model = Foto
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__str__', 'show_sites', 'beschrijving_truncated', 'show_tags', 'show_doelgroepen', 'betrokken_personen', 'betrokken_organisaties')
    list_filter = ('tags', 'doelgroepen', 'sites')
    inlines = [InlineSiteProject, InlineParticipatie, InlineHyperlink, InlineFoto]

    def beschrijving_truncated(self, project):
        s = strip_tags(project.beschrijving)
        if len(s) > 500:
            s = s[:500] + '...'
        return mark_safe(s)
    beschrijving_truncated.short_description = 'beschrijving'

    def show_sites(self, project):
        return ', '.join([site.domain for site in project.sites.all()])
    show_sites.short_description = 'zichtbaar op'

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
    list_display = ['naam', 'tagline_truncated', 'show_tags', 'show_doelgroepen']
    list_filter = ['tags', 'doelgroepen']
    inlines = [InlineSiteOrganisatie, InlineParticipatie, InlineOrganisatieHyperlink]

    def tagline_truncated(self, org):
        s = strip_tags(org.tagline)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    tagline_truncated.short_description = 'tagline'

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
