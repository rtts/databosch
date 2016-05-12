from django import forms
from django.forms.formsets import BaseFormSet
from .models import Taak

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
    voornaam = forms.CharField(label='Voornaam', max_length=100, required=False)
    achternaam = forms.CharField(label='Achternaam', max_length=100, required=False)
    email = forms.EmailField(label='Email', required=False)
    taak = forms.ModelChoiceField(label='Taak', queryset=Taak.objects.all(), empty_label=None)

class ContactForm(forms.Form):
    titel = forms.CharField(label='Titel initiatief', max_length=100)
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
