from copy import copy
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
import datetime
from .models import *
from .utils import *

def download(request, filename):
    return redirect(settings.MEDIA_URL + '/' + filename)

class BaseView(TemplateView):
    def edition(self):
        try:
            return Edition.objects.get(date__year=self.kwargs.get('year'))
        except:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = Page.objects.filter(menu=True)
        icons = SocialMediaIcon.objects.all()
        footer_center = get_config(10)
        footer_left = get_config(11)
        footer_right = get_config(12)
        extra_css = get_config(30)
        consent_request = get_config(1)
        consent1 = get_config(2)
        consent2 = get_config(3)
        consent = self.request.session.get('consent')
        button_color = get_config(20)
        sponsors = Sponsor.objects.all()

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
            'consent_request': consent_request,
            'consent': consent,
            'consent1': consent1,
            'consent2': consent2,
            'menu': menu,
            'pages': pages,
            'icons': icons,
            'footer_center': footer_center,
            'footer_left': footer_left,
            'footer_right': footer_right,
            'extra_css': extra_css,
            'button_color': button_color,
            'sponsors': sponsors,
        })
        return context

class ProgramView(BaseView):
    template_name = 'rauwkost/program.html'

    # def get(self, request, *args, **kwargs):
    #     if self.kwargs.get('year') == '2020' and not self.request.GET.get('datum'):
    #         params = request.GET.copy()
    #         params['datum'] = '2020-01-24'
    #         return redirect(reverse('homepage', args=['2020']) + '?' + params.urlencode())
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edition = self.edition()
        programs = Program.objects.filter(active=True, edition=edition).select_related('edition', 'location', 'type').prefetch_related('photos', 'timeslots')
        color = None

        if edition.date.year == 2020:
            dates = [datetime.date(2020, 1, 24), datetime.date(2020, 1, 25)]
        else:
            dates = None

        current_dates = []
        for d in self.request.GET.getlist('datum'):
            try:
                year, month, day = [int(x) for x in d.split('-')]
                current_dates.append(datetime.date(year, month, day))
            except:
                pass
        if current_dates:
            programs = programs.filter(timeslots__date__in=current_dates).prefetch_related('timeslots').distinct()

        current_tags = Tag.objects.filter(name__in=self.request.GET.getlist('tag'))
        if current_tags:
            programs = programs.filter(tags__in=current_tags)

        current_locations = Location.objects.filter(slug__in=self.request.GET.getlist('locatie'))
        if current_locations.exists():
            programs = programs.filter(location__in=current_locations)
        if len(current_locations) == 1:
            color = current_locations[0].color

        current_types = ProgramType.objects.filter(slug__in=self.request.GET.getlist('soort'))
        if current_types.exists():
            programs = programs.filter(type__in=current_types)

        def shift(x):
            return (x - 6) % 24

        try:
            current_time = int(self.request.GET.get('tijd'))
            hour = shift(current_time)
        except:
            current_time = None
            hour = 0

        result = []
        unique_titles = set()
        for p in programs:
            for t in p.timeslots.all():
                if not current_dates or t.date in current_dates:
                    if shift(t.end.hour) > hour:
                        if current_dates or p.title not in unique_titles:
                            unique_titles.add(p.title)
                            program = copy(p)
                            program.timeslot = t
                            result.append(program)
        programs = sorted(result, key=lambda p: shift(p.timeslot.begin.hour))

        context.update({
            'year': edition.date.year,
            'current_tags': current_tags,
            'current_locations': current_locations,
            'current_types': current_types,
            'current_time': current_time,
            'programs': programs,
            'color': color,
            'dates': dates,
            'current_dates': current_dates,
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

class ProgramDetailView(BaseView):
    template_name = 'rauwkost/program_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.edition().date.year
        slug = self.kwargs.get('slug')
        program = Program.objects.filter(slug=slug).first()
        if program is None:
            raise Http404
        locations = Location.objects.all()
        current_location = program.location
        #current_time = program.begin.hour
        current_type = program.type
        color = program.location.color

        links = list(program.hyperlinks.all())
        for link in links:
            icon = SocialMediaIcon.objects.filter(type=link.type).first()
            if icon:
                link.icon = icon

        location_links = list(program.location.hyperlinks.all())
        for link in location_links:
            icon = SocialMediaIcon.objects.filter(type=link.type).first()
            if icon:
                link.icon = icon

        blogs = program.blogs.filter(active=True)

        context.update({
            'year': year,
            'program': program,
            'locations': locations,
            'current_location': current_location,
            #'current_time': current_time,
            'current_type': current_type,
            'color': color,
            'links': links,
            'location_links': location_links,
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
        return redirect('homepage', year=Edition.objects.last().date.year)
        #try:
        #    page = Page.objects.get(slug='')
        #except Page.DoesNotExist:
        #    return redirect('homepage', year=Edition.objects.last().date.year)
        #return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = Page.objects.get(slug='')
        news = NewsItem.objects.all()
        blogs = Blog.objects.filter(active=True)
        items = list(blogs) + list(news)
        items.sort(key=lambda item: item.date, reverse=True)

        context.update({
            'page': page,
            'items': items,
        })
        return context

class BlogView(BaseView):
    template_name = 'rauwkost/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'], active=True)

        context.update({
            'blog': blog,
        })
        return context

class TeamView(BaseView):
    template_name = 'rauwkost/team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members = TeamMember.objects.filter(active=True).select_related('role')

        context.update({
            'members': members,
        })
        return context

class LocationsView(BaseView):
    template_name = 'rauwkost/locations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locations = Location.objects.all()

        context.update({
            'locations': locations,
        })
        return context

class ConsentView(View):
    def post(self, form):
        self.request.session['consent'] = self.request.POST.get('consent') == 'yes'
        return redirect(self.request.GET.get('return', '/'))
