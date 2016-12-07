from django import forms
from django.forms import BaseFormSet, formset_factory, inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils.text import slugify
from registration.forms import RegistrationFormUniqueEmail
from maakdenbosch.models import *
from .models import *
from .utils import *

#class Form(forms.Form):
#    '''Base form class without label suffixes'''
#    def __init__(self, *args, **kwargs):
#        kwargs.setdefault('label_suffix', '')
#        super(Form, self).__init__(*args, **kwargs)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Persoon
        fields = ['voornaam', 'achternaam', 'email']

class PersonWithPhotoForm(forms.ModelForm):
    class Meta:
        model = Persoon
        fields = ['voornaam', 'achternaam', 'email', 'profielfoto']

class EntityForm(forms.ModelForm):
    class Meta:
        model = Entiteit
        fields = ['soort', 'titel', 'tagline', 'beschrijving', 'emailadres', 'logo']

    def save(self, person, *args, **kwargs):
        entity = super(EntityForm, self).save(*args, **kwargs)
        role, created = Rol.objects.get_or_create(naam='netwerkhouder')
        EntiteitParticipatie(rol=role, persoon=person, entiteit=entity).save()
        return entity

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Bijeenkomst
        fields = ['slug', 'datum', 'tijd', 'locatie', 'adres', 'beschrijving']

    def save(self, entity, *args, **kwargs):
        meeting = super(MeetingForm, self).save(*args, commit=False, **kwargs)
        meeting.entity = entity
        meeting.save()
        return meeting

class MayorForm(forms.ModelForm):
    class Meta:
        model = Mayor
        exclude = ['person', 'meeting']

    def save(self, *args, person=None, meeting=None, commit=True, **kwargs):
        mayor = super(MayorForm, self).save(*args, commit=False, **kwargs)
        if person:
            mayor.person = person
        if meeting:
            mayor.meeting = meeting
        if commit:
            mayor.save()
        return mayor

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        exclude = ['number']

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

class ParticipantForm(forms.Form):
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

class BaseParticipantFormSet(BaseFormSet):
    def save(self, bijeenkomst):
        '''Clear and re-save all submitted deelnames'''
        bijeenkomst.deelnames.all().delete()
        for form in self.forms:
            form.save(bijeenkomst)

ParticipantFormSet = formset_factory(ParticipantForm, extra=3, formset=BaseParticipantFormSet)

IdeaFormSet = inlineformset_factory(Mayor, Idea, form=IdeaForm, extra=0, min_num=1)
