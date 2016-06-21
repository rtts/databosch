from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from registration.forms import RegistrationFormUniqueEmail
from maakdenbosch.models import Persoon
from .models import *
from .utils import *

#class Form(forms.Form):
#    '''Base form class without label suffixes'''
#    def __init__(self, *args, **kwargs):
#        kwargs.setdefault('label_suffix', '')
#        super(Form, self).__init__(*args, **kwargs)

class MijnDenBoschRegistrationForm(RegistrationFormUniqueEmail):
    voornaam = forms.CharField(max_length=255)
    achternaam = forms.CharField(max_length=255)

    class Meta(RegistrationFormUniqueEmail.Meta):
        fields = [
            'voornaam',
            'achternaam',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        voornaam = self.cleaned_data.get('voornaam')
        achternaam = self.cleaned_data.get('achternaam')
        user = super(MijnDenBoschRegistrationForm, self).save(*args, **kwargs)
        user.first_name = voornaam
        user.last_name = achternaam
        user.save()

        # Try to retrieve and add site object, fail silently
        try:
            site = Site.objects.get(domain='mijndenbosch.nl')
            user.persoon.sites.add(site)
        except:
            pass

        return user

class BijeenkomstForm(forms.Form):
    '''The initial registrationform for bijeenkomsten'''
    halfsized_fields = ['voornaam', 'achternaam', 'datum', 'tijd']
    voornaam = forms.CharField(label='Mijn voornaam', max_length=255)
    achternaam = forms.CharField(label='Mijn achternaam', max_length=255)
    naam = forms.CharField(label='De naam van mijn netwerk', max_length=100)
    datum = forms.DateField(label='Datum', localize=True, widget=forms.TextInput(attrs={'class': 'datefield'}), required=False)
    tijd = forms.TimeField(label='Tijd', required=False)
    locatie = forms.CharField(label='Naam van de locatie', help_text='Kun je geen geschikte ruimte vinden? Er zijn een aantal locaties beschikbaar die je kunt reserveren. De gegevens en locaties vind je in de checklist die je na het opslaan ontvangt.', max_length=100, required=False)
    adres = forms.CharField(label='Adres van de locatie', widget=forms.Textarea(attrs={'rows': 3}), required=False)
    besloten = forms.BooleanField(label='Dit is een besloten bijeenkomst', required=False)

    def save(self, persoon, bijeenkomst):
        '''Save user details and bijeenkomst details'''
        persoon.voornaam = self.cleaned_data['voornaam']
        persoon.achternaam = self.cleaned_data['achternaam']
        persoon.save()

        bijeenkomst.netwerkhouder = persoon
        bijeenkomst.naam = self.cleaned_data['naam']
        bijeenkomst.datum = self.cleaned_data['datum']
        bijeenkomst.tijd = self.cleaned_data['tijd']
        bijeenkomst.locatie = self.cleaned_data['locatie']
        bijeenkomst.adres = self.cleaned_data['adres']
        bijeenkomst.besloten = self.cleaned_data['besloten']
        bijeenkomst.save()

class DeelnemerForm(forms.Form):
    '''Form for adding deelnemers (Deelnames, actually) to bijeenkomst'''
    voornaam = forms.CharField(label='Voornaam', max_length=255, required=False)
    achternaam = forms.CharField(label='Achternaam', max_length=255, required=False)
    email = forms.EmailField(label='Email', required=False)
    taak = forms.ModelChoiceField(label='Taak', queryset=Taak.objects.all(), empty_label=None)

    def clean(self):
        '''Custom clean method to allow empty forms'''
        voornaam = self.cleaned_data.get('voornaam')
        achternaam = self.cleaned_data.get('achternaam')
        email = self.cleaned_data.get('email')
        taak = self.cleaned_data.get('taak')

        if not voornaam and not achternaam and not email:
            return
        if not voornaam:
            self.add_error('voornaam', 'ontbreekt')
        if not achternaam:
            self.add_error('achternaam', 'ontbreekt')
        if not email:
            self.add_error('email', 'ontbreekt')

    def save(self, bijeenkomst):
        '''Create and save a new Deelname'''
        voornaam = self.cleaned_data.get('voornaam')
        achternaam = self.cleaned_data.get('achternaam')
        email = self.cleaned_data.get('email')
        taak = self.cleaned_data.get('taak')

        if voornaam and achternaam and email and taak:
            persoon = Persoon.objects.filter(email=email).first()
            if not persoon:
                persoon = Persoon(email=email)
            persoon.voornaam = voornaam
            persoon.achternaam = achternaam
            persoon.save()
            try:
                Deelname.objects.get_or_create(taak=taak, persoon=persoon, bijeenkomst=bijeenkomst)
            except Deelname.MultipleObjectsReturned:
                pass

class BurgermeesterForm(forms.Form):
    '''The form for submitting the chosen burgermeester'''
    naam = forms.CharField(label='Naam Burgermeester', max_length=255)
    foto = forms.ImageField(label='Foto uploaden', required=False, widget=forms.FileInput())
    beschrijving = forms.CharField(label='Karaktereigenschappen', widget=forms.Textarea())

    def __init__(self, bijeenkomst, *args, **kwargs):
        '''Custom init to allow access to bijeenkomst during validation'''
        self.bijeenkomst = bijeenkomst
        super(BurgermeesterForm, self).__init__(*args, **kwargs)

    def clean(self):
        '''Allow missing photos when a previous photo is available'''
        foto = self.cleaned_data.get('foto')
        if not foto and not self.bijeenkomst.foto:
            self.add_error('foto', 'ontbreekt')

    def save(self, bijeenkomst):
        '''Save bijeenkomst details and foto, if supplied'''
        bijeenkomst.burgermeester = self.cleaned_data.get('naam')
        bijeenkomst.beschrijving = self.cleaned_data['beschrijving']
        foto = self.cleaned_data.get('foto')
        if foto:
            bijeenkomst.foto = foto
        bijeenkomst.save()

class IdeeForm(forms.Form):
    '''Formset-form for Ideeen'''
    beschrijving = forms.CharField(label='Beschrijving', max_length=255, required=False)
    toelichting = forms.CharField(label='Toelichting', widget=forms.Textarea(), required=False)

    # In view code, set form.fields['x'].queryset to the correct subset
    speerpunt = forms.ModelChoiceField(label='Dit idee hoort bij het volgende speerpunt', queryset=Speerpunt.objects.all(), empty_label=None, required=False)
    kartrekker = forms.ModelChoiceField(queryset=Persoon.objects.all(), empty_label=None, required=False)
    helpers = forms.ModelMultipleChoiceField(help_text='Dit is een lijst van alle beschikbare helpers. Je kunt er meerdere selecteren door de Ctrl of Command toets ingedrukt te houden.', queryset=Persoon.objects.all(), required=False)

    def clean(self):
        beschrijving = self.cleaned_data.get('beschrijving')
        toelichting = self.cleaned_data.get('toelichting')
        speerpunt = self.cleaned_data.get('speerpunt')
        kartrekker = self.cleaned_data.get('kartrekker')

        if not beschrijving and not toelichting:
            return
        if not beschrijving:
            self.add_error('beschrijving', 'ontbreekt')
        if not toelichting:
            self.add_error('toelichting', 'ontbreekt')
        if not speerpunt:
            self.add_error('speerpunt', 'ontbreekt')
        if not kartrekker:
            self.add_error('kartrekker', 'ontbreekt')

    def save(self, bijeenkomst):
        beschrijving = self.cleaned_data.get('beschrijving')
        toelichting = self.cleaned_data.get('toelichting')
        speerpunt = self.cleaned_data.get('speerpunt')
        kartrekker = self.cleaned_data.get('kartrekker')
        helpers = self.cleaned_data.get('helpers')
        if beschrijving and toelichting and speerpunt and kartrekker:
            idee = Idee(beschrijving=beschrijving, toelichting=toelichting, speerpunt=speerpunt)
            idee.save()
            Ondersteuning(rol='kartrekker', idee=idee, persoon=kartrekker).save()
            for persoon in helpers:
                Ondersteuning(rol='helper', idee=idee, persoon=persoon).save()

class ContactForm(forms.Form):
    titel = forms.CharField(label='Titel initiatief', max_length=255)
    toelichting = forms.CharField(label='Omschrijving', widget=forms.Textarea())
    link = forms.URLField(label='Website van het initiatief')
    email = forms.EmailField(label='Emailadres van het initiatief')

class DeelnameForm(forms.Form):
    '''Form for anonymous users to add themselves to a bijeenkomst'''
    voornaam = forms.CharField(label='Voornaam', max_length=255)
    achternaam = forms.CharField(label='Achternaam', max_length=255)
    email = forms.EmailField(label='Email')

    def save(self, bijeenkomst):
        '''Create and save a new Deelname'''
        voornaam = self.cleaned_data['voornaam']
        achternaam = self.cleaned_data['achternaam']
        email = self.cleaned_data['email']
        persoon = Persoon.objects.filter(email=email).first()
        if not persoon:
            persoon = Persoon(email=email)
            persoon.voornaam = voornaam
            persoon.achternaam = achternaam
        persoon.save()
        taak, created = Taak.objects.get_or_create(naam='deelnemer')
        try:
            Deelname.objects.get_or_create(taak=taak, persoon=persoon, bijeenkomst=bijeenkomst)
        except Deelname.MultipleObjectsReturned:
            pass

class BaseDeelnemerFormSet(BaseFormSet):
    def save(self, bijeenkomst):
        '''Clear and re-save all submitted deelnames'''
        bijeenkomst.deelnames.all().delete()
        for form in self.forms:
            form.save(bijeenkomst)

class BaseIdeeFormSet(BaseFormSet):
    def save(self, bijeenkomst):
        '''Clear and re-save all submitted Ideeen'''
        Idee.objects.filter(speerpunt__bijeenkomst=bijeenkomst).delete()
        for form in self.forms:
            form.save(bijeenkomst)
