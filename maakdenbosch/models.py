from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class Persoon(AbstractUser):
    telefoonnummer = models.CharField(max_length=32, blank=True)
    beschrijving = RichTextField(blank=True)
    profielfoto = models.ImageField(blank=True)

    class Meta:
        verbose_name_plural = 'personen'

    def __str__(self):
        return self.get_full_name() or self.username

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
    omschrijving = RichTextField(blank=True)
    emailadres = models.EmailField(blank=True)
    bezoekadres = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    doelgroepen = models.ManyToManyField(Doelgroep, blank=True)

    def __str__(self):
        return self.titel

    class Meta:
        ordering = ['titel']
        verbose_name_plural = 'projecten'

class Participatie(models.Model):
    persoon = models.ForeignKey(Persoon, related_name='participaties')
    rol = models.ForeignKey(Rol)
    project = models.ForeignKey(Project, related_name='participaties')

    def __str__(self):
        return '{} is {} bij {}'.format(self.persoon, self.rol, self.project)

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

class Foto(models.Model):
    bestand = models.ImageField()
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name_plural = 'foto’s'
