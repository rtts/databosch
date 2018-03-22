from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField
from maakdenbosch.models import Entiteit, Persoon, LinkType

class NewsItem(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'nieuwsbericht'
        verbose_name_plural = 'nieuwsberichten'

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

class Section(NumberedModel):
    types = [
        (10, 'Normaal'),
        (20, 'Nieuwsberichten'),
    ]
    page = models.ForeignKey(Page, verbose_name='pagina', related_name='sections', on_delete=models.CASCADE)
    type = models.PositiveIntegerField('soort sectie', default=10, choices=types)
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    content = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    button = models.CharField('button', blank=True, max_length=255)
    hyperlink = models.CharField(max_length=255, blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']

class Config(models.Model):
    TYPES = [
        (10, 'Footer midden'),
        (11, 'Footer links'),
        (12, 'Footer rechts'),
        (20, 'Homepage header'),
        (30, 'Extra CSS'),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES, unique=True)
    content = models.TextField('inhoud', blank=True)
    image = models.FileField('bestand', blank=True)

    def __str__(self):
        return "{}. {}".format(self.parameter, self.get_parameter_display())

    class Meta:
        verbose_name = 'Parameter'
        ordering = ['parameter']

COLORS = [
    (1, 'Groen'),
    (2, 'Oranje'),
    (3, 'Geel'),
    (4, 'Roze'),
    (5, 'Paars'),
    (6, 'Blauw'),
    (7, 'Turquoise'),
    (8, 'Grijs'),
    (9, 'Rood'),
    (10, 'Bruin'),
]

class Location(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField('URL', unique=True, null=True)
    address = models.TextField('adres', blank=True)
    photo = models.ImageField('foto', blank=True)
    logo = models.ImageField('logo', blank=True)
    icon = models.ImageField('icoon kleur', blank=True)
    iconbw = models.ImageField('icoon zwart/wit', blank=True)
    color = models.PositiveIntegerField('kleur', choices=COLORS)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('location', args=[self.slug])

    class Meta:
        verbose_name = 'Locatie'
        ordering = ['position']

class ProgramType(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    name = models.CharField('naam', max_length=255)
    slug = models.SlugField('URL', unique=True, null=True)
    icon = models.ImageField('icoon', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('type', args=[self.slug])

    class Meta:
        ordering = ['position']
        verbose_name = 'soort'
        verbose_name_plural = 'soorten'

class ProgramHyperlink(models.Model):
    type = models.ForeignKey(LinkType, related_name='+', on_delete=models.CASCADE)
    url = models.URLField('URL')
    program = models.ForeignKey('Program', related_name='hyperlinks', on_delete=models.CASCADE)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'hyperlink'

class ProgramPhoto(models.Model):
    image = models.ImageField('afbeelding')
    program = models.ForeignKey('Program', related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = 'foto'
        verbose_name_plural = 'foto’s'

class ProgramVideo(models.Model):
    video = EmbedVideoField(blank=True)
    program = models.ForeignKey('Program', related_name='videos', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.video)

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'video’s'

class Program(models.Model):
    active = models.BooleanField('actief', default=True)
    location = models.ForeignKey('Location', verbose_name='locatie', related_name='programs', on_delete=models.CASCADE)
    type = models.ForeignKey('ProgramType', verbose_name='soort', related_name='programs', on_delete=models.CASCADE)
    begin = models.TimeField('begintijd')
    end = models.TimeField('eindtijd')
    title = models.CharField('titel', max_length=255)
    tagline = models.CharField('ondertitel', max_length=255)
    slug = models.SlugField()
    thumbnail = models.ImageField('thumbnail', blank=True)
    short_description = models.TextField('korte beschrijving', blank=True)
    long_description = RichTextField('lange beschrijving', blank=True)
    video = EmbedVideoField(blank=True)
    ticketlink = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('program_detail', args=[self.slug])

    class Meta:
        ordering = ['begin']
        verbose_name = 'Programma item'

class SocialMediaIcon(models.Model):
    type = models.ForeignKey(LinkType, related_name='+', on_delete=models.CASCADE)
    icon = models.ImageField()
    hyperlink = models.URLField(blank=True)

    def __str__(self):
        return self.type.type

    class Meta:
        ordering = ['pk']
