from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField
from maakdenbosch.models import Entiteit, Persoon, LinkType

class Page(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField('URL', blank=True, unique=True)
    menu = models.BooleanField('zichtbaar in het menu', default=True)

    def __str__(self):
        return '{}. {}'.format(self.position, self.title)

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Pagina’s'
        ordering = ['position']

class Config(models.Model):
    TYPES = [
        (10, 'Footer tekst'),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES)
    content = models.TextField('inhoud')

    def __str__(self):
        return "{}. {}".format(self.parameter, self.get_parameter_display())

    class Meta:
        verbose_name = 'Parameter'
        ordering = ['parameter']

COLORS = [
    (1, 'Kleur 1'),
    (2, 'Kleur 2'),
    (3, 'Kleur 3'),
]

class Location(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    address = models.TextField('adres')
    photo = models.ImageField('foto', blank=True)
    logo = models.ImageField('logo', blank=True)
    icon = models.ImageField('icoon', blank=True)
    color = models.PositiveIntegerField('kleur', choices=COLORS)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Locatie'
        ordering = ['position']

class ProgramType(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    name = models.CharField('naam', max_length=255)
    icon = models.ImageField('icoon', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']
        verbose_name = 'soort'
        verbose_name_plural = 'soorten'

class ProgramHyperlink(models.Model):
    type = models.ForeignKey(LinkType, related_name='+')
    url = models.URLField('URL')
    program = models.ForeignKey('Program', related_name='hyperlinks')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'hyperlink'

class ProgramPhoto(models.Model):
    image = models.ImageField('afbeelding')
    program = models.ForeignKey('Program', related_name='photos')

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = 'foto'
        verbose_name_plural = 'foto’s'

class Program(models.Model):
    location = models.ForeignKey('Location', verbose_name='locatie')
    begin = models.TimeField('begintijd')
    end = models.TimeField('eindtijd')
    title = models.CharField('titel', max_length=255)
    tagline = models.CharField('ondertitel', max_length=255)
    slug = models.SlugField()
    short_description = models.TextField('korte beschrijving', blank=True)
    long_description = RichTextField('lange beschrijving', blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Programma item'