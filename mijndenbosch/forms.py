from django import forms
from django.forms.formsets import BaseFormSet
from .models import *

class Form(forms.Form):
    '''Base form class without label suffixes'''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(Form, self).__init__(*args, **kwargs)

class BijeenkomstForm(Form):
    '''The initial registrationform for bijeenkomsten'''
    voornaam = forms.CharField(label='Voornaam', max_length=255)
    achternaam = forms.CharField(label='Achternaam', max_length=255)
    naam = forms.CharField(label='Naam netwerk', max_length=100)
    datum = forms.DateField(label='Datum', localize=True, widget=forms.TextInput(attrs={'class': 'datefield'}))
    tijd = forms.TimeField(label='Tijd')
    locatie = forms.CharField(label='Naam van de locatie', max_length=100)
    adres = forms.CharField(label='Adres van de locatie', widget=forms.Textarea(attrs={'rows': 3}))
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

class DeelnemerForm(Form):
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
            Deelname(taak=taak, persoon=persoon, bijeenkomst=bijeenkomst).save()

class BurgermeesterForm(Form):
    '''The form for submitting the chosen burgermeester'''
    naam = forms.CharField(label='Naam Burgermeester', max_length=255)
    foto = forms.ImageField(required=False, widget=forms.FileInput())
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

class SpeerpuntForm(Form):
    '''Formset-form for Speerpunten'''
    woord = forms.CharField(label='In één woord', max_length=255, required=False)
    beschrijving = forms.CharField(label='Beschrijving', widget=forms.Textarea(), required=False)

    def clean(self):
        woord = self.cleaned_data.get('woord')
        beschrijving = self.cleaned_data.get('beschrijving')

        if not woord and not beschrijving:
            return
        if not woord:
            self.add_error('woord', 'ontbreekt')
        if not beschrijving:
            self.add_error('beschrijving', 'ontbreekt')

    def save(self, bijeenkomst):
        woord = self.cleaned_data.get('woord')
        beschrijving = self.cleaned_data.get('beschrijving')
        if woord and beschrijving:
            Speerpunt(bijeenkomst=bijeenkomst, woord=woord, beschrijving=beschrijving).save()

class IdeeForm(Form):
    '''Formset-form for Ideeen'''
    beschrijving = forms.CharField(label='Beschrijving', max_length=255, required=False)
    toelichting = forms.CharField(label='Toelichting', widget=forms.Textarea(), required=False)

    # In view code, set form.fields['x'].queryset to the correct subset
    speerpunt = forms.ModelChoiceField(label='Dit idee hoort bij het volgende speerpunt', queryset=Speerpunt.objects.all(), empty_label=None)
    kartrekker = forms.ModelChoiceField(queryset=Persoon.objects.all(), empty_label=None)
    helpers = forms.ModelMultipleChoiceField(queryset=Persoon.objects.all(), required=False)

    def clean(self):
        beschrijving = self.cleaned_data.get('beschrijving')
        toelichting = self.cleaned_data.get('toelichting')

        if not beschrijving and not toelichting:
            return
        if not beschrijving:
            self.add_error('beschrijving', 'ontbreekt')
        if not toelichting:
            self.add_error('toelichting', 'ontbreekt')

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

class ContactForm(Form):
    titel = forms.CharField(label='Titel initiatief', max_length=255)
    toelichting = forms.CharField(label='Omschrijving', widget=forms.Textarea())
    link = forms.URLField(label='Website van het initiatief')
    email = forms.EmailField(label='Emailadres van het initiatief')

class BaseDeelnemerFormSet(BaseFormSet):
    def save(self, bijeenkomst):
        '''Clear and re-save all submitted deelnames'''
        bijeenkomst.deelnames.all().delete()
        for form in self.forms:
            form.save(bijeenkomst)

class BaseSpeerpuntFormSet(BaseFormSet):
    def save(self, bijeenkomst):
        '''Clear and re-save all submitted speerpunten'''
        bijeenkomst.speerpunten.all().delete()
        for form in self.forms:
            form.save(bijeenkomst)

class BaseIdeeFormSet(BaseFormSet):
    def save(self, bijeenkomst):
        '''Clear and re-save all submitted Ideeen'''
        Idee.objects.filter(speerpunt__bijeenkomst=bijeenkomst).delete()
        for form in self.forms:
            form.save(bijeenkomst)
