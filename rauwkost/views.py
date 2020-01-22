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

    def edition(self):
        try:
            return Edition.objects.get(date__year=self.kwargs.get('year'))
        except:
            return Edition.objects.last()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edition = self.edition()
        programs = Program.objects.filter(active=True, edition=edition)
        color = None

        if edition.date.year == 2020:
            dates = sorted(list(set([program.date for program in programs])))
        else:
            dates = None

        try:
            current_dates = []
            for d in self.request.GET.getlist('datum'):
                year, month, day = [int(x) for x in d.split('-')]
                current_dates.append(datetime.date(year, month, day))
            if current_dates:
                programs = programs.filter(timeslots__date__in=current_dates)
            else:
                current_dates = dates
        except:
            raise

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

        try:
            current_time = int(self.request.GET.get('tijd'))
            if current_time > 6:
                programs_before_midnight = programs.filter(timeslots__end__hour__gt=current_time).distinct()
                programs_after_midnight = programs.filter(timeslots__end__hour__gte=0, timeslots__end__hour__lt=7).distinct()
                programs = list(programs_before_midnight) + list(programs_after_midnight)
            else:
                programs = programs.filter(timeslots__end__hour__gt=current_time, timeslots__end__hour__lt=7).distinct()

            # if current_time < 7:
            #     # Programs that started before midnight but haven't ended yet
            #     result = list(programs.filter(begin__hour__gte=7, end__hour__lt=7, end__hour__gt=current_time))

            #     # Programs that started after midnight and haven't ended yet
            #     result += list(programs.filter(begin__hour__lt=7, end__hour__gte=current_time))
            # else:
            #     # All programs that start before midnight and end after midnight
            #     result = list(programs.filter(begin__hour__gte=7, end__hour__lt=7))

            #     # Add programs that start and end before midnight but haven't ended yet
            #     result += list(programs.filter(begin__hour__gte=7, end__hour__gt=current_time))

            #     # Re-sort these programs according to begin time
            #     result = sorted(result, key=lambda p: p.begin)

            #     # Add programs that start after midnight
            #     result += list(programs.filter(begin__hour__gte=0, begin__hour__lt=7, end__hour__lt=7))

            # programs = result

        except:
            current_time = None
            programs_before_midnight = programs.filter(timeslots__begin__hour__gt=6).distinct()
            programs_after_midnight = programs.filter(timeslots__end__hour__gte=0, timeslots__end__hour__lt=7).distinct()
            programs = list(programs_before_midnight) + list(programs_after_midnight)

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

class ProgramDetailView(ProgramView):
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
        current_time = program.begin.hour
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
            'current_time': current_time,
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
        try:
            page = Page.objects.get(slug='')
        except Page.DoesNotExist:
            return redirect('homepage', year=Edition.objects.last().date.year)
        return super().get(request)

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
        members = TeamMember.objects.filter(active=True)

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
