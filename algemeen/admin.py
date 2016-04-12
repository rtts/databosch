from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from .models import *

@admin.register(Persoon)
class PersoonAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'telefoonnummer', 'beschrijving', 'profielfoto')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    list_filter = ('participatie__rol', 'is_staff')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    pass

class InlineParticipatie(admin.StackedInline):
    model = Participatie
    extra = 0

class InlineHyperlink(admin.StackedInline):
    model = Hyperlink
    extra = 0

class InlineFoto(admin.StackedInline):
    model = Foto
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titel', 'omschrijving_truncated', 'betrokkenen')
    list_filter = ('participaties__persoon', )
    inlines = [InlineParticipatie, InlineHyperlink, InlineFoto]

    def omschrijving_truncated(self, project):
        s = strip_tags(project.omschrijving)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    omschrijving_truncated.short_description = 'omschrijving'

    def betrokkenen(self, project):
        return ', '.join([str(p.persoon) for p in project.participaties.all()])
