from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from ckeditor.fields import RichTextField

class Rol(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'rollen'

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

    class Meta:
        ordering = ['voornaam', 'achternaam']
        verbose_name_plural = 'personen'

class Project(models.Model):
    titel = models.CharField(max_length=255)
    logo = models.ImageField(blank=True)
    tagline = models.TextField(blank=True)
    beschrijving = RichTextField(blank=True)
    emailadres = models.EmailField(blank=True)
    locatie_naam = models.CharField(max_length=255, blank=True)
    bezoekadres = models.TextField(blank=True)
    opgericht = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    sites = models.ManyToManyField(Site, related_name='projects', through='SiteProject')
    gewijzigd = models.DateTimeField(auto_now=True)
    aangemaakt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titel

    class Meta:
        ordering = ['titel']
        verbose_name_plural = 'projecten'

class SiteProject(models.Model):
    site = models.ForeignKey(Site, related_name='siteprojects')
    project = models.ForeignKey(Project, related_name='siteprojects')
    tagline = models.TextField(blank=True)
    beschrijving = RichTextField(blank=True)
    actief = models.BooleanField(default=True)

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = 'site-specifieke beschrijving'
        verbose_name_plural = 'site-specifieke beschrijvingen'

class Organisatie(models.Model):
    naam = models.CharField(max_length=255)
    logo = models.ImageField(blank=True)
    tagline = models.TextField(blank=True)
    beschrijving = RichTextField(blank=True)
    emailadres = models.EmailField(blank=True)
    locatie_naam = models.CharField(max_length=255, blank=True)
    bezoekadres = models.TextField(blank=True)
    opgericht = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    sites = models.ManyToManyField(Site, related_name='organisaties', through='SiteOrganisatie')
    gewijzigd = models.DateTimeField(auto_now=True)
    aangemaakt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']

class SiteOrganisatie(models.Model):
    site = models.ForeignKey(Site, related_name='site_organisaties')
    organisatie = models.ForeignKey(Organisatie, related_name='site_organisaties')
    tagline = models.TextField(blank=True)
    beschrijving = RichTextField(blank=True)
    actief = models.BooleanField(default=True)

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = 'site-specifieke beschrijving'
        verbose_name_plural = 'site-specifieke beschrijvingen'

class Participatie(models.Model):
    rol = models.ForeignKey(Rol)
    email = models.EmailField(blank=True)
    persoon = models.ForeignKey(Persoon, related_name='participaties', blank=True, null=True)
    organisatie = models.ForeignKey(Organisatie, related_name='participaties',  blank=True, null=True)
    project = models.ForeignKey(Project, related_name='participaties', blank=True, null=True)

    def clean(self):
        if self.persoon and self.organisatie and self.project:
            raise ValidationError('Één van de koppelingen moet leeg blijven. Je kunt een project koppelen aan een persoon óf aan een organisatie, maar niet allebei tegelijk. Je kunt natuurlijk wel nóg een participatie toevoegen.')

    def __str__(self):
        return 'Participatie als {}'.format(self.rol)

class LinkType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Hyperlink(models.Model):
    type = models.ForeignKey(LinkType)
    url = models.URLField('URL')
    project = models.ForeignKey(Project, related_name='hyperlinks')

    def __str__(self):
        return self.url

class OrganisatieHyperlink(models.Model):
    type = models.ForeignKey(LinkType)
    url = models.URLField('URL')
    project = models.ForeignKey(Organisatie, related_name='hyperlinks')

    def __str__(self):
        return self.url

class PersoonHyperlink(models.Model):
    type = models.ForeignKey(LinkType)
    url = models.URLField('URL')
    project = models.ForeignKey(Persoon, related_name='hyperlinks')

    def __str__(self):
        return self.url

class Foto(models.Model):
    bestand = models.ImageField()
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name_plural = 'foto’s'
