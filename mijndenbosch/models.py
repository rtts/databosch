from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from maakdenbosch.models import Persoon

class Webtekst(models.Model):
    plek = models.IntegerField(unique=True, choices=(
        (1, 'Homepage 1'),
        (2, 'Homepage 2'),
        (10, 'Aboutpage 1'),
        (11, 'Aboutpage 2'),
        (12, 'Aboutpage 3'),
        (20, 'Aanmelden puntenlijst 1'),
        (21, 'Aanmelden puntenlijst 2'),
        (22, 'Aanmelden puntenlijst 3'),
        (23, 'Aanmelden puntenlijst 4'),
        (30, 'Aanmelden stap 3'),
        (31, 'Aanmelden stap 4'),
        (40, 'Burgermeesters galerij'),
        (50, 'Initiatieven pagina'),
        (100, 'Email na het aanmelden'),
    ))
    tekst = RichTextField()

    def __str__(self):
        return self.tekst

    class Meta:
        ordering = ['plek']
        verbose_name_plural = 'webteksten'

class Mayor(models.Model):
    name = models.CharField('naam', max_length=255)
    photo = models.ImageField('foto')
    person = models.ForeignKey(Persoon, verbose_name='door persoon', related_name='mayors')
    created = models.DateTimeField('aangemeld op', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'BurgeRmeester'
        ordering = ['created', 'name']

class Idea(NumberedModel):
    number = models.PositiveIntegerField('nummer', blank=True)
    title = models.CharField('titel', max_length=255)
    description = RichTextField('beschrijving')
    word = models.CharField('in één woord', max_length=255)
    mayor = models.ForeignKey(Mayor, related_name='ideas')

    def __str__(self):
        return self.title

    def number_with_respect_to(self):
        return self.mayor.ideas.all()

    class Meta:
        verbose_name = 'idee'
        verbose_name_plural = 'ideeën'
        ordering = ['number', 'mayor']

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

    def get_nice_url(self):
        if self.slug:
            return self.slug
        else:
            return 'bijeenkomst/' + str(self.pk)

    class Meta:
        ordering = ['-datum', '-pk']
        verbose_name_plural = 'bijeenkomsten'

class Taak(models.Model):
    naam = models.CharField(max_length=255)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'taken'

class Deelname(models.Model):
    taak = models.ForeignKey(Taak)
    persoon = models.ForeignKey(Persoon, related_name='deelnames')
    bijeenkomst = models.ForeignKey(Bijeenkomst, related_name='deelnames')

    def __str__(self):
        return '{} is {} bij {}'.format(self.persoon, self.taak, self.bijeenkomst)

class Speerpunt(NumberedModel):
    nummer = models.PositiveIntegerField(blank=True)
    beschrijving = models.CharField(max_length=255)
    toelichting = models.TextField()
    bijeenkomst = models.ForeignKey(Bijeenkomst, related_name='speerpunten')

    def __str__(self):
        return 'Speerpunt "{}" van het netwerk "{}"'.format(self.beschrijving, self.bijeenkomst)

    def number_with_respect_to(self):
        return self.bijeenkomst.speerpunten.all()

    class Meta:
        ordering = ['nummer', 'bijeenkomst']
        verbose_name_plural = 'speerpunten'

class Idee(NumberedModel):
    nummer = models.PositiveIntegerField(blank=True)
    beschrijving = models.CharField(max_length=255)
    toelichting = models.TextField()
    speerpunt = models.ForeignKey(Speerpunt, related_name='ideeen')

    def __str__(self):
        return 'Idee "{}" van het netwerk "{}"'.format(self.beschrijving, self.speerpunt.bijeenkomst)

    def number_with_respect_to(self):
        return Idee.objects.filter(speerpunt__in=self.speerpunt.bijeenkomst.speerpunten.all())

    class Meta:
        ordering = ['nummer', 'speerpunt']
        verbose_name = 'idee (oude stijl)'
        verbose_name_plural = 'ideeën (oude stijl)'

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
