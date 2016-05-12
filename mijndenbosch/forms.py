from django import forms
from django.forms.formsets import BaseFormSet
from .models import *

class BijeenkomstForm(forms.Form):
    voornaam = forms.CharField(label='Voornaam', max_length=255)
    achternaam = forms.CharField(label='Achternaam', max_length=255)
    naam = forms.CharField(label='Naam netwerk', max_length=100)
    datum = forms.DateField(label='Datum', localize=True, widget=forms.TextInput(attrs={'class': 'datefield'}))
    tijd = forms.TimeField(label='Tijd')
    locatie = forms.CharField(label='Naam van de locatie', max_length=100)
    adres = forms.CharField(label='Adres van de locatie', widget=forms.Textarea(attrs={'rows': 3}))
    besloten = forms.BooleanField(label='Dit is een besloten bijeenkomst', required=False)

class DeelnemerForm(forms.Form):
    voornaam = forms.CharField(label='Voornaam', max_length=255, required=False)
    achternaam = forms.CharField(label='Achternaam', max_length=255, required=False)
    email = forms.EmailField(label='Email', required=False)
    taak = forms.ModelChoiceField(label='Taak', queryset=Taak.objects.all(), empty_label=None)

class BurgermeesterForm(forms.Form):
    naam = forms.CharField(label='Naam Burgermeester', max_length=255)
    foto = forms.ImageField()
    beschrijving = forms.CharField(label='Karaktereigenschappen', widget=forms.Textarea())

class SpeerpuntForm(forms.Form):
    woord = forms.CharField(label='In één woord', max_length=255)
    beschrijving = forms.CharField(label='Beschrijving', widget=forms.Textarea())

class IdeeForm(forms.Form):
    beschrijving = forms.CharField(label='Beschrijving', max_length=255)
    toelichting = forms.CharField(label='Toelichting', widget=forms.Textarea())

    # In view code, set form.fields['speerpunt'].queryset to bijeenkomst.speerpunten.all()
    speerpunt = forms.ModelChoiceField(label='Speerpunt', queryset=Speerpunt.objects.all(), empty_label=None)

class OndersteuningForm(forms.Form):
    rol = forms.CharField(label='Rol van deze persoon', max_length=255)

    # In view code, set form.fields['persoon'].queryset to Personen.objects.filter(deelnames__bijeenkomst=bijeenkomst)
    persoon = forms.ModelChoiceField(label='Persoon', queryset=Persoon.objects.all(), empty_label=None)

class ContactForm(forms.Form):
    titel = forms.CharField(label='Titel initiatief', max_length=255)
    toelichting = forms.CharField(label='Omschrijving', widget=forms.Textarea())
    link = forms.URLField(label='Website van het initiatief')
    email = forms.EmailField(label='Emailadres van het initiatief')

class BaseDeelnemerFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            voornaam = form.cleaned_data['voornaam']
            achternaam = form.cleaned_data['achternaam']
            email = form.cleaned_data['email']
            taak = form.cleaned_data['taak']

            if not voornaam and not achternaam and not email:
                return
            if not voornaam:
                form.add_error('voornaam', 'ontbreekt')
            if not achternaam:
                form.add_error('achternaam', 'ontbreekt')
            if not email:
                form.add_error('email', 'ontbreekt')

class BaseSpeerpuntFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            woord = form.cleaned_data['woord']
            beschrijving = form.cleaned_data['beschrijving']

            if not woord and not beschrijving:
                return
            if not woord:
                form.add_error('woord', 'ontbreekt')
            if not beschrijving:
                form.add_error('beschrijving', 'ontbreekt')

class BaseIdeeFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            beschrijving = form.cleaned_data['beschrijving']
            toelichting = form.cleaned_data['toelichting']

            if not beschrijving and not toelichting:
                return
            if not beschrijving:
                form.add_error('beschrijving', 'ontbreekt')
            if not toelichting:
                form.add_error('toelichting', 'ontbreekt')

class BaseOndersteuningFormSet(BaseFormSet):
    pass
