from django.contrib import admin
from django.utils.html import mark_safe
from django.forms import CheckboxSelectMultiple
from .models import *

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_url']
    def get_url(self, obj):
        return mark_safe('<a href="https://www.rauwkost.online/download/{}" target="_blank" download>https://www.rauwkost.online/download/{}</a>'.format(str(obj), str(obj)))
    get_url.short_description = 'downloadlink'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'date', 'program']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'program':
            edition = Edition.objects.last()
            kwargs['queryset'] = Program.objects.filter(edition=edition)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ['date']

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'url']
    def has_add_permission(self, request):
        return False

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_filter = ['page']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'content']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

class HyperlinkAdmin(admin.StackedInline):
    model = ProgramHyperlink
    extra = 0

class PhotoAdmin(admin.StackedInline):
    model = ProgramPhoto
    extra = 0

class VideoAdmin(admin.StackedInline):
    model = ProgramVideo
    extra = 0

class PartnerAdmin(admin.StackedInline):
    model = ProgramPartner
    extra = 0

class InlineBlogAdmin(admin.StackedInline):
    prepopulated_fields = {'slug': ('title',)}
    model = Blog
    extra = 0
    min_num = 1

@admin.register(ProgramType)
class ProgramTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    save_on_top = True
    ordering = ['title']
    list_display = ['title', 'tagline', 'edition', 'location', 'active']
    list_filter = ['edition', 'location', 'tags']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [HyperlinkAdmin, PhotoAdmin, VideoAdmin, InlineBlogAdmin]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(SocialMediaIcon)
class SocialAdmin(admin.ModelAdmin):
    pass

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

