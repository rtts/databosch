from django import forms
from django.forms.formsets import BaseFormSet

class BijeenkomstForm(forms.Form):
    fullname = forms.CharField(label='Jouw volledige naam', max_length=255)
    naam = forms.CharField(label='Naam netwerk', max_length=100)
    datum = forms.DateField(label='Datum', localize=True, widget=forms.TextInput(attrs={'class': 'datefield'}))
    tijd = forms.TimeField(label='Tijd')
    locatie = forms.CharField(label='Naam van de locatie', max_length=100)
    adres = forms.CharField(label='Adres van de locatie', widget=forms.Textarea(attrs={'rows': 3}))
    besloten = forms.BooleanField(label='Dit is een besloten bijeenkomst', required=False)

    gespreksleider_naam = forms.CharField(label='Gespreksleider', max_length=100, required=False)
    gespreksleider_email = forms.EmailField(label='Email', required=False)
    notulist_naam = forms.CharField(label='Notulist', max_length=100, required=False)
    notulist_email = forms.EmailField(label='Email', required=False)
    twitteraar_naam = forms.CharField(label='Twitteraar', max_length=100, required=False)
    twitteraar_email = forms.EmailField(label='Email', required=False)
    fotograaf_naam = forms.CharField(label='Fotograaf', max_length=100, required=False)
    fotograaf_email = forms.EmailField(label='Email', required=False)
    videograaf_naam = forms.CharField(label='Videograaf', max_length=100, required=False)
    videograaf_email = forms.EmailField(label='Email', required=False)

    def clean(self):
        for (name, email) in [
                ('gespreksleider_naam', 'gespreksleider_email'),
                ('notulist_naam', 'notulist_email'),
                ('twitteraar_naam', 'twitteraar_email'),
                ('fotograaf_naam', 'fotograaf_email'),
                ('videograaf_naam', 'videograaf_email'),
                ]:
            if self.cleaned_data[email] and not self.cleaned_data[name]:
                self.add_error(name, 'ontbreekt')
            if self.cleaned_data[name] and not self.cleaned_data[email]:
                self.add_error(email, 'ontbreekt')

class DeelnemerForm(forms.Form):
    naam = forms.CharField(label='Naam', max_length=100, required=False)
    email = forms.EmailField(label='Email', required=False)

class ContactForm(forms.Form):
    titel = forms.CharField(label='Titel initiatief', max_length=100)
    toelichting = forms.CharField(label='Omschrijving', widget=forms.Textarea())
    link = forms.URLField(label='Website van het initiatief')
    email = forms.EmailField(label='Emailadres van het initiatief')

class BaseDeelnemerFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            if form.cleaned_data:
                naam = form.cleaned_data['naam']
                email = form.cleaned_data['email']

                if naam and not email:
                    form.add_error('email', 'ontbreekt')

                if email and not naam:
                    form.add_error('naam', 'ontbreekt')
