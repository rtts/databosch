from django.contrib import admin
from .models import *

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    save_on_top = True

#@admin.register(Project)
#class ProjectAdmin(admin.ModelAdmin):
#    save_on_top = True

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    save_on_top = True

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    save_on_top = True

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    save_on_top = True

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['parameter', 'content']

