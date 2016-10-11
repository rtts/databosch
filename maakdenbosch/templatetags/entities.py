from django import template
from django.utils.safestring import mark_safe
from django.contrib.sites.shortcuts import get_current_site

register = template.Library()

@register.simple_tag(takes_context=True)
def tagline(context, entity):
    request = context['request']
    site = get_current_site(request)
    tagline = entity.site_entiteiten.filter(site=site).first().tagline
    if not tagline:
        tagline = entity.tagline
    return mark_safe(tagline)

@register.simple_tag(takes_context=True)
def description(context, entity):
    request = context['request']
    site = get_current_site(request)
    description = entity.site_entiteiten.filter(site=site).first().beschrijving
    if not description:
        description = entity.beschrijving
    return mark_safe(description)
