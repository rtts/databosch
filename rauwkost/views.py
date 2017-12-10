from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import *
from .utils import *

class ProgramView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.all()
        return context

class ProgramLocationView(ProgramView):
    template_name = 'rauwkost/location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()

        try:
            location = Location.objects.get(slug=self.kwargs['slug'])
            context['current_location'] = location
            context['programs'] = location.programs.all()
            context['color'] = location.color
        except:
            pass

        return context

class ProgramTimeView(ProgramView):
    template_name = 'rauwkost/time.html'

class ProgramTypeView(ProgramView):
    template_name = 'rauwkost/type.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = ProgramType.objects.all()

        try:
            type = ProgramType.objects.get(slug=self.kwargs['slug'])
            context['current_type'] = type
            context['programs'] = type.programs.all()
            context['color'] = type.color
        except:
            pass

        return context

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    footer = get_config(10)

    return render(request, 'rauwkost/page.html', {
        'page': page,
        'pages': pages,
        'footer': footer,
    })
