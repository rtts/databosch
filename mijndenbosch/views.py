from django.utils import timezone
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.template import Template, Context
from django.core.mail import send_mail

from registration.forms import RegistrationFormUniqueEmail
from maakdenbosch.models import Entiteit, Persoon
from .models import *
from .forms import *

def homepage(request):
    news = Nieuwsbericht.objects.first()
    now = timezone.now()
    bijeenkomsten = Bijeenkomst.objects.filter(besloten=False, datum__gte=now.date()).order_by('datum')
    latest = Mayor.objects.filter(visible=True).order_by('created').last()
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

def submit(request):
    if request.user.is_authenticated():
        return submit_full(request)
    else:
        return submit_light(request)

def submit_light(request):
    if request.user.is_authenticated():
        return redirect('aanmelden')

    if request.method == "POST":
        person_form = PersonForm(request.POST)
        if person_form.is_valid():
            person = person_form.save(commit=False)
        else:
            person = None

        mayor_form = MayorForm(request.POST, request.FILES)
        if mayor_form.is_valid() and person:
            mayor = mayor_form.save(person=person, commit=False)
        else:
            mayor = None

        idea_forms = IdeaFormSet(request.POST, instance=mayor)
        if idea_forms.is_valid() and person and mayor:
            person.save()
            mijndenbosch = Site.objects.filter(domain='mijndenbosch.nl').first()
            person.sites.add(mijndenbosch)
            mayor.person = person
            mayor.save()
            idea_forms.save()

            email = EmailMessage(
                subject = 'NIEUWE BURGERMEESTER AANGEMELD!',
                body = '''
Hoi,

Deze email is automatisch verzonden omdat er op Mijn Den Bosch een nieuwe BurgeRmeester is aangemeld. Vanwege veiligheidsoverwegingen is deze BurgeRmeester standaard niet zichtbaar in de galerij. Bezoek a.u.b. de volgende URL om de nieuwe aanmelding zichtbaar te maken:

http://databosch.created.today/mijndenbosch/mayor/?o=-2.1
                ''',
                to = settings.CONTACT_FORM_RECIPIENTS,
                )
            email.send()
            return redirect('thanks')

    else:
        person_form = PersonForm()
        mayor_form = MayorForm()
        idea_forms = IdeaFormSet(instance=Mayor())

    return render(request, 'submit_light.html', {
        'person_form': person_form,
        'mayor_form': mayor_form,
        'idea_forms': idea_forms,
        'currentpage': 'aanmelden',
    })

def mayors(request):
    word = request.GET.get('waarde')
    mayors = Mayor.objects.filter(visible=True).prefetch_related('ideas')
    words = sorted(set([i.word for m in mayors for i in m.ideas.all()]))
    if word:
        mayors = mayors.filter(ideas__word=word).distinct()

    return render(request, 'mayors.html', {
        'word': word,
        'words': words,
        'mayors': mayors,
        'currentpage': 'burgermeesters',
    })

def ideas(request):
    word = request.GET.get('waarde')
    ideas = Idea.objects.filter(mayor__visible=True).select_related('mayor')
    words = sorted(set([i.word for i in ideas]))
    if word:
        ideas = ideas.filter(word=word)

    return render(request, 'ideas.html', {
        'word': word,
        'words': words,
        'ideas': ideas,
        'currentpage': 'burgermeesters',
    })

def mayor(request, pk):
    mayor = get_object_or_404(Mayor, pk=pk, visible=True)
    if mayor.meeting and mayor.meeting.entity:
        role, created = Rol.objects.get_or_create(naam='netwerkhouder')
        netwerkhouder = Persoon.objects.filter(entiteit_participaties__entiteit=mayor.meeting.entity, entiteit_participaties__rol=role).first()
    else:
        netwerkhouder = None

    return render(request, 'mayor.html', {
        'mayor': mayor,
        'netwerkhouder': netwerkhouder,
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

@login_required
def submit_full(request):
    person = request.user.persoon
    role, created = Rol.objects.get_or_create(naam='netwerkhouder')
    entity = Entiteit.objects.filter(participaties__persoon=person, participaties__rol=role).first()
    if entity:
        meeting = entity.meetings.first()
    else:
        meeting = None
    if meeting:
        participants = [{'voornaam': d.persoon.voornaam, 'achternaam': d.persoon.achternaam, 'email': d.persoon.email, 'taak': d.taak} for d in meeting.deelnames.all()]
        mayor = meeting.mayors.first()
    else:
        participants = []
        mayor = None

    return render(request, 'aanmelden.html', {
        'person': person,
        'entity': entity,
        'meeting': meeting,
        'participants': participants,
        'mayor': mayor,
        'currentpage': 'aanmelden'
    })

@login_required
def submit_person(request):
    person = request.user.persoon
    person_form = PersonWithPhotoForm(request.POST or None, request.FILES or None, instance=person)
    if request.method == 'POST' and person_form.is_valid():
        person = person_form.save()
        return redirect('aanmelden')

    return render(request, 'submit_person.html', {
        'form': person_form,
        'currentpage': 'aanmelden',
    })

@login_required
def submit_entity(request):
    person = request.user.persoon
    role, created = Rol.objects.get_or_create(naam='netwerkhouder')
    entity = Entiteit.objects.filter(participaties__persoon=person, participaties__rol=role).first()
    entity_form = EntityForm(request.POST or None, request.FILES or None, instance=entity)
    if request.method == 'POST' and entity_form.is_valid():
        entity = entity_form.save(person)
        return redirect('aanmelden')

    return render(request, 'submit_entity.html', {
        'form': entity_form,
        'currentpage': 'aanmelden',
    })

@login_required
def submit_meeting(request):
    person = request.user.persoon
    role, created = Rol.objects.get_or_create(naam='netwerkhouder')
    entity = Entiteit.objects.filter(participaties__persoon=person, participaties__rol=role).first()
    if not entity:
        return redirect('aanmelden')
    meeting = entity.meetings.first()
    meeting_form = MeetingForm(request.POST or None, request.FILES or None, instance=meeting)
    if request.method == 'POST' and meeting_form.is_valid():
        meeting = meeting_form.save(entity)
        return redirect('aanmelden')

    return render(request, 'submit_meeting.html', {
        'form': meeting_form,
        'currentpage': 'aanmelden',
    })

@login_required
def submit_participants(request):
    person = request.user.persoon
    role, created = Rol.objects.get_or_create(naam='netwerkhouder')
    entity = Entiteit.objects.filter(participaties__persoon=person, participaties__rol=role).first()
    if not entity:
        return redirect('aanmelden')
    meeting = entity.meetings.first()
    if not meeting:
        return redirect('aanmelden')

    participants = [{'voornaam': d.persoon.voornaam, 'achternaam': d.persoon.achternaam, 'email': d.persoon.email, 'taak': d.taak} for d in meeting.deelnames.all()]
    participant_forms = ParticipantFormSet(request.POST or None, initial=participants)
    if request.method == 'POST' and participant_forms.is_valid():
        participant_forms.save(meeting)
        return redirect('aanmelden')

    return render(request, 'submit_participants.html', {
        'forms': participant_forms,
        'currentpage': 'aanmelden',
    })

@login_required
def submit_mayor(request):
    person = request.user.persoon
    role, created = Rol.objects.get_or_create(naam='netwerkhouder')
    entity = Entiteit.objects.filter(participaties__persoon=person, participaties__rol=role).first()
    if not entity:
        return redirect('aanmelden')
    meeting = entity.meetings.first()
    if not meeting:
        return redirect('aanmelden')
    mayor = meeting.mayors.first()
    mayor_form = MayorForm(request.POST or None, request.FILES or None, instance=mayor)
    idea_forms = IdeaFormSet(request.POST or None, instance=mayor)
    if request.method == 'POST':
        if mayor_form.is_valid():
            mayor = mayor_form.save(meeting=meeting, commit=False)
            idea_forms = IdeaFormSet(request.POST, instance=mayor) # in case this is a new mayor
        if idea_forms.is_valid() and mayor:
            mayor.visible = True
            mayor.save()
            idea_forms.save()
            return redirect('aanmelden')

    return render(request, 'submit_mayor.html', {
        'mayor_form': mayor_form,
        'idea_forms': idea_forms,
        'currentpage': 'aanmelden',
    })

# @login_required
# def stap3(request):
#     tekst = Webtekst.objects.filter(plek=30)
#     bijeenkomst = Bijeenkomst.objects.filter(netwerkhouder=request.user.persoon).first()
#     step2_allowed = True
#     step3_allowed = True
#     step4_allowed = False
#     if not bijeenkomst:
#         return HttpResponseForbidden()
#     elif bijeenkomst.burgermeester:
#         step4_allowed = True

#     if bijeenkomst.speerpunten.all().exists():
#         extra = 0
#     else:
#         extra = 1

#     SpeerpuntFormSet = inlineformset_factory(Bijeenkomst, Speerpunt, extra=extra, fields=['nummer', 'beschrijving', 'toelichting'])

#     if request.method == "POST":
#         form = BurgermeesterForm(bijeenkomst, request.POST, request.FILES, initial={'foto': bijeenkomst.foto})
#         speerpunt_forms = SpeerpuntFormSet(request.POST, instance=bijeenkomst)
#         if all([form.is_valid(), speerpunt_forms.is_valid()]):
#             form.save(bijeenkomst)
#             speerpunt_forms.save()
#             response = redirect('aanmelden')
#             response['Location'] += '?stap=4'
#             return response

#     else:
#         form = BurgermeesterForm(bijeenkomst, initial={
#             'naam': bijeenkomst.burgermeester,
#             'foto': bijeenkomst.foto,
#             'beschrijving': bijeenkomst.beschrijving,
#         })
#         speerpunt_forms = SpeerpuntFormSet(instance=bijeenkomst)

#     emailadressen = ', '.join([d.persoon.email for d in bijeenkomst.deelnames.all() if d.persoon.email])

#     return render(request, 'aanmelden_stap3.html', {
#         'tekst': tekst,
#         'bijeenkomst': bijeenkomst,
#         'form': form,
#         'speerpunt_forms': speerpunt_forms,
#         'currentpage': 'aanmelden',
#         'emailadressen': emailadressen,
#         'step3_current': True,
#         'step2_allowed': step2_allowed,
#         'step3_allowed': step3_allowed,
#         'step4_allowed': step4_allowed,
#     })

# @login_required
# def stap4(request):
#     tekst = Webtekst.objects.filter(plek=31)
#     bijeenkomst = Bijeenkomst.objects.filter(netwerkhouder=request.user.persoon).first()
#     if not bijeenkomst:
#         return HttpResponseForbidden()
#     if not bijeenkomst.burgermeester:
#         return HttpResponseForbidden()

#     if Idee.objects.filter(speerpunt__in=bijeenkomst.speerpunten.all()).exists():
#         extra = 0
#     else:
#         extra = 1

#     IdeeFormSet = formset_factory(IdeeForm, extra=extra, formset=BaseIdeeFormSet)

#     if request.method == "POST":
#         idee_forms = IdeeFormSet(request.POST)
#         if idee_forms.is_valid():
#             idee_forms.save(bijeenkomst)
#             return redirect('klaar')
#     else:
#         ideeen = []
#         for idee in Idee.objects.filter(speerpunt__bijeenkomst=bijeenkomst):
#             ond = Ondersteuning.objects.filter(idee=idee, rol='kartrekker').first()
#             if not ond:
#                 kartrekker = None
#             else:
#                 kartrekker = ond.persoon
#             helpers = [ond.persoon for ond in Ondersteuning.objects.filter(idee=idee, rol='helper')]
#             ideeen.append({
#                 'nummer': idee.nummer,
#                 'beschrijving': idee.beschrijving,
#                 'toelichting': idee.toelichting,
#                 'speerpunt': idee.speerpunt,
#                 'kartrekker': kartrekker,
#                 'helpers': helpers,
#             })
#         idee_forms = IdeeFormSet(initial=ideeen)

#     for f in idee_forms:
#         f.fields['speerpunt'].queryset = bijeenkomst.speerpunten.all()
#         f.fields['kartrekker'].queryset = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)
#         f.fields['helpers'].queryset = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)

#     return render(request, 'aanmelden_stap4.html', {
#         'tekst': tekst,
#         'idee_forms': idee_forms,
#         'currentpage': 'aanmelden',
#         'step4_current': True,
#         'step2_allowed': True,
#         'step3_allowed': True,
#         'step4_allowed': True,
#     })

def netwerk(request, slug):
    b = get_object_or_404(Bijeenkomst, slug=slug, besloten=False)
    return bijeenkomst(request, b.pk)

def bijeenkomst(request, bpk):
    bijeenkomst = get_object_or_404(Bijeenkomst, pk=bpk, besloten=False)
    entity = bijeenkomst.entity
    if entity:
        role, created = Rol.objects.get_or_create(naam='netwerkhouder')
        netwerkhouder = Persoon.objects.filter(entiteit_participaties__entiteit=entity, entiteit_participaties__rol=role).first()
        naam = entity.titel
        website = entity.hyperlinks.filter(type__type='Website').first
    else:
        netwerkhouder = bijeenkomst.netwerkhouder
        naam = bijeenkomst.naam
        website = None
    deelnemers = Persoon.objects.filter(deelnames__bijeenkomst=bijeenkomst)

    if request.method == 'POST':
        form = DeelnameForm(request.POST)
        if form.is_valid():
            form.save(bijeenkomst)
            messages.success(request, 'Je bent succesvol aangemeld bij deze bijeenkomst. Schrijf het in je agenda!')
    else:
        form = DeelnameForm()

    return render(request, 'bijeenkomst.html', {
        'naam': naam,
        'website': website,
        'netwerkhouder': netwerkhouder,
        'bijeenkomst': bijeenkomst,
        'entity': entity,
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
