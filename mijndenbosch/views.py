from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
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

def leden(request):
    if not request.user.is_authenticated():
        return redirect('registration_register')

    deelnemer_prefix = 'deelnemersform'
    DeelnemerFormSet = formset_factory(DeelnemerForm, extra=3, formset=BaseDeelnemerFormSet)

    bijeenkomst = request.user.persoon.bijeenkomsten.first()
    if not bijeenkomst:
        bijeenkomst = Bijeenkomst()
        noob = True
        deelnemers = []
    else:
        noob = False
        deelnemers = [{'voornaam': d.persoon.voornaam, 'achternaam': d.persoon.achternaam, 'email': d.persoon.email, 'taak': d.taak} for d in bijeenkomst.deelnames.all()]

    # Handle posted forms, whether new or change data
    if request.method == 'POST':
        form = BijeenkomstForm(request.POST)
        deelnemer_formset = DeelnemerFormSet(request.POST, prefix=deelnemer_prefix)

        if all([form.is_valid(), deelnemer_formset.is_valid()]):
            # 1. Save user details
            request.user.persoon.voornaam = form.cleaned_data['voornaam']
            request.user.persoon.achternaam = form.cleaned_data['achternaam']
            request.user.persoon.save()

            # 2. Save bijeenkomst details
            bijeenkomst.netwerkhouder = request.user.persoon
            bijeenkomst.naam = form.cleaned_data['naam']
            bijeenkomst.datum = form.cleaned_data['datum']
            bijeenkomst.tijd = form.cleaned_data['tijd']
            bijeenkomst.locatie = form.cleaned_data['locatie']
            bijeenkomst.adres = form.cleaned_data['adres']
            bijeenkomst.besloten = form.cleaned_data['besloten']
            bijeenkomst.save()

            # 3. Clear and re-save all submitted deelnames
            bijeenkomst.deelnames.all().delete()
            for deelnemer_form in deelnemer_formset:
                voornaam = deelnemer_form.cleaned_data['voornaam']
                achternaam = deelnemer_form.cleaned_data['achternaam']
                email = deelnemer_form.cleaned_data['email']
                taak = deelnemer_form.cleaned_data['taak']

                if voornaam and achternaam and email and taak:
                    persoon = Persoon.objects.filter(email=email).first()
                    if not persoon:
                        persoon = Persoon(email=email)
                    persoon.voornaam = voornaam
                    persoon.achternaam = achternaam
                    persoon.save()
                    Deelname(taak=taak, persoon=persoon, bijeenkomst=bijeenkomst).save()

            messages.success(request, 'Alle wijzigingen zijn opgeslagen!')
            return redirect('leden')

    # Handle GET requests, serve new or change form
    else:
        if noob:
            form = BijeenkomstForm(label_suffix="")
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
            }, label_suffix="")

        deelnemer_formset = DeelnemerFormSet(initial=deelnemers, prefix=deelnemer_prefix)

    return render(request, 'leden.html', {
        'betrokken': betrokken,
        'form': form,
        'deelnemer_formset': deelnemer_formset,
        'currentpage': 'leden',
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
    return render(request, 'burgemeesters.html', {
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
