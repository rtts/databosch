from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
import datetime
from .models import *
from .utils import *

class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        icons = SocialMediaIcon.objects.all()
        footer_center = get_config(10)
        footer_left = get_config(11)
        footer_right = get_config(12)
        extra_css = get_config(30)

        menu = []
        try:
            for item in get_config(25).content.split('\n'):
                (link, title) = item.split(' ', 1)
                menu.append({
                    'link': link,
                    'title': title,
                })
        except:
            pass

        context.update({
            'menu': menu,
            'pages': pages,
            'icons': icons,
            'footer_center': footer_center,
            'footer_left': footer_left,
            'footer_right': footer_right,
            'extra_css': extra_css,
        })
        return context

class ProgramView(BaseView):
    template_name = 'rauwkost/program.html'

    def edition(self):
        try:
            return Edition.objects.get(date__year=self.kwargs.get('year'))
        except:
            return Edition.objects.last()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edition = self.edition()
        programs = Program.objects.filter(active=True, edition=edition)

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
                # Programs that started before midnight but haven't ended yet
                result = list(programs.filter(begin__hour__gte=7, end__hour__lt=7, end__hour__gt=current_time))

                # Programs that started after midnight and haven't ended yet
                result += list(programs.filter(begin__hour__lt=7, end__hour__gte=current_time))
            else:
                # All programs that start before midnight and end after midnight
                result = list(programs.filter(begin__hour__gte=7, end__hour__lt=7))

                # Add programs that start and end before midnight but haven't ended yet
                result += list(programs.filter(begin__hour__gte=7, end__hour__gt=current_time))

                # Re-sort these programs according to begin time
                result = sorted(result, key=lambda p: p.begin)

                # Add programs that start after midnight
                result += list(programs.filter(begin__hour__gte=0, begin__hour__lt=7, end__hour__lt=7))

            programs = result

        except:
            current_time = None
            programs = list(programs.filter(begin__hour__gte=7)) + list(programs.filter(begin__hour__lte=7))

        context.update({
            'year': edition.date.year,
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
        edition = self.edition()
        locations = Location.objects.filter(programs__edition=edition).distinct() # REVERSE RELATED LOOKUP!!!

        context.update({
            'locations': locations,
        })
        return context

class HomepageView(ProgramLocationView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        header = self.edition().header
        context.update({
            'header': header,
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
            earliest = Program.objects.filter(begin__hour__gte=7).order_by('begin').first().begin.hour
            latest = Program.objects.filter(end__hour__lte=7).order_by('end').last().end.hour
            times = [hour for hour in (list(range(earliest,24)) + list(range(0,latest+1)))]
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
        current_time = program.begin.hour
        current_type = program.type
        color = program.location.color

        links = list(program.hyperlinks.all())
        for link in links:
            icon = SocialMediaIcon.objects.filter(type=link.type).first()
            if icon:
                link.icon = icon

        context.update({
            'program': program,
            'locations': locations,
            'current_location': current_location,
            'current_time': current_time,
            'current_type': current_type,
            'color': color,
            'links': links,
        })
        return context

class PageView(BaseView):
    template_name = 'rauwkost/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        page = get_object_or_404(Page, slug=slug)
        news = NewsItem.objects.all()
        context.update({
            'page': page,
            'news': news,
        })
        return context

class FrontPageView(BaseView):
    template_name = 'rauwkost/page.html'

    def get(self, request):
        try:
            page = Page.objects.get(slug='')
        except Page.DoesNotExist:
            return redirect('homepage', year=Edition.objects.last().date.year)
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = Page.objects.get(slug='')
        news = NewsItem.objects.all()

        context.update({
            'header': Edition.objects.last().header,
            'page': page,
            'news': news,
        })
        return context
