from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField

class Persoon(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)
    voornaam = models.CharField(max_length=255, blank=True)
    achternaam = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    telefoonnummer = models.CharField(max_length=32, blank=True)
    beschrijving = RichTextField(blank=True)
    profielfoto = models.ImageField(blank=True)

    def __str__(self):
        if self.voornaam and self.achternaam:
            return ' '.join([self.voornaam, self.achternaam])
        else:
            return str(self.user)

    class Meta:
        ordering = ['achternaam']
        verbose_name_plural = 'personen'

class Bijeenkomst(models.Model):
    slug = models.SlugField('url', help_text='De burgermeester van dit netwerk is ook te bezoeken op mijndenbosch.nl/[watjijhierinvult]/', blank=True)
    naam = models.CharField('naam netwerk', max_length=255)
    netwerkhouder = models.ForeignKey(Persoon, related_name='bijeenkomsten')
    datum = models.DateField(blank=True, null=True)
    tijd = models.TimeField(blank=True, null=True)
    locatie = models.CharField('naam locatie', max_length=255, blank=True)
    adres = models.TextField('adres locatie', blank=True)
    besloten = models.BooleanField('dit is een besloten bijeenkomst', default=False)
    burgermeester = models.CharField('naam burgermeester', max_length=255, blank=True)
    foto = models.ImageField(blank=True)
    beschrijving = models.TextField('Karaktereigenschappen', blank=True)

    def __str__(self):
        return self.naam

    def get_absolute_url(self):
        return reverse('bijeenkomst', args=[self.pk])

    class Meta:
        ordering = ['-datum', '-pk']
        verbose_name_plural = 'bijeenkomsten'

class Taak(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['pk']
        verbose_name_plural = 'taken'

class Deelname(models.Model):
    taak = models.ForeignKey(Taak)
    persoon = models.ForeignKey(Persoon, related_name='deelnames')
    bijeenkomst = models.ForeignKey(Bijeenkomst, related_name='deelnames')

    def __str__(self):
        return '{} is {} bij {}'.format(self.persoon, self.taak, self.bijeenkomst)

class Speerpunt(models.Model):
    beschrijving = models.CharField(max_length=255)
    toelichting = models.TextField()
    bijeenkomst = models.ForeignKey(Bijeenkomst, related_name='speerpunten')

    def __str__(self):
        return self.beschrijving

    class Meta:
        ordering = ['pk']
        verbose_name_plural = 'speerpunten'

class Idee(models.Model):
    beschrijving = models.CharField(max_length=255)
    toelichting = models.TextField()
    speerpunt = models.ForeignKey(Speerpunt, related_name='ideeen')

    def __str__(self):
        return self.beschrijving

    class Meta:
        ordering = ['pk']
        verbose_name_plural = 'ideeën'

class Ondersteuning(models.Model):
    rol = models.CharField(help_text='Wat is de rol van de persoon bij dit idee? (Bijvoorbeeld bedenker, kartrekker, betrokkene)', max_length=255)
    idee = models.ForeignKey(Idee, related_name='ondersteuningen')
    persoon = models.ForeignKey(Persoon, related_name='ondersteuningen')

    class Meta:
        verbose_name_plural = 'ondersteuningen'

class Nieuwsbericht(models.Model):
    datum = models.DateField()
    titel = models.CharField(max_length=255)
    inhoud = RichTextField(blank=True)

    class Meta:
        ordering = ['-datum']
        verbose_name_plural = 'nieuwsberichten'
