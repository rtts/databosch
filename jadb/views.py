from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve
from maakdenbosch.models import Entiteit, Tag

class Entities(View):
    def get(self, request):
        jadb = Site.objects.get(domain='jadb.nl')
        requested_tags = request.GET.getlist('tag')
        if requested_tags:
            tags = Tag.objects.filter(naam__in=requested_tags)
            entities = jadb.entiteiten.filter(tags__in=tags).distinct()
            selected_tags = [tag.id for tag in tags]
        else:
            entities = jadb.entiteiten.filter(tags__in=self.tags).distinct()
            selected_tags = []

        return render(request, 'jadb/base.html', {
            'tags': self.tags,
            'selected_tags': selected_tags,
            'entities': entities,
            'current_url': resolve(request.path_info).url_name
        })

class Alles(Entities):
    tags = Tag.objects.all()

class Cultureel(Entities):
    tags = Tag.objects.filter(groep__naam='Cultuur categorie')

class Maatschappelijk(Entities):
    tags = Tag.objects.filter(groep__naam='Maatschappelijk thema')

class Persoonlijk(Entities):
    tags = Tag.objects.filter(groep__naam='Participatiedoel')

class Initiatieven(Entities):
    tags = Tag.objects.filter(groep__naam='Type Entiteit')

