from django.db import models
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField

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

class Location(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    name = models.CharField('naam', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Locatie'
        ordering = ['position']

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

    class Meta:
        ordering = ['date']
        verbose_name = 'Nieuwsbericht'
        verbose_name_plural = 'Nieuwsberichten'

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
        (3, 'Nieuws klein'),
        (4, 'Nieuws groot'),
        (5, 'Projecten'),
        (6, 'Partners'),
        (7, 'Minisectie'),
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
    hyperlink = models.URLField(blank=True)
    icon = models.ForeignKey('Icon', blank=True, null=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return 'Sectie: #{} {}'.format(self.position, self.title)

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']
