from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField

class Rol(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'participatierollen'

class LinkType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['type']

class Relatiesoort(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'relatiesoorten'
        ordering = ['naam']

class Entiteitsoort(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'entiteitsoorten'
        ordering = ['naam']

class TagGroep(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'tag groepen'
        ordering = ['naam']

class Tag(models.Model):
    naam = models.CharField(max_length=255)
    groep = models.ForeignKey(TagGroep, related_name='tags')

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']

class SiteTag(models.Model):
    naam = models.CharField(max_length=255)
    site = models.ForeignKey(Site, related_name='tags')

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name = 'site-specifieke tag'
        ordering = ['naam']

class Persoon(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)
    voornaam = models.CharField(max_length=255, blank=True)
    achternaam = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    telefoonnummer = models.CharField(max_length=32, blank=True)
    beschrijving = RichTextField(blank=True)
    profielfoto = models.ImageField(blank=True)
    sites = models.ManyToManyField(Site, related_name='personen', blank=True)
    gewijzigd = models.DateTimeField(auto_now=True)
    aangemaakt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.voornaam and self.achternaam:
            return ' '.join([self.voornaam, self.achternaam])
        else:
            return '[naamloos]'

    def email_spec(self):
        if not self.email:
            return None
        if self.voornaam and self.achternaam:
            return '{} {} <{}>'.format(self.voornaam, self.achternaam, self.email)
        else:
            return self.email

    class Meta:
        ordering = ['voornaam', 'achternaam']
        verbose_name_plural = 'personen'
        permissions = (
            ("view_persoon", "Can view persoon"),
        )

class PersoonHyperlink(models.Model):
    type = models.ForeignKey(LinkType)
    url = models.URLField('URL')
    project = models.ForeignKey(Persoon, related_name='hyperlinks')

    def __str__(self):
        return self.url

class Entiteit(models.Model):
    soort = models.ForeignKey(Entiteitsoort)
    titel = models.CharField(max_length=255) # Should've been unique, alas duplicates already exist...
    logo = models.ImageField(blank=True)
    tagline = models.TextField(blank=True)
    beschrijving = RichTextField(blank=True)
    emailadres = models.EmailField(blank=True)
    telefoonnummer = models.CharField(max_length=255, blank=True)
    locatie_naam = models.CharField(max_length=255, blank=True)
    bezoekadres = models.TextField(blank=True)
    opgericht = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    sites = models.ManyToManyField(Site, related_name='entiteiten', through='SiteEntiteit')
    gewijzigd = models.DateTimeField(auto_now=True)
    aangemaakt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titel

    class Meta:
        ordering = ['titel']
        verbose_name_plural = 'entiteiten'
        permissions = (
            ("view_entiteit", "Can view entiteit"),
        )

class SiteEntiteit(models.Model):
    site = models.ForeignKey(Site, related_name='site_entiteiten')
    actief = models.BooleanField(help_text='Geef hiermee aan of deze entiteit zichtbaar is op deze site', default=True)
    tags = models.ManyToManyField(SiteTag, verbose_name='site-specifieke tags', blank=True)
    entiteit = models.ForeignKey(Entiteit, related_name='site_entiteiten')
    tagline = models.TextField(help_text='Laat dit veld leeg om de algemene tagline te gebruiken', blank=True)
    beschrijving = RichTextField(help_text='Laat dit veld leeg om de algemene beschrijving te gebruiken', blank=True)

    def __str__(self):
        if self.site:
            return str(self.site)
        else:
            return 'SiteEntiteit zonder site'

    class Meta:
        verbose_name = 'site-specifieke beschrijving'
        verbose_name_plural = 'site-specifieke beschrijvingen'

class EntiteitRelatie(models.Model):
    soort = models.ForeignKey(Relatiesoort)
    van_entiteit = models.ForeignKey(Entiteit, verbose_name='entiteit', related_name='relaties_naar')
    naar_entiteit = models.ForeignKey(Entiteit, verbose_name='entiteit', related_name='relaties_van')

    def __str__(self):
        return '{} is {} van {}'.format(self.van_entiteit, self.soort, self.naar_entiteit)

    class Meta:
        verbose_name = 'relatie'

class EntiteitParticipatie(models.Model):
    rol = models.ForeignKey(Rol)
    persoon = models.ForeignKey(Persoon, related_name='entiteit_participaties')
    email = models.EmailField(blank=True)
    entiteit = models.ForeignKey(Entiteit, related_name='participaties')

    def __str__(self):
        return '{} is {} van {}'.format(self.persoon, self.rol, self.entiteit)

    class Meta:
        verbose_name = 'participatie'

class EntiteitHyperlink(models.Model):
    type = models.ForeignKey(LinkType)
    url = models.URLField('URL')
    entiteit = models.ForeignKey(Entiteit, related_name='hyperlinks')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'hyperlink'

class EntiteitFoto(models.Model):
    bestand = models.ImageField()
    entiteit = models.ForeignKey(Entiteit, related_name='fotos')

    def __str__(self):
        return self.bestand.name

    class Meta:
        verbose_name = 'foto'
        verbose_name_plural = 'foto’s'

class EntiteitVideo(models.Model):
    video = EmbedVideoField()
    entiteit = models.ForeignKey(Entiteit, related_name='videos')

    def __str__(self):
        return self.video

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'video’s'
