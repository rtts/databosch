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

@admin.register(Entiteitsoort)
class EntiteitsoortAdmin(admin.ModelAdmin):
    pass

@admin.register(Relatiesoort)
class RelatiesoortAdmin(admin.ModelAdmin):
    pass

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

class InlineSiteEntiteit(admin.StackedInline):
    model = SiteEntiteit
    extra = 0

class InlineEntiteitParticipatie(admin.StackedInline):
    model = EntiteitParticipatie
    extra = 0

class InlineRelatiesVan(admin.StackedInline):
    model = EntiteitRelatie
    extra = 0
    fk_name = 'naar_entiteit'
    verbose_name = 'relatie'
    verbose_name_plural = 'inkomende relaties'

class InlineRelatiesNaar(admin.StackedInline):
    model = EntiteitRelatie
    extra = 0
    fk_name = 'van_entiteit'
    verbose_name = 'relatie'
    verbose_name_plural = 'uitgaande relaties'

class InlineEntiteitHyperlink(admin.StackedInline):
    model = EntiteitHyperlink
    extra = 0

class InlinePersoonHyperlink(admin.StackedInline):
    model = PersoonHyperlink
    extra = 0

class InlineEntiteitFoto(admin.StackedInline):
    model = EntiteitFoto
    extra = 0

class EntiteitForm(forms.ModelForm):
  class Meta:
    model = Entiteit
    fields = '__all__'
    widgets = {
      'tags': TagWidget(),
    }

@admin.register(Entiteit)
class EntiteitAdmin(admin.ModelAdmin):
    form = EntiteitForm
    list_display = ('__str__', 'soort', 'show_sites', 'tagline_truncated', 'show_tags', 'show_relaties_naar', 'show_relaties_van', 'betrokken_personen', 'gewijzigd', 'aangemaakt')
    list_filter = ['soort', 'sites', 'tags']
    inlines = [InlineSiteEntiteit, InlineRelatiesVan, InlineRelatiesNaar, InlineEntiteitParticipatie, InlineEntiteitHyperlink, InlineEntiteitFoto]

    save_on_top = True
    actions = ['tagchange_action', 'sitechange_action', 'typechange_action']
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

    def typechange_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect('typechange/?ids={}'.format(','.join(selected)))
    typechange_action.short_description = "Soort veranderen van geselecteerde entiteiten"

    def get_urls(self):
        urls = super(EntiteitAdmin, self).get_urls()
        my_urls = [
            url(r'tagchange/$', self.admin_site.admin_view(self.tagchange)),
            url(r'sitechange/$', self.admin_site.admin_view(self.sitechange)),
            url(r'typechange/$', self.admin_site.admin_view(self.typechange)),
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
                        SiteEntiteit(entiteit=obj, site=site).save()
                messages.success(request, 'De geselecteerde sites zijn succesvol toegevoegd')
            elif 'delete' in request.POST:
                for obj in objects:
                    for site in sites:
                        try:
                            SiteEntiteit(entiteit=obj, site=site).delete()
                        except SiteEntiteit.DoesNotExist:
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

    def typechange(self, request):
        admin_url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        ids = request.GET.get('ids')
        if not ids:
            raise SuspiciousOperation('GET parameter "ids" is missing')
        objects = Entiteit.objects.filter(id__in=ids.split(','))
        soorten = Entiteitsoort.objects.all()

        if request.method == 'POST':
            soort_id = request.POST.get('soort')
            soort = Entiteitsoort.objects.get(id=soort_id)
            for obj in objects:
                obj.soort = soort
                obj.save()
            messages.success(request, 'De relatiesoort van de geselecteerde entiteiten is gewijzigd')
            return HttpResponseRedirect(admin_url)

        return render(request, 'admin/typechange.html', {
            'title': 'Soort wijzigen',
            'objects': objects,
            'soorten': soorten,
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
        return ', '.join([site.name for site in obj.sites.all()])
    show_sites.short_description = 'zichtbaar op'

    def show_tags(self, obj):
        return ', '.join([tag.naam for tag in obj.tags.all()])
    show_tags.short_description = 'tags'

    def show_relaties_naar(self, obj):
        return mark_safe(', '.join(['{} van <a href="{}/change/">{}</a>'.format(r.soort, r.naar_entiteit.pk, r.naar_entiteit) for r in obj.relaties_naar.all()]))
    show_relaties_naar.short_description = 'uitgaande relaties'

    def show_relaties_van(self, obj):
        return mark_safe(', '.join(['<a href="{}/change/">{}</a> is {}'.format(r.van_entiteit.pk, r.van_entiteit, r.soort) for r in obj.relaties_van.all()]))
    show_relaties_van.short_description = 'inkomende relaties'

    def betrokken_personen(self, obj):
        return mark_safe(', '.join(['<a href="../persoon/{}/change/">{}</a> ({})'.format(p.persoon.pk, p.persoon, p.rol) for p in obj.participaties.all()]))
    betrokken_personen.short_description = 'participaties'

@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    list_display = ('id', 'voornaam', 'achternaam', 'email', 'show_sites', 'geassocieerde_gebruiker', 'gewijzigd', 'aangemaakt')
    list_display_links = ['id', 'voornaam']
    list_filter = ['sites', 'deelnames__bijeenkomst'] # 'deelnames__bijeenkomst__speerpunten__ideeen' results in "Filtering not allowed"?!
    actions = ['email_action']
    inlines = [InlineEntiteitParticipatie, InlinePersoonHyperlink]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def email_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect('email/?ids={}'.format(','.join(selected)))
    email_action.short_description = "Email de geselecteerde personen"

    def get_urls(self):
        urls = super(PersoonAdmin, self).get_urls()
        my_urls = [
            url(r'email/$', self.admin_site.admin_view(self.show_emails)),
        ]
        return my_urls + urls

    def show_emails(self, request):
        admin_url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        ids = request.GET.get('ids')
        if not ids:
            raise SuspiciousOperation('GET parameter "ids" is missing')
        objects = self.model.objects.filter(id__in=ids.split(','))
        email_addresses = ', '.join([obj.email_spec() for obj in objects if obj.email])

        return render(request, 'admin/show_emails.html', {
            'title': 'Verstuur een email',
            'email_addresses': email_addresses,
            'admin_url': admin_url,
            'opts': self.model._meta,
        })

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

