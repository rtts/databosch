from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    sections = page.sections.exclude(visibility=3)
    icons = SocialMedia.objects.all()
    footer = Config.objects.filter(parameter__in=[1])

    return render(request, 'page.html', {
        'page': page,
        'pages': pages,
        'sections': sections,
        'footer': footer,
        'icons': icons,
    })
