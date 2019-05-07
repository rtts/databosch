import os
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField
from maakdenbosch.models import Entiteit, Persoon, LinkType

class Download(models.Model):
    file = models.FileField('bestand')

    def __str__(self):
        return os.path.basename(str(self.file))

    class Meta:
        ordering = ['file']

class Page(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    header = models.ForeignKey('Header', on_delete=models.CASCADE)
    mobile_header = models.ForeignKey('Header', related_name='+', on_delete=models.CASCADE)
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
    type = models.ForeignKey(LinkType, related_name='+', on_delete=models.CASCADE)
    url = models.URLField('URL')
    program = models.ForeignKey('Program', related_name='hyperlinks', on_delete=models.CASCADE)

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
    location = models.ForeignKey('Location', verbose_name='locatie', blank=True, on_delete=models.CASCADE)
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
    url = models.URLField('URL', help_text='Plak hier een externe link naar het nieuwsbericht', blank=True)
    content = RichTextField('inhoud', blank=True)
    project = models.ForeignKey('Project', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Nieuwsbericht'
        verbose_name_plural = 'Nieuwsberichten'

class Event(models.Model):
    date = models.DateField('datum')
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField('foto', blank=True)
    content = RichTextField('inhoud', blank=True)
    project = models.ForeignKey('Project', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Agenda-item'
        verbose_name_plural = 'Agenda-items'

class Partnership(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    project = models.ForeignKey('Project', related_name='partnerships', on_delete=models.CASCADE)
    partner = models.ForeignKey(Entiteit, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.partner)

    def number_with_respect_to(self):
        return self.project.partnerships.all()

    class Meta:
        ordering = ['position']

class Project(models.Model):
    title = models.CharField('titel', max_length=255)
    subtitle = models.CharField('onndertitel', max_length=255, blank=True)
    slug = models.SlugField()
    active = models.BooleanField('actief', default=True)
    image = models.ImageField('foto', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    content = RichTextField('inhoud', blank=True)
    entity = models.ForeignKey(Entiteit, verbose_name='bestaande entiteit', help_text='Kies hier de DataBosch entiteit die dit project vertegenwoordigt', blank=True, null=True, related_name='+', on_delete=models.CASCADE)
    person = models.ForeignKey(Persoon, related_name='+', verbose_name='projectleider', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Projecten'

class ProjectPhoto(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    image = models.ImageField('high-res origineel')
    project = models.ForeignKey('Project', related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return '#{}'.format(self.position)

    def number_with_respect_to(self):
        return self.project.photos.all()

    class Meta:
        ordering = ['position']
        verbose_name = 'Foto'

class Certification(models.Model):
    name = models.CharField('naam', max_length=255)
    logo = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Keurmerk/Certificatie'
        verbose_name_plural = 'Keurmerken en Certificaties'

class Partner(models.Model):
    name = models.CharField('naam', max_length=255)
    logo = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fonds'
        verbose_name_plural = 'Fondsen'

class Sponsor(models.Model):
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
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
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
        # (8, 'Formulier'),
        (9, 'Agenda'),
    ]
    page = models.ForeignKey(Page, verbose_name='pagina', related_name='sections', on_delete=models.CASCADE)
    position = models.PositiveIntegerField('positie', blank=True)
    visibility = models.PositiveIntegerField('zichtbaarheid', default=1, choices=visibility)
    type = models.PositiveIntegerField('soort sectie', default=1, choices=types)
    show_certifications = models.BooleanField('laat keurmerken en certificaties zien in deze partnersectie', default=False)
    show_partners = models.BooleanField('laat fondsen zien in deze partnersectie', default=False)
    show_sponsors = models.BooleanField('laat sponsors zien in deze partnersectie', default=False)
    show_partnerships = models.BooleanField('laat alle projectpartners zien in partnersectie', default=False)
    color = models.PositiveIntegerField('kleur', default=1, choices=colors)
    title = models.CharField('titel', max_length=255, blank=True)
    contents = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    button = models.CharField('button', max_length=255, blank=True)
    hyperlink = models.CharField(max_length=255, blank=True)
    icon = models.ForeignKey('Icon', blank=True, null=True, on_delete=models.CASCADE)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return '{}. {}: {}'.format(self.position, self.get_type_display(), self.title)

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']
