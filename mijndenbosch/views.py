from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from registration.backends.hmac.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from maakdenbosch.models import Project
from .models import *
from .forms import *

def homepage(request):
    news = Nieuwsbericht.objects.first()
    return render(request, 'homepage.html', {
        'news': news,
        'currentpage': 'homepage',
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

# Workaround due to get_context_data() not being called for FormViews
# (the other half of the workaround lives in navigation.html)
class Aanmelden(RegistrationView):
    aanmelden = True

def aanmelden(request):
    stap = request.GET.get('stap')
    if not stap:
        if request.user.is_authenticated():
            stap = '2'
        else:
            stap = '1'
        response = redirect('leden')
        response['Location'] += '?stap=' + stap
        return response
    try:
        stap = int(stap)
    except:
        raise Http404
    if stap == 1:
        return Aanmelden.as_view(form_class=RegistrationFormUniqueEmail)(request)
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
            response = redirect('leden')
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
        'form': form,
        'deelnemer_forms': deelnemer_forms,
        'currentpage': 'leden',
        'step2_current': True,
        'step2_allowed': step2_allowed,
        'step3_allowed': step3_allowed,
        'step4_allowed': step4_allowed,
    })

@login_required
def stap3(request):
    bijeenkomst = Bijeenkomst.objects.filter(netwerkhouder=request.user.persoon).first()
    step2_allowed = True
    step3_allowed = True
    step4_allowed = False
    if not bijeenkomst:
        return HttpResponseForbidden()
    elif bijeenkomst.burgermeester:
        step4_allowed = True

    SpeerpuntFormSet = formset_factory(SpeerpuntForm, extra=3, formset=BaseSpeerpuntFormSet)

    if request.method == "POST":
        form = BurgermeesterForm(bijeenkomst, request.POST, request.FILES)
        speerpunt_forms = SpeerpuntFormSet(request.POST)
        if all([form.is_valid(), speerpunt_forms.is_valid()]):
            form.save(bijeenkomst)
            speerpunt_forms.save(bijeenkomst)
            response = redirect('leden')
            response['Location'] += '?stap=4'
            return response

    else:
        form = BurgermeesterForm(bijeenkomst, initial={
            'naam': bijeenkomst.burgermeester,
            'foto': bijeenkomst.foto,
            'beschrijving': bijeenkomst.beschrijving,
        })
        speerpunten = [{'woord': s.woord, 'beschrijving': s.beschrijving} for s in bijeenkomst.speerpunten.all()]
        speerpunt_forms = SpeerpuntFormSet(initial=speerpunten)

    return render(request, 'aanmelden_stap3.html', {
        'form': form,
        'speerpunt_forms': speerpunt_forms,
        'currentpage': 'leden',
        'step3_current': True,
        'step2_allowed': step2_allowed,
        'step3_allowed': step3_allowed,
        'step4_allowed': step4_allowed,
    })

@login_required
def stap4(request):
    bijeenkomst = Bijeenkomst.objects.filter(netwerkhouder=request.user.persoon).first()
    if not bijeenkomst:
        return HttpResponseForbidden()
    if not bijeenkomst.burgermeester:
        return HttpResponseForbidden()

    IdeeFormSet = formset_factory(IdeeForm, extra=3, formset=BaseIdeeFormSet)

    if request.method == "POST":
        idee_forms = IdeeFormSet(request.POST)
        if idee_forms.is_valid():
            idee_forms.save(bijeenkomst)
            return redirect('klaar')
    else:
        ideeen = []
        for idee in Idee.objects.filter(speerpunt__bijeenkomst=bijeenkomst):
            ond = Ondersteuning.objects.filter(idee=idee, rol='kartrekker').first()
            kartrekker = ond.persoon
            helpers = [ond.persoon for ond in Ondersteuning.objects.filter(idee=idee, rol='helper')]
            ideeen.append({
                'beschrijving': idee.beschrijving,
                'toelichting': idee.toelichting,
                'kartrekker': kartrekker,
                'helpers': helpers,
            })
        idee_forms = IdeeFormSet(initial=ideeen)

    for f in idee_forms:
        f.fields['speerpunt'].queryset = bijeenkomst.speerpunten.all()
        f.fields['kartrekker'].queryset = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)
        f.fields['helpers'].queryset = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)

    return render(request, 'aanmelden_stap4.html', {
        'idee_forms': idee_forms,
        'currentpage': 'leden',
        'step4_current': True,
        'step2_allowed': True,
        'step3_allowed': True,
        'step4_allowed': True,
    })


def bijeenkomst(request, bpk):
    b = get_object_or_404(Bijeenkomst, pk=bpk)

    return render(request, 'bijeenkomst.html', {
        'bijeenkomst': b,
        'currentpage': 'leden'
    })

def about(request):
    return render(request, 'about.html', {
        'currentpage': 'about'
    })

def burgemeesters(request):
    bijeenkomsten = Bijeenkomst.objects.filter(besloten=False)
    return render(request, 'burgemeesters.html', {
        'bijeenkomsten': bijeenkomsten,
        'currentpage': 'burgemeesters'
    })

def initiatieven(request):
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

    projects = Project.objects.filter(mijndenbosch=True)

    return render(request, 'initiatieven.html', {
        'form': form,
        'projects': projects,
        'currentpage': 'initiatieven'
    })
