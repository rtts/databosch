from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.forms import CheckboxSelectMultiple
from .models import *

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

@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
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
    list_display = ('__str__', 'show_sites', 'tagline_truncated', 'show_tags', 'show_doelgroepen', 'betrokken_personen', 'betrokken_organisaties', 'aangemaakt')
    list_filter = ('tags', 'doelgroepen', 'sites')
    inlines = [InlineSiteProject, InlineParticipatie, InlineHyperlink, InlineFoto]

    def tagline_truncated(self, project):
        s = project.tagline
        if len(s) > 50:
            s = s[:50] + '...'
        return mark_safe(s)
    tagline_truncated.short_description = 'tagline'

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
    list_filter = ['site_organisaties__site', 'tags', 'doelgroepen']
    inlines = [InlineSiteOrganisatie, InlineParticipatie, InlineOrganisatieHyperlink]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
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

@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    list_display = ('voornaam', 'achternaam', 'email', 'show_sites', 'geassocieerde_gebruiker', 'aangemaakt')
    list_filter = ['sites', 'deelnames__bijeenkomst', 'deelnames__bijeenkomst__speerpunten__ideeen']
    inlines = [InlineParticipatie]
    def geassocieerde_gebruiker(self, persoon):
        if persoon.user:
            return mark_safe('<a href="{}">{}</a>'.format(reverse('admin:auth_user_change', args=[persoon.user.pk]), persoon.user))
        else:
            return '[geen]'
    def show_sites(self, persoon):
        return ', '.join([site.domain for site in persoon.sites.all()])
    show_sites.short_description = 'sites'
    def get_queryset(self, request):
        qs = super(PersoonAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(voornaam='', achternaam='')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Doelgroep)
class DoelgroepAdmin(admin.ModelAdmin):
    pass
