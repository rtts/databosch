from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import *

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'content']

class HyperlinkAdmin(admin.StackedInline):
    model = ProgramHyperlink
    extra = 0

class PhotoAdmin(admin.StackedInline):
    model = ProgramPhoto
    extra = 0

@admin.register(ProgramType)
class ProgramTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'tagline', 'location']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [HyperlinkAdmin, PhotoAdmin]
