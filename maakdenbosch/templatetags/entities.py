from django import template
from django.utils.safestring import mark_safe
from django.contrib.sites.shortcuts import get_current_site
from ..models import SiteEntiteit

register = template.Library()

@register.simple_tag(takes_context=True)
def tagline(context, entity):
    request = context['request']
    site = get_current_site(request)
    try:
        tagline = entity.site_entiteiten.filter(site=site).first().tagline
        if tagline == "":
            tagline = entity.tagline
    except SiteEntiteit.DoesNotExist:
        tagline = entity.tagline
    return mark_safe(tagline)

@register.simple_tag(takes_context=True)
def description(context, entity):
    request = context['request']
    site = get_current_site(request)
    try:
        description = entity.site_entiteiten.filter(site=site).first().beschrijving
        if description == "":
            description = entity.beschrijving
    except SiteEntiteit.DoesNotExist:
        description = entity.beschrijving
    return mark_safe(description)
