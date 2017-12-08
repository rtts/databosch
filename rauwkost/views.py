from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .utils import *

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    footer = get_config(10)

    return render(request, 'maakdenbosch/page.html', {
        'page': page,
        'pages': pages,
        'footer': footer,
    })
