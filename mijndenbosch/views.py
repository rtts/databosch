from django.utils import timezone
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.template import Template, Context
from django.core.mail import send_mail

from registration.backends.hmac.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from maakdenbosch.models import Entiteit, Persoon
from .models import *
from .forms import *

def homepage(request):
    news = Nieuwsbericht.objects.first()
    now = timezone.now()
    bijeenkomsten = Bijeenkomst.objects.filter(besloten=False, datum__gte=now.date()).order_by('datum')
    latest = Mayor.objects.order_by('created').last()
    tekst = Webtekst.objects.filter(plek__in=[1,2])
    return render(request, 'homepage.html', {
        'news': news,
        'latest': latest,
        'bijeenkomsten': bijeenkomsten,
        'tekst': tekst,
        'currentpage': 'homepage',
    })

def about(request):
    tekst = Webtekst.objects.filter(plek__in=[10,11,12])
    return render(request, 'about.html', {
        'currentpage': 'about',
        'tekst': tekst,
    })

def thanks(request):
    return render(request, 'thanks.html', {
        'currentpage': 'submit_mayor',
    })

def submit_mayor(request):
    IdeaFormSet = inlineformset_factory(Mayor, Idea, form=IdeaForm, extra=0, min_num=1)

    if request.method == "POST":
        person_form = PersonForm(request.POST)
        if person_form.is_valid():
            valid_person = True
            person = person_form.save()
            mijndenbosch = Site.objects.filter(domain='mijndenbosch.nl').first()
            person.sites.add(mijndenbosch)
        else:
            valid_person = False

        mayor_form = MayorForm(request.POST, request.FILES)
        if mayor_form.is_valid() and valid_person:
            valid_mayor = True
            mayor = mayor_form.save(person)
        else:
            valid_mayor = False
            mayor = Mayor()

        idea_forms = IdeaFormSet(request.POST, instance=mayor)
        if idea_forms.is_valid() and valid_mayor:
            idea_forms.save()
            return redirect('thanks')

    else:
        person_form = PersonForm()
        mayor_form = MayorForm()
        idea_forms = IdeaFormSet(instance=Mayor())

    return render(request, 'submit_mayor.html', {
        'person_form': person_form,
        'mayor_form': mayor_form,
        'idea_forms': idea_forms,
        'currentpage': 'submit_mayor',
    })

def mayors(request):
    mayors = Mayor.objects.all().prefetch_related('ideas')
    return render(request, 'mayors.html', {
        'mayors': mayors,
        'currentpage': 'burgermeesters',
    })

def mayor(request, pk):
    mayor = get_object_or_404(Mayor, pk=pk)

    return render(request, 'mayor.html', {
        'mayor': mayor,
        'currentpage': 'burgermeesters'
    })

def news(request):
    news = Nieuwsbericht.objects.all()
    return render(request, 'news.html', {
        'news': news,
    })

def bedankt(request):
    return render(request, 'bedankt.html', {})

def klaar(request):
    return render(request, 'klaar.html', {})

class Aanmelden(RegistrationView):
    # Workaround to highlight the "aanmelden" in the menu in registration_form.html
    # (this variable is accessed in navigation.html)
    aanmelden = True

    # Workaround to pass Webtekst objects to the registration_form.html template
    tekst = Webtekst.objects.filter(plek__in=[20,21,22,23])

    form_class = MijnDenBoschRegistrationForm

def aanmelden(request):
    stap = request.GET.get('stap')
    if not stap:
        if request.user.is_authenticated():
            stap = '2'
        else:
            stap = '1'
        response = redirect('aanmelden')
        response['Location'] += '?stap=' + stap
        return response
    try:
        stap = int(stap)
    except:
        raise Http404
    if stap == 1:
        return Aanmelden.as_view()(request)
    if stap == 2:
        return stap2(request)
    if stap == 3:
        return stap3(request)
    if stap == 4:
        return stap4(request)
    if stap > 4:
        return HttpResponseForbidden()

@login_required
def stap2(request):
    tekst = Webtekst.objects.filter(plek__in=[20,21,22,23])
    bijeenkomst = request.user.persoon.bijeenkomsten.first()
    step2_allowed = True
    step3_allowed = False
    step4_allowed = False
    if not bijeenkomst:
        bijeenkomst = Bijeenkomst()
    else:
        step3_allowed = True
        if bijeenkomst.burgermeester:
            step4_allowed = True

    DeelnemerFormSet = formset_factory(DeelnemerForm, extra=3, formset=BaseDeelnemerFormSet)

    if request.method == 'POST':
        form = BijeenkomstForm(request.POST)
        deelnemer_forms = DeelnemerFormSet(request.POST)

        if all([form.is_valid(), deelnemer_forms.is_valid()]):
            form.save(request.user.persoon, bijeenkomst)
            deelnemer_forms.save(bijeenkomst)

            # Send email:
            email_template = Template(Webtekst.objects.get(plek=100).tekst)
            email_context = Context({
                'voornaam': request.user.persoon.voornaam,
                'achternaam': request.user.persoon.achternaam,
                'datum': bijeenkomst.datum,
                'locatie': bijeenkomst.locatie,
                'aanmeldlink': 'http://mijndenbosch.nl/' + bijeenkomst.get_nice_url(),
            })
            email_string = email_template.render(email_context)
            send_mail(
                subject = 'Mijndenbosch aanmelding geslaagd',
                from_email = 'info@mijndenbosch.nl',
                recipient_list = [request.user.persoon.email],
                message = strip_tags(email_string),
                html_message = email_string,
            )

            response = redirect('aanmelden')
            response['Location'] += '?stap=3'
            return response

    else:
        form = BijeenkomstForm(initial={
            'voornaam': request.user.persoon.voornaam,
            'achternaam': request.user.persoon.achternaam,
            'naam': bijeenkomst.naam,
            'datum': bijeenkomst.datum,
            'tijd': bijeenkomst.tijd,
            'locatie': bijeenkomst.locatie,
            'adres': bijeenkomst.adres,
            'besloten': bijeenkomst.besloten,
        })

        deelnemers = [{'voornaam': d.persoon.voornaam, 'achternaam': d.persoon.achternaam, 'email': d.persoon.email, 'taak': d.taak} for d in bijeenkomst.deelnames.all()]
        deelnemer_forms = DeelnemerFormSet(initial=deelnemers)

    return render(request, 'aanmelden_stap2.html', {
        'tekst': tekst,
        'form': form,
        'deelnemer_forms': deelnemer_forms,
        'currentpage': 'aanmelden',
        'step2_current': True,
        'step2_allowed': step2_allowed,
        'step3_allowed': step3_allowed,
        'step4_allowed': step4_allowed,
    })

@login_required
def stap3(request):
    tekst = Webtekst.objects.filter(plek=30)
    bijeenkomst = Bijeenkomst.objects.filter(netwerkhouder=request.user.persoon).first()
    step2_allowed = True
    step3_allowed = True
    step4_allowed = False
    if not bijeenkomst:
        return HttpResponseForbidden()
    elif bijeenkomst.burgermeester:
        step4_allowed = True

    if bijeenkomst.speerpunten.all().exists():
        extra = 0
    else:
        extra = 1

    SpeerpuntFormSet = inlineformset_factory(Bijeenkomst, Speerpunt, extra=extra, fields=['nummer', 'beschrijving', 'toelichting'])

    if request.method == "POST":
        form = BurgermeesterForm(bijeenkomst, request.POST, request.FILES, initial={'foto': bijeenkomst.foto})
        speerpunt_forms = SpeerpuntFormSet(request.POST, instance=bijeenkomst)
        if all([form.is_valid(), speerpunt_forms.is_valid()]):
            form.save(bijeenkomst)
            speerpunt_forms.save()
            response = redirect('aanmelden')
            response['Location'] += '?stap=4'
            return response

    else:
        form = BurgermeesterForm(bijeenkomst, initial={
            'naam': bijeenkomst.burgermeester,
            'foto': bijeenkomst.foto,
            'beschrijving': bijeenkomst.beschrijving,
        })
        speerpunt_forms = SpeerpuntFormSet(instance=bijeenkomst)

    emailadressen = ', '.join([d.persoon.email for d in bijeenkomst.deelnames.all() if d.persoon.email])

    return render(request, 'aanmelden_stap3.html', {
        'tekst': tekst,
        'bijeenkomst': bijeenkomst,
        'form': form,
        'speerpunt_forms': speerpunt_forms,
        'currentpage': 'aanmelden',
        'emailadressen': emailadressen,
        'step3_current': True,
        'step2_allowed': step2_allowed,
        'step3_allowed': step3_allowed,
        'step4_allowed': step4_allowed,
    })

@login_required
def stap4(request):
    tekst = Webtekst.objects.filter(plek=31)
    bijeenkomst = Bijeenkomst.objects.filter(netwerkhouder=request.user.persoon).first()
    if not bijeenkomst:
        return HttpResponseForbidden()
    if not bijeenkomst.burgermeester:
        return HttpResponseForbidden()

    if Idee.objects.filter(speerpunt__in=bijeenkomst.speerpunten.all()).exists():
        extra = 0
    else:
        extra = 1

    IdeeFormSet = formset_factory(IdeeForm, extra=extra, formset=BaseIdeeFormSet)

    if request.method == "POST":
        idee_forms = IdeeFormSet(request.POST)
        if idee_forms.is_valid():
            idee_forms.save(bijeenkomst)
            return redirect('klaar')
    else:
        ideeen = []
        for idee in Idee.objects.filter(speerpunt__bijeenkomst=bijeenkomst):
            ond = Ondersteuning.objects.filter(idee=idee, rol='kartrekker').first()
            if not ond:
                kartrekker = None
            else:
                kartrekker = ond.persoon
            helpers = [ond.persoon for ond in Ondersteuning.objects.filter(idee=idee, rol='helper')]
            ideeen.append({
                'nummer': idee.nummer,
                'beschrijving': idee.beschrijving,
                'toelichting': idee.toelichting,
                'speerpunt': idee.speerpunt,
                'kartrekker': kartrekker,
                'helpers': helpers,
            })
        idee_forms = IdeeFormSet(initial=ideeen)

    for f in idee_forms:
        f.fields['speerpunt'].queryset = bijeenkomst.speerpunten.all()
        f.fields['kartrekker'].queryset = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)
        f.fields['helpers'].queryset = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)

    return render(request, 'aanmelden_stap4.html', {
        'tekst': tekst,
        'idee_forms': idee_forms,
        'currentpage': 'aanmelden',
        'step4_current': True,
        'step2_allowed': True,
        'step3_allowed': True,
        'step4_allowed': True,
    })

def bijeenkomst(request, bpk):
    bijeenkomst = get_object_or_404(Bijeenkomst, pk=bpk, besloten=False)
    deelnemers = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)

    if request.method == 'POST':
        form = DeelnameForm(request.POST)
        if form.is_valid():
            form.save(bijeenkomst)
            messages.success(request, 'Je bent succesvol aangemeld bij deze bijeenkomst. Schrijf het in je agenda!')
    else:
        form = DeelnameForm()

    return render(request, 'bijeenkomst.html', {
        'bijeenkomst': bijeenkomst,
        'deelnemers': deelnemers,
        'form': form,
    })

def burgermeesters(request):
    bijeenkomsten = Bijeenkomst.objects.filter(besloten=False).exclude(burgermeester='')
    tekst = Webtekst.objects.filter(plek=40)
    return render(request, 'burgermeesters.html', {
        'bijeenkomsten': bijeenkomsten,
        'tekst': tekst,
        'currentpage': 'burgermeesters'
    })

def netwerk(request, slug):
    bijeenkomst = get_object_or_404(Bijeenkomst, slug=slug, besloten=False)
    if bijeenkomst.burgermeester:
        return render(request, 'burgermeester.html', {
            'bijeenkomst': bijeenkomst,
            'currentpage': 'burgermeesters'
        })
    else:
        deelnemers = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)

        if request.method == 'POST':
            form = DeelnameForm(request.POST)
            if form.is_valid():
                form.save(bijeenkomst)
                messages.success(request, 'Je bent succesvol aangemeld bij deze bijeenkomst. Schrijf het in je agenda!')
        else:
            form = DeelnameForm()

        return render(request, 'bijeenkomst.html', {
            'bijeenkomst': bijeenkomst,
            'deelnemers': deelnemers,
            'form': form,
        })

def burgermeester(request, bpk):
    bijeenkomst = get_object_or_404(Bijeenkomst, pk=bpk, besloten=False)
    if bijeenkomst.slug:
        return redirect('netwerk', bijeenkomst.slug)

    return render(request, 'burgermeester.html', {
        'bijeenkomst': bijeenkomst,
        'currentpage': 'burgermeesters'
    })

def initiatieven(request):
    tekst = Webtekst.objects.filter(plek=50)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = EmailMessage(
                subject = 'Aanmelding initiatief via MijnDenBosch.nl',
                body = '\n\n'.join([form.cleaned_data['titel'], form.cleaned_data['toelichting'], form.cleaned_data['link']]),
                to = settings.CONTACT_FORM_RECIPIENTS,
                headers = {'Reply-To': form.cleaned_data['email']},
                )
            email.send()
            return redirect('bedankt')
    else:
        form = ContactForm()

    site = get_object_or_404(Site, domain='mijndenbosch.nl')
    projects = site.entiteiten.all()

    return render(request, 'initiatieven.html', {
        'tekst': tekst,
        'form': form,
        'projects': projects,
        'currentpage': 'initiatieven'
    })
