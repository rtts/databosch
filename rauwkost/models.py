import os
import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField
from maakdenbosch.models import Entiteit, Persoon, LinkType

from django.forms import TextInput
class VarCharField(models.TextField):
    def formfield(self, **kwargs):
        kwargs.update({'widget': TextInput})
        return super().formfield(**kwargs)

class Blog(models.Model):
    active = models.BooleanField('actief', default=False)
    title = VarCharField('titel')
    slug = models.SlugField('URL', help_text='rauwkost.online/nieuws/[URL]', unique=True)
    date = models.DateField('datum', default=datetime.datetime.now)
    program = models.ForeignKey('Program', blank=True, null=True, verbose_name='programma item', related_name='blogs', on_delete=models.PROTECT)
    introduction = models.TextField('introductie', blank=True)
    content = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(help_text='Plak hier een YouTube of Vimeo link', blank=True)

    def get_intro(self):
        return '<p>' + self.introduction + '</p>'

    def get_url(self):
        return reverse('blog', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class Download(models.Model):
    file = models.FileField('bestand')

    def __str__(self):
        return os.path.basename(str(self.file))

    class Meta:
        ordering = ['file']

class NewsItem(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    button = models.CharField(max_length=255, blank=True)
    content = RichTextField()
    image = models.ImageField(blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')

    def get_intro(self):
        return self.content

    def get_url(self):
        return self.url

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'nieuwsbericht'
        verbose_name_plural = 'nieuwsberichten (niet meer gebruiken!)'
        ordering = ['-date']

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
        (5, 'Homepage'),
        (10, 'Normaal'),
        (20, 'Nieuws/Blog'),
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
        (1, 'Consent verzoek (cookiemelding)'),
        (2, 'Consent button tekst'),
        (10, 'Footer midden'),
        (11, 'Footer links'),
        (12, 'Footer rechts'),
        (20, 'Button kleur'),
        (25, 'Extra menu items'),
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

class Edition(models.Model):
    date = models.DateField('datum')
    header = models.FileField('header', blank=True)

    def __str__(self):
        return str(self.date.year)

    class Meta:
        ordering = ['date']

class Location(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    introduction = models.TextField('introductie', blank=True)
    description = RichTextField('beschrijving', blank=True)
    slug = models.SlugField('URL', unique=True, null=True)
    address = models.TextField('adres', blank=True)
    photo = models.ImageField('buitenfoto', blank=True)
    photo_inside = models.ImageField('binnenfoto', blank=True)
    logo = models.ImageField('logo', blank=True)
    icon = models.ImageField('icoon kleur', blank=True)
    iconbw = models.ImageField('icoon zwart/wit', blank=True)
    color = models.PositiveIntegerField('kleur', choices=COLORS)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('location', args=[self.slug])

    class Meta:
        verbose_name = 'Locatie'
        ordering = ['position']

class SubLocation(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    location = models.ForeignKey(Location, related_name='sublocations', on_delete=models.CASCADE)
    title = models.CharField('titel', max_length=255)
    introduction = models.TextField('introductie', blank=True)
    description = RichTextField('beschrijving', blank=True)
    photo = models.ImageField('foto', blank=True)
    logo = models.ImageField('logo', blank=True)
    icon = models.ImageField('icoon kleur', blank=True)
    iconbw = models.ImageField('icoon zwart/wit', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Plek'
        verbose_name_plural = 'Plekken'
        ordering = ['position']

class ProgramType(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    name = models.CharField('naam', max_length=255)
    slug = models.SlugField('URL', unique=True, null=True)
    icon = models.ImageField('icoon', blank=True)

    def __str__(self):
        return self.name

    def get_url(self):
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

class ProgramPartner(models.Model):
    program = models.ForeignKey('Program', related_name='partners', on_delete=models.CASCADE)
    partner = models.ForeignKey(Entiteit, related_name='+', on_delete=models.CASCADE)
    description = RichTextField('site-specifieke beschrijving', help_text='Wanneer je deze beschrijving leeg laat, toont de website de algemene beschrijving van de entiteit', blank=True)

    def __str__(self):
        return str(self.partner)

    def get_description(self):
        if self.description:
            return self.description
        else:
            return self.partner.beschrijving

    class Meta:
        verbose_name = 'partner'
        verbose_name_plural = 'partners'

class Tag(models.Model):
    name = models.SlugField('naam', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

def getedition():
    return Edition.objects.last().pk

def default_date():
    return datetime.date(2020,1,24)

class Program(models.Model):
    active = models.BooleanField('actief', default=True)
    location = models.ForeignKey('Location', verbose_name='locatie', related_name='programs', on_delete=models.PROTECT)
    sublocation = models.ForeignKey(SubLocation, blank=True, null=True, related_name='+', on_delete=models.PROTECT)
    type = models.ForeignKey('ProgramType', verbose_name='soort', related_name='programs', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    edition = models.ForeignKey(Edition, verbose_name='editie', on_delete=models.PROTECT, default=getedition)
    date = models.DateField('datum', default=default_date)
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

    def get_url(self):
        return reverse('program_detail', kwargs={'slug': self.slug, 'year': self.edition.date.year})

    class Meta:
        ordering = ['begin']
        verbose_name = 'Programma item'

class Sponsor(models.Model):
    name = VarCharField()
    icon = models.ImageField()
    hyperlink = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']

class SocialMediaIcon(models.Model):
    type = models.ForeignKey(LinkType, related_name='+', on_delete=models.CASCADE)
    icon = models.ImageField()
    hyperlink = models.URLField(blank=True)

    def __str__(self):
        return self.type.type

    class Meta:
        ordering = ['pk']

class Role(models.Model):
    name = VarCharField('naam')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Teamnaam'
        verbose_name_plural = 'Teamnamen'

class TeamMember(models.Model):
    active = models.BooleanField('actief', default=True)
    editions = models.ManyToManyField(Edition, verbose_name='edities', related_name='+')
    name = VarCharField('naam')
    role = models.ForeignKey(Role, null=True, blank=True, verbose_name='team', related_name='+', on_delete=models.PROTECT)
    function = VarCharField('functie', blank=True)
    email = models.EmailField('email', blank=True)
    phone = VarCharField('telefoonnummer', help_text='dit nummer wordt niet op de site getoond', blank=True)
    description = models.TextField('over jezelf', blank=True)
    photo_bw = models.ImageField('foto zwart/wit', blank=True)
    photo_fc = models.ImageField('foto kleur', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Bendelid'
        verbose_name_plural = 'Bendeleden'
