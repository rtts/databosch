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

    for section in sections:
        if section.type == 6:
            if section.show_partners:
                section.funds = Partner.objects.all()
            if section.show_sponsors:
                section.sponsors = Sponsor.objects.all()
            if section.show_partnerships:
                section.partners = set([p.partner for p in Partnership.objects.all()])
        if section.type == 9:
            section.locations = Location.objects.all()
        if section.type == 10:
            timeslots = TimeSlot.objects.select_related('program', 'program__location').reverse()
            locations = Location.objects.filter(visible=True)

            for location in locations:
                location.slots = []
                for timeslot in timeslots:
                    if timeslot.program.location.pk == location.pk:
                        timeslot.top = (((timeslot.begin.hour - 7.53) + (timeslot.begin.minute / 60)) * 100) + 5
                        delta = timeslot.end - timeslot.begin
                        timeslot.height = ((delta.seconds / 3600) * 100) - 10
                        location.slots.append(timeslot)

            section.locations = locations


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
    mobile_header = Header.objects.last()
    footer = get_config(1)
    social = SocialMedia.objects.all()

    return render(request, 'effect/project.html', {
        'project': project,
        'partners': partners,
        'news': news,
        'pages': pages,
        'header': header,
        'mobile_header': mobile_header,
        'footer': footer,
        'social': social,
    })

def program(request, slug):

    program = get_object_or_404(Program, slug=slug, visible=True)
    pages = Page.objects.filter(menu=True)
    header = Header.objects.first()
    mobile_header = Header.objects.last()
    footer = get_config(1)
    social = SocialMedia.objects.all()

    return render(request, 'effect/program.html', {
        'program': program,
        'pages': pages,
        'header': header,
        'mobile_header': mobile_header,
        'footer': footer,
        'social': social,
    })
