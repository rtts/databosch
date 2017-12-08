from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import *
from .utils import *

class ProgramView(ListView):
    queryset = Program.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProgramLocationView(ProgramView):
    location = None
    template_name = 'rauwkost/location.html'

class ProgramTimeView(ProgramView):
    time = None
    template_name = 'rauwkost/time.html'

class ProgramTypeView(ProgramView):
    type = None
    template_name = 'rauwkost/type.html'

def page(request, slug=''):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.filter(menu=True)
    footer = get_config(10)

    return render(request, 'rauwkost/page.html', {
        'page': page,
        'pages': pages,
        'footer': footer,
    })