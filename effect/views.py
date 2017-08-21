from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .utils import *

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    sections = page.sections.exclude(visibility=3)
    icons = SocialMedia.objects.all()
    footer = get_config(1)

    return render(request, 'effect/page.html', {
        'page': page,
        'pages': pages,
        'sections': sections,
        'footer': footer,
        'icons': icons,
    })
