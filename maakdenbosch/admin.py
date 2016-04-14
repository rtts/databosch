from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from .models import *

@admin.register(Persoon)
class PersoonAdmin(UserAdmin):
    list_display = ('naam', 'email', 'actief_als', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'telefoonnummer', 'beschrijving', 'profielfoto')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    list_filter = ('participaties__rol', 'is_staff')

    def naam(self, user):
        return str(user)

    def actief_als(self, user):
        return ', '.join(['{} bij {}'.format(p.rol, p.project) for p in user.participaties.all()])

@admin.register(Participatie)
class ParticipatieAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'persoon', 'rol', 'project')
    list_filter = ('persoon', 'rol', 'project')
    pass

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
    list_display = ('__str__', 'omschrijving_truncated', 'show_tags', 'show_doelgroepen', 'betrokkenen')
    list_filter = ('tags', 'doelgroepen', 'participaties__persoon', )
    inlines = [InlineParticipatie, InlineHyperlink, InlineFoto]

    def omschrijving_truncated(self, project):
        s = strip_tags(project.omschrijving)
        if len(s) > 50:
            s = s[:50] + '...'
        return s
    omschrijving_truncated.short_description = 'omschrijving'

    def show_tags(self, project):
        print(project.tags.all())
        return ', '.join([tag.naam for tag in project.tags.all()])
    show_tags.short_description = 'tags'

    def show_doelgroepen(self, project):
        print(project.doelgroepen.all())
        return ', '.join([doelgroep.naam for doelgroep in project.doelgroepen.all()])
    show_doelgroepen.short_description = 'doelgroepen'

    def betrokkenen(self, project):
        return ', '.join(['{} ({})'.format(p.persoon, p.rol) for p in project.participaties.all()])

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Doelgroep)
class DoelgroepAdmin(admin.ModelAdmin):
    pass
