from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .utils import *

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    sections = page.sections.exclude(visibility=3)
    news = News.objects.all()
    projects = Project.objects.filter(active=True)
    partners = Partner.objects.all()
    social = SocialMedia.objects.all()
    footer = get_config(1)

    return render(request, 'effect/page.html', {
        'page': page,
        'header': page.header,
        'mobile_header': page.mobile_header,
        'pages': pages,
        'sections': sections,
        'news': news,
        'projects': projects,
        'partners': partners,
        'footer': footer,
        'social': social,
    })

def news(request, slug):
    news = get_object_or_404(News, slug=slug)
    pages = Page.objects.filter(menu=True)
    header = Header.objects.first()
    mobile_header = Header.objects.last()
    footer = get_config(1)
    social = SocialMedia.objects.all()

    return render(request, 'effect/news.html', {
        'news': news,
        'pages': pages,
        'header': header,
        'mobile_header': mobile_header,
        'footer': footer,
        'social': social,
    })

def project(request, slug):
    project = get_object_or_404(Project, slug=slug, active=True)
    partners = [p.partner for p in project.partnerships.all()]
    news = News.objects.filter(project=project)
    pages = Page.objects.filter(menu=True)
    header = Header.objects.first()
    footer = get_config(1)
    social = SocialMedia.objects.all()

    return render(request, 'effect/project.html', {
        'project': project,
        'partners': partners,
        'news': news,
        'pages': pages,
        'header': header,
        'footer': footer,
        'social': social,
    })
