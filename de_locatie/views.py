from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import *
from .forms import *
from .utils import *

def download(request, filename):
    return redirect(settings.MEDIA_URL + '/' + filename)

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    sections = page.sections.exclude(visibility=3)
    news = News.objects.all()
    agenda = []
    projects = Project.objects.filter(active=True)

    for section in sections:
        if section.type == 6:
            if section.show_certifications:
                section.certifications = Certification.objects.all()
            if section.show_partners:
                section.funds = Partner.objects.all()
            if section.show_sponsors:
                section.sponsors = Sponsor.objects.all()
            if section.show_partnerships:
                section.partners = set([p.partner for p in Partnership.objects.all()])
        if section.type == 9:
            agenda = Event.objects.order_by('date')

    social = SocialMedia.objects.all()
    footer = get_config(1)

    return render(request, 'de_locatie/page.html', {
        'page': page,
        'header': page.header,
        'mobile_header': page.mobile_header,
        'pages': pages,
        'sections': sections,
        'news': news,
        'projects': projects,
        'footer': footer,
        'social': social,
        'agenda': agenda,
    })

def news(request, slug):
    #news = get_object_or_404(News, slug=slug)
    news = News.objects.filter(slug=slug).first()
    if not news:
        raise Http404
    pages = Page.objects.filter(menu=True)
    header = Header.objects.first()
    mobile_header = Header.objects.last()
    footer = get_config(1)
    social = SocialMedia.objects.all()

    return render(request, 'de_locatie/news.html', {
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

    return render(request, 'de_locatie/project.html', {
        'project': project,
        'partners': partners,
        'news': news,
        'pages': pages,
        'header': header,
        'footer': footer,
        'social': social,
    })
