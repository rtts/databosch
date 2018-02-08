from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.sites.models import Site
from django.urls import resolve
from maakdenbosch.models import Entiteit, Entiteitsoort, Tag
from .forms import SearchForm

class Entities(View):
    def get(self, request):
        form = SearchForm(request.GET)
        jadb = Site.objects.get(domain='jadb.nl')
        entities = jadb.entiteiten.filter(site_entiteiten__actief=True).prefetch_related('tags', 'sites', 'site_entiteiten__entiteit', 'site_entiteiten__site', 'relaties_van__van_entiteit', 'relaties_van__naar_entiteit', 'relaties_naar__van_entiteit', 'relaties_naar__naar_entiteit', 'relaties_van__soort', 'relaties_naar__soort', 'participaties', 'participaties__persoon', 'participaties__rol', 'hyperlinks__type', 'fotos', 'videos')

        if form.is_valid():
            soort = form.cleaned_data.get('soort')
            wijk = form.cleaned_data.get('wijk')
            if soort:
                entities = entities.filter(soort=soort)
            if wijk:
                entities = entities.filter(tags__in=[wijk])
            tags = form.cleaned_data.get('tags')
            query = form.cleaned_data.get('query')
            if query:
                entities = entities.filter(titel__icontains=query)
            if tags:
                entities = entities.filter(tags__in=tags).distinct()

        return render(request, 'jadb/entities.html', {
            'form': form,
            'entities': entities,
        })
        # jadb = Site.objects.get(domain='jadb.nl')
        # tags = Tag.objects.all()
        # requested_tags = request.GET.getlist('tag')
        # requested_soort = request.GET.get('soort')
        # entities = jadb.entiteiten.all()
        # selected_tags = []
        # if requested_soort:
        #     soort = get_object_or_404(Entiteitsoort, naam=requested_soort)
        #     entities = entities.filter(soort=soort)
        # if requested_tags:
        #     tags = entities.filter(naam__in=requested_tags)
        #     entities = jadb.entiteiten.filter(tags__in=tags).distinct()
        #     selected_tags = [tag.id for tag in tags]
        # return request(

# class Entities(View):
#     def get(self, request):
#         jadb = Site.objects.get(domain='jadb.nl')
#         requested_tags = request.GET.getlist('tag')
#         if requested_tags:
#             tags = Tag.objects.filter(naam__in=requested_tags)
#             entities = jadb.entiteiten.filter(tags__in=tags).distinct()
#             selected_tags = [tag.id for tag in tags]
#         else:
#             entities = jadb.entiteiten.filter(tags__in=self.tags).distinct()
#             selected_tags = []

#         return render(request, 'jadb/base.html', {
#             'tags': self.tags,
#             'selected_tags': selected_tags,
#             'entities': entities,
#             'current_url': resolve(request.path_info).url_name
#         })

# class Alles(Entities):
#     tags = Tag.objects.all()

# class Cultureel(Entities):
#     tags = Tag.objects.filter(groep__naam='Cultuur categorie')

# class Maatschappelijk(Entities):
#     tags = Tag.objects.filter(groep__naam='Maatschappelijk thema')

# class Persoonlijk(Entities):
#     tags = Tag.objects.filter(groep__naam='Participatiedoel')

# class Initiatieven(Entities):
#     tags = Tag.objects.filter(groep__naam='Type Entiteit')

