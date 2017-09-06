from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField
from maakdenbosch.models import Entiteit, Persoon

class Page(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField('URL', blank=True, unique=True)
    menu = models.BooleanField('zichtbaar in het menu', default=True)
    image = models.ImageField('afbeelding', blank=True)

    def __str__(self):
        return '{}. {}'.format(self.position, self.title)

    def get_absolute_url(self):
        if self.slug:
            return reverse('page', args=[self.slug])
        else:
            return '/'

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Pagina’s'
        ordering = ['position']

class Project(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField(max_length=255)
    tagline = models.CharField(blank=True, max_length=255)
    logo = models.ImageField(blank=True)
    description = RichTextField(blank=True)
    visible_locatie = models.BooleanField('Zichtbaar op de website van De Locatie', blank=True)
    visible_effect = models.BooleanField('Zichtbaar op de website van het Effect Festival', blank=True)
    person = models.ForeignKey(Persoon, verbose_name='persoon', blank=True, null=True)
    entity = models.ForeignKey(Entiteit, verbose_name='partner', related_name='locatie_projecten', blank=True, null=True)
    created = models.DateTimeField('aangemaakt', auto_now_add=True)
    changed = models.DateTimeField('gewijzigd', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Projecten'
        permissions = (
            ("view_project", "Can view project"),
        )

class ProjectPerson(models.Model):
    pass

class ProjectEntity(models.Model):
    pass

class News(models.Model):
    date = models.DateField('datum')
    title = models.CharField('titel', max_length=255)
    image = models.ImageField('afbeelding', blank=True)
    contents = RichTextField('inhoud', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = 'Nieuwsbericht'
        verbose_name_plural = 'Nieuwsberichten'

class Config(models.Model):
    TYPES = [
        (1, 'Footer tekst'),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES)
    content = models.TextField('inhoud')

    class Meta:
        verbose_name = 'Parameter'
        ordering = ['parameter']

class SocialMedia(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    image = models.ImageField('afbeelding')
    hyperlink = models.URLField()

    class Meta:
        verbose_name_plural = 'Social Media'
        ordering = ['position']

class Section(NumberedModel):
    visibility = [
        (1, 'Altijd zichtbaar'),
        (2, 'Alleen op desktop'),
        (3, 'Onzichtbaar'),
    ]
    colors = [
        (1, 'Wit'),
        (2, 'Blauw'),
        (3, 'Blauw-Wit'),
    ]
    types = [
        (1, 'Normaal'),
        (2, 'Agenda smal'),
        (3, 'Agenda breed'),
        (4, 'Partners'),
    ]
    page = models.ForeignKey(Page, verbose_name='pagina', related_name='sections')
    position = models.PositiveIntegerField('positie', blank=True)
    visibility = models.PositiveIntegerField('zichtbaarheid', default=1, choices=visibility)
    #type = models.PositiveIntegerField('soort sectie', default=1, choices=types)
    #color = models.PositiveIntegerField('kleur', default=1, choices=colors)
    title = models.CharField('titel', max_length=255, blank=True)
    contents = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    button = models.CharField('button', max_length=255, blank=True)
    hyperlink = models.URLField(blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return 'Sectie: #{} {}'.format(self.position, self.title)

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']
