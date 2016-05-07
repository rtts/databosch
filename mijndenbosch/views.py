from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from maakdenbosch.models import Project
from .models import *
from .forms import *

def homepage(request):
    nieuws = Nieuwsbericht.objects.all()
    return render(request, 'homepage.html', {
        'nieuws': nieuws,
        'currentpage': 'homepage',
    })

def bedankt(request):
    return render(request, 'bedankt.html', {})

def leden(request):
    if not request.user.is_authenticated():
        return redirect('registration_register')

    deelnemer_prefix = 'deelnemersform'
    DeelnemerFormSet = formset_factory(DeelnemerForm, extra=3, formset=BaseDeelnemerFormSet)

    # Get this user's first bijeenkomst (multiple bijeenkomsten not
    # yet supported)
    try:
        bijeenkomst = request.user.persoon.bijeenkomsten.first()
    except Persoon.DoesNotExist:
        # this should not happen, but fix it anyway
        p = Persoon(user=request.user, naam=request.user.username, email=request.user.email)
        p.save()
        bijeenkomst = request.user.persoon.bijeenkomsten.first()

    if not bijeenkomst:
        bijeenkomst = Bijeenkomst()
        noob = True
        deelnemers = []
    else:
        noob = False
        deelnemers = [{'naam': d.naam, 'email': d.email} for d in bijeenkomst.deelnemers.all()]

    # Handle posted forms, whether new or change data
    if request.method == 'POST':
        form = BijeenkomstForm(request.POST)
        deelnemer_formset = DeelnemerFormSet(request.POST, prefix=deelnemer_prefix)

        if form.is_valid() and deelnemer_formset.is_valid():
            bijeenkomst.netwerkhouder = request.user.persoon
            bijeenkomst.naam = form.cleaned_data['naam']
            bijeenkomst.datum = form.cleaned_data['datum']
            bijeenkomst.tijd = form.cleaned_data['tijd']
            bijeenkomst.locatie = form.cleaned_data['locatie']
            bijeenkomst.adres = form.cleaned_data['adres']
            bijeenkomst.besloten = form.cleaned_data['besloten']
            bijeenkomst.save()

            # DANGER
            bijeenkomst.deelnemers.clear()

            for deelnemer_form in deelnemer_formset:
                try:
                    naam = deelnemer_form.cleaned_data['naam']
                    email = deelnemer_form.cleaned_data['email']
                except (KeyError, AttributeError):
                    continue

                if naam and email:
                    (p, created) = Persoon.objects.get_or_create(email=email)
                    p.naam = naam
                    p.save()
                    bijeenkomst.deelnemers.add(p)

            messages.success(request, 'Alle wijzigingen zijn opgeslagen!')
            return redirect('leden')

    # Handle GET requests, serve new or change form
    else:
        if noob:
            form = BijeenkomstForm(label_suffix="")
        else:
            form = BijeenkomstForm({
                'naam': bijeenkomst.naam,
                'datum': bijeenkomst.datum,
                'tijd': bijeenkomst.tijd,
                'locatie': bijeenkomst.locatie,
                'adres': bijeenkomst.adres,
                'besloten': bijeenkomst.besloten,
            }, label_suffix="")

        deelnemer_formset = DeelnemerFormSet(initial=deelnemers, prefix=deelnemer_prefix)

    # Show betrokkenheid with other networks?
    betrokken = []
    if hasattr(request.user, 'persoon'):
        for t in request.user.persoon.taken.order_by('bijeenkomst'):
            betrokken.append([t.bijeenkomst, t.naam])

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
