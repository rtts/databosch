from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import *
from .utils import *

class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        footer = get_config(10)
        context.update({
            'pages': pages,
            'footer': footer,
        })
        return context

class ProgramView(BaseView):
    template_name = 'rauwkost/program.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programs = Program.objects.filter(active=True)
        programs = list(programs.filter(begin__hour__gte=7)) + list(programs.filter(begin__hour__lte=7))

        try:
            current_location = Location.objects.get(slug=self.request.GET.get('locatie'))
            programs = programs.filter(location=current_location)
            color = current_location.color
        except:
            current_location = None
            color = None

        try:
            current_type = ProgramType.objects.get(slug=self.request.GET.get('soort'))
            programs = programs.filter(type=current_type)
        except:
            current_type = None

        try:
            current_time = int(self.request.GET.get('tijd'))
            if current_time < 7:
                programs = programs.filter(begin__hour__gte=current_time, end__hour__lte=7)
            else:
                programs = list(programs.filter(begin__hour__gte=current_time)) + list(programs.filter(begin__hour__lte=7))
        except:
            current_time = None

        context.update({
            'current_location': current_location,
            'current_type': current_type,
            'current_time': current_time,
            'programs': programs,
            'color': color,
        })
        return context

class ProgramLocationView(ProgramView):
    template_name = 'rauwkost/location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locations = Location.objects.all()
        context.update({
            'locations': locations,
        })
        return context

class ProgramTypeView(ProgramView):
    template_name = 'rauwkost/type.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        types = ProgramType.objects.all()
        context.update({
            'types': types,
        })
        return context

class ProgramTimeView(ProgramView):
    template_name = 'rauwkost/time.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            earliest = Program.objects.filter(begin__hour__gte=12).first().begin.hour
            latest = Program.objects.filter(end__hour__lte=12).last().end.hour
            times = [hour for hour in (list(range(earliest,24)) + list(range(0,latest)))]
            context.update({
                'times': times,
            })
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
