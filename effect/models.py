from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField
from maakdenbosch.models import Entiteit, LinkType

class Page(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    header = models.ForeignKey('Header')
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
        (1, 'Footer tekst'),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES)
    content = models.TextField('inhoud')

    class Meta:
        verbose_name = 'Parameter'
        ordering = ['parameter']

class Icon(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    image = models.ImageField('afbeelding')
    name = models.CharField('naam', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']

class Header(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    image = models.ImageField('afbeelding')
    name = models.CharField('naam', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']

class Location(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    name = models.CharField('naam', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Locatie'
        ordering = ['position']

class ProgramHyperlink(models.Model):
    type = models.ForeignKey(LinkType)
    url = models.URLField('URL')
    program = models.ForeignKey('Program', related_name='hyperlinks')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'hyperlink'

class Program(models.Model):
    visible_in_timetable = models.BooleanField('zichtbaar in blokkenschema', blank=True)
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField()
    tagline = models.CharField(max_length=255)
    description = RichTextField('beschrijving', blank=True)
    location = models.ForeignKey('Location', verbose_name='locatie', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Programmaonderdeel'
        verbose_name_plural = 'Programmaonderdelen'

class News(models.Model):
    date = models.DateField('datum')
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField()
    image = models.ImageField('foto', blank=True)
    content = RichTextField('inhoud', blank=True)
    project = models.ForeignKey('Project', blank=True, null=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Nieuwsbericht'
        verbose_name_plural = 'Nieuwsberichten'

class Partnership(models.Model):
    project = models.ForeignKey('Project', related_name='partnerships')
    partner = models.ForeignKey(Entiteit)

    def __str__(self):
        return str(self.partner)

class Project(models.Model):
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField()
    image = models.ImageField('foto', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    content = RichTextField('inhoud', blank=True)
    entity = models.ForeignKey(Entiteit, verbose_name='bestaande entiteit', help_text='Kies hier de DataBosch entiteit die dit project vertegenwoordigt', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Projecten'

class ProjectPhoto(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    image = models.ImageField('high-res origineel')
    caption = models.CharField('bijschrift', max_length=255)
    project = models.ForeignKey('Project', related_name='photos')

    def __str__(self):
        return self.caption

    def order_with_respect_to(self):
        return self.project.photos.all()

    class Meta:
        ordering = ['position']
        verbose_name = 'Foto'

class Partner(models.Model):
    name = models.CharField('naam', max_length=255)
    logo = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('naam', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class TimeSlot(models.Model):
    program = models.ForeignKey('Program')
    begin = models.DateTimeField('begintijd')
    end = models.DateTimeField('eindtijd')

    def __str__(self):
        return 'Van {} tot {}'.format(self.begin, self.end)

class SocialMedia(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    name = models.CharField('Naam', max_length=255)
    image = models.ImageField('afbeelding')
    hyperlink = models.URLField()

    def __str__(self):
        return self.name

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
        (2, 'Oranje'),
        (3, 'Groen'),
    ]
    types = [
        (1, 'Normaal'),
        (2, 'Video'),
        # (3, 'Nieuws klein'),
        (4, 'Nieuws'),
        (5, 'Projecten'),
        (6, 'Partners'),
        (7, 'Foto'),
    ]
    page = models.ForeignKey(Page, verbose_name='pagina', related_name='sections')
    position = models.PositiveIntegerField('positie', blank=True)
    visibility = models.PositiveIntegerField('zichtbaarheid', default=1, choices=visibility)
    type = models.PositiveIntegerField('soort sectie', default=1, choices=types)
    color = models.PositiveIntegerField('kleur', default=1, choices=colors)
    title = models.CharField('titel', max_length=255, blank=True)
    contents = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    button = models.CharField('button', max_length=255, blank=True)
    hyperlink = models.CharField(max_length=255, blank=True)
    icon = models.ForeignKey('Icon', blank=True, null=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return '{}. {}: {}'.format(self.position, self.get_type_display(), self.title)

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']
