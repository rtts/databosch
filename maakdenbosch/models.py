from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from mijndenbosch.models import Persoon

class Rol(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'rollen'

class Tag(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']

class Doelgroep(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'Doelgroepen'

class Project(models.Model):
    titel = models.CharField(max_length=255)
    logo = models.ImageField(blank=True)
    korte_beschrijving = RichTextField(blank=True)
    lange_beschrijving = RichTextField(blank=True)
    emailadres = models.EmailField(blank=True)
    bezoekadres = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    doelgroepen = models.ManyToManyField(Doelgroep, blank=True)
    mijndenbosch = models.BooleanField('Zichtbaar op MijnDenBosch.nl', default=False)

    def __str__(self):
        return self.titel

    class Meta:
        ordering = ['titel']
        verbose_name_plural = 'projecten'

class Organisatie(models.Model):
    naam = models.CharField(max_length=255)
    emailadres = models.EmailField(blank=True)
    bezoekadres = models.TextField(blank=True)
    beschrijving = RichTextField(blank=True)

    def __str__(self):
        return self.naam

class Participatie(models.Model):
    rol = models.ForeignKey(Rol)
    persoon = models.ForeignKey(Persoon, related_name='participaties', blank=True, null=True)
    organisatie = models.ForeignKey(Organisatie, related_name='participaties',  blank=True, null=True)
    project = models.ForeignKey(Project, related_name='participaties', blank=True, null=True)

    def clean(self):
        if self.persoon and self.organisatie and self.project:
            raise ValidationError('Één van de koppelingen moet leeg blijven. Je kunt een project koppelen aan een persoon óf aan een organisatie, maar niet allebei tegelijk. Je kunt natuurlijk wel nóg een participatie toevoegen.')

    def __str__(self):
        return 'Participatie als {}'.format(self.rol)

class Hyperlink(models.Model):
    type = models.CharField(max_length=16, choices=(
        ('Website'  , 'Website'),
        ('Facebook' , 'Facebook'),
        ('Twitter'  , 'Twitter'),
        ('Flickr'   , 'Flickr'),
        ('Other'    , 'Other'),
    ))
    url = models.URLField('URL')
    project = models.ForeignKey(Project, related_name='hyperlinks')

    def __str__(self):
        return self.url

class Foto(models.Model):
    bestand = models.ImageField()
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name_plural = 'foto’s'
