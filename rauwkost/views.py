from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import *
from .utils import *

class ProgramView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.filter(active=True)
        context['pages'] = Page.objects.filter(menu=True)
        context['footer'] = get_config(10)
        return context

class ProgramLocationView(ProgramView):
    template_name = 'rauwkost/location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()

        try:
            location = Location.objects.get(slug=self.kwargs['slug'])
            context['current_location'] = location
            context['programs'] = location.programs.filter(active=True)
            context['color'] = location.color
        except:
            pass

        return context

class ProgramTimeView(ProgramView):
    template_name = 'rauwkost/time.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['times'] = ['{:02d}:{:02d}'.format(hour, minute) for hour in range(14,24) for minute in [0, 30]] + ['{:02d}:{:02d}'.format(hour, minute) for hour in range(0,5) for minute in [0, 30]]

        try:
            time = self.kwargs['slug']
            context['current_time'] = time
            (hours, minutes) = time.split(':')
            context['programs'] = context['programs'].filter(begin__hour__gte=hours)
        except:
            pass

        return context

class ProgramTypeView(ProgramView):
    template_name = 'rauwkost/type.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = ProgramType.objects.all()

        try:
            type = ProgramType.objects.get(slug=self.kwargs['slug'])
            context['current_type'] = type
            context['programs'] = type.programs.filter(active=True)
            context['color'] = type.color
        except:
            pass

        return context

class ProgramDetailView(ProgramView):
    template_name = 'rauwkost/program_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        program = get_object_or_404(Program, slug=slug)
        locations = Location.objects.all()
        current_location = program.location
        color = program.location.color

        context.update({
            'program': program,
            'locations': locations,
            'current_location': current_location,
            'color': color,
        })
        return context

class PageView(ProgramView):
    template_name = 'rauwkost/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        page = get_object_or_404(Page, slug=slug)
        context.update({
            'page': page,
        })
        return context
