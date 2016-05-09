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

class DeelnemerForm(forms.Form):
    naam = forms.CharField(label='Naam', max_length=100, required=False)
    email = forms.EmailField(label='Email', required=False)

class ContactForm(forms.Form):
    titel = forms.CharField(label='Titel initiatief', max_length=100)
    toelichting = forms.CharField(label='Één zin toelichting', max_length=255)
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

                #if naam and not email:
                #    form.add_error('email', 'ontbreekt')
                #    raise forms.ValidationError(
                #        'Het emailadres ontbreekt',
                #        code='missing_email'
                #    )
                if email and not naam:
                    form.add_error('naam', 'ontbreekt')
                    raise forms.ValidationError(
                        'De naam ontbreekt',
                        code='missing_naam'
                    )
