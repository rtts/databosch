from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import *

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_filter = ['page', 'type', 'visibility']

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    save_on_top = True

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    pass

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    save_on_top = True

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['parameter', 'content']

class InlineTimeSlotAdmin(admin.StackedInline):
    model = TimeSlot
    extra = 0

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'tagline', 'location']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [InlineTimeSlotAdmin]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'date']
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
