from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.forms import CheckboxSelectMultiple
from django.conf.urls import url
from django.core.exceptions import SuspiciousOperation
from django.contrib import messages
from .widgets import TagWidget
from .models import *

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

@admin.register(TagGroep)
class TagGroepAdmin(admin.ModelAdmin):
    list_display = ['naam', 'show_tags']
    def show_tags(self, obj):
        return ', '.join([tag.naam for tag in obj.tags.all()])
    show_tags.short_description = 'tags'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['naam', 'groep']
    list_filter = ['groep']

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

class InlinePersoonHyperlink(admin.StackedInline):
    model = PersoonHyperlink
    extra = 1

class InlineFoto(admin.StackedInline):
    model = Foto
    extra = 1

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    fields = '__all__'
    widgets = {
      'tags': TagWidget(),
    }

class OrganisatieForm(forms.ModelForm):
  class Meta:
    model = Organisatie
    fields = '__all__'
    widgets = {
      'tags': TagWidget(),
    }

class ProjectOrganisatieAdmin(admin.ModelAdmin):
    actions = ['tagchange_action', 'sitechange_action']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def tagchange_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect('tagchange/?ids={}'.format(','.join(selected)))
    tagchange_action.short_description = "Tags toevoegen/verwijderen"

    def sitechange_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect('sitechange/?ids={}'.format(','.join(selected)))
    sitechange_action.short_description = "Sites toevoegen/verwijderen"

    def get_urls(self):
        urls = super(ProjectOrganisatieAdmin, self).get_urls()
        my_urls = [
            url(r'tagchange/$', self.admin_site.admin_view(self.tagchange)),
            url(r'sitechange/$', self.admin_site.admin_view(self.sitechange)),
        ]
        return my_urls + urls

    def tagchange(self, request):
        admin_url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        ids = request.GET.get('ids')
        if not ids:
            raise SuspiciousOperation('GET parameter "ids" is missing')
        objects = self.model.objects.filter(id__in=ids.split(','))
        tags = Tag.objects.all()

        if request.method == 'POST':
            tag_ids = request.POST.getlist('tag')
            tags = Tag.objects.filter(id__in=tag_ids)
            if 'add' in request.POST:
                for obj in objects:
                    obj.tags.add(*tags)
                messages.success(request, 'De geselecteerde tags zijn succesvol toegevoegd')
            elif 'delete' in request.POST:
                for obj in objects:
                    obj.tags.remove(*tags)
                messages.success(request, 'De geselecteerde tags zijn succesvol verwijderd')
            return HttpResponseRedirect(admin_url)

        return render(request, 'admin/tagchange.html', {
            'title': 'Change tags',
            'type': 'tags',
            'objects': objects,
            'tags': tags,
            'admin_url': admin_url,
            'opts': self.model._meta,
        })

    def sitechange(self, request):
        admin_url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        ids = request.GET.get('ids')
        if not ids:
            raise SuspiciousOperation('GET parameter "ids" is missing')
        objects = self.model.objects.filter(id__in=ids.split(','))
        sites = Site.objects.all()

        if request.method == 'POST':
            site_ids = request.POST.getlist('tag')
            sites = Site.objects.filter(id__in=site_ids)
            if 'add' in request.POST:
                for obj in objects:
                    for site in sites:
                        if self.model._meta.model_name == 'project':
                            self.sitemodel(project=obj, site=site).save()
                        if self.model._meta.model_name == 'organisatie':
                            self.sitemodel(organisatie=obj, site=site).save()
                messages.success(request, 'De geselecteerde sites zijn succesvol toegevoegd')
            elif 'delete' in request.POST:
                for obj in objects:
                    for site in sites:
                        try:
                            if self.model._meta.model_name == 'project':
                                self.sitemodel.objects.get(project=obj, site=site).delete()
                            if self.model._meta.model_name == 'organisatie':
                                self.sitemodel.objects.get(organisatie=obj, site=site).delete()
                        except self.sitemodel.DoesNotExist:
                            pass
                messages.success(request, 'De geselecteerde sites zijn succesvol verwijderd')
            return HttpResponseRedirect(admin_url)

        return render(request, 'admin/tagchange.html', {
            'title': 'Change sites',
            'type': 'sites',
            'objects': objects,
            'tags': sites,
            'admin_url': admin_url,
            'opts': self.model._meta,
        })

    def tagline_truncated(self, obj):
        s = obj.tagline
        if len(s) > 50:
            s = s[:50] + '...'
        return mark_safe(s)
    tagline_truncated.short_description = 'tagline'

    def show_sites(self, obj):
        return ', '.join([site.domain for site in obj.sites.all()])
    show_sites.short_description = 'zichtbaar op'

    def show_tags(self, obj):
        return ', '.join([tag.naam for tag in obj.tags.all()])
    show_tags.short_description = 'tags'

    def show_doelgroepen(self, obj):
        return ', '.join([doelgroep.naam for doelgroep in obj.doelgroepen.all()])
    show_doelgroepen.short_description = 'doelgroepen'

@admin.register(Project)
class ProjectAdmin(ProjectOrganisatieAdmin):
    form = ProjectForm
    sitemodel = SiteProject
    save_on_top = True
    list_display = ('__str__', 'show_sites', 'tagline_truncated', 'show_tags', 'betrokken_personen', 'betrokken_organisaties', 'gewijzigd', 'aangemaakt')
    list_filter = ('tags', 'sites')
    inlines = [InlineSiteProject, InlineParticipatie, InlineHyperlink, InlineFoto]

    def betrokken_personen(self, project):
        participaties = project.participaties.filter(persoon__isnull=False)
        return ', '.join(['{} ({})'.format(p.persoon, p.rol) for p in participaties])

    def betrokken_organisaties(self, project):
        participaties = project.participaties.filter(organisatie__isnull=False)
        return ', '.join(['{} ({})'.format(p.organisatie, p.rol) for p in participaties])

@admin.register(Organisatie)
class OrganisatieAdmin(ProjectOrganisatieAdmin):
    form = OrganisatieForm
    sitemodel = SiteOrganisatie
    list_display = ['__str__', 'show_sites', 'tagline_truncated', 'show_tags', 'betrokken_personen', 'betrokken_projecten', 'gewijzigd', 'aangemaakt']
    list_filter = ['site_organisaties__site', 'tags']
    inlines = [InlineSiteOrganisatie, InlineParticipatie, InlineOrganisatieHyperlink]

    def betrokken_personen(self, org):
        participaties = org.participaties.filter(persoon__isnull=False)
        return ', '.join(['{} ({})'.format(p.persoon, p.rol) for p in participaties])

    def betrokken_projecten(self, org):
        participaties = org.participaties.filter(project__isnull=False)
        return ', '.join(['{} ({})'.format(p.project, p.rol) for p in participaties])

@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    list_display = ('id', 'voornaam', 'achternaam', 'email', 'show_sites', 'geassocieerde_gebruiker', 'gewijzigd', 'aangemaakt')
    list_display_links = ['id', 'voornaam']
    list_filter = ['sites', 'deelnames__bijeenkomst'] # 'deelnames__bijeenkomst__speerpunten__ideeen' results in "Filtering not allowed"?!
    inlines = [InlineParticipatie, InlinePersoonHyperlink]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

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

