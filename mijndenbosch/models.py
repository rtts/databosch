from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

class Persoon(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)
    naam = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    telefoonnummer = models.CharField(max_length=32, blank=True)
    beschrijving = RichTextField(blank=True)
    profielfoto = models.ImageField(blank=True)

    def __str__(self):
        return self.naam

    def email_first(self):
        pass;

    def email_more(self):
        pass;

    class Meta:
        verbose_name_plural = 'personen'

class Bijeenkomst(models.Model):
    naam = models.CharField('naam netwerk', max_length=255)
    netwerkhouder = models.ForeignKey(Persoon, related_name='bijeenkomsten')
    datum = models.DateField(blank=True, null=True)
    tijd = models.TimeField(blank=True, null=True)
    locatie = models.CharField('naam locatie', max_length=255, blank=True)
    adres = models.TextField('adres locatie', blank=True)
    besloten = models.BooleanField('dit is een besloten bijeenkomst', default=False)
    deelnemers = models.ManyToManyField(Persoon, related_name='deelnames', blank=True)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name = 'netwerk'
        verbose_name_plural = 'netwerken'

class Taak(models.Model):
    bijeenkomst = models.ForeignKey(Bijeenkomst, verbose_name='netwerk', related_name='taken')
    naam = models.CharField(max_length=255)
    persoon = models.ForeignKey(Persoon, related_name='taken')

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'taken'

class Speerpunt(models.Model):
    woord = models.CharField('In één woord', max_length=32)
    beschrijving = RichTextField(blank=True)
    bijeenkomst = models.ForeignKey(Bijeenkomst, related_name='speerpunten')

    def __str__(self):
        return self.woord

    class Meta:
        ordering = ['woord']
        verbose_name_plural = 'speerpunten'

class Idee(models.Model):
    beschrijving = models.CharField(max_length=255)
    speerpunt = models.ForeignKey(Speerpunt, related_name='ideeen')
    kartrekker = models.ForeignKey(Persoon, related_name='kartrekker_van', blank=True, null=True)
    initiatiefnemers = models.ManyToManyField(Persoon, related_name='initiatiefnemer_van', blank=True)

    def __str__(self):
        return self.beschrijving

    class Meta:
        ordering = ['beschrijving']
        verbose_name_plural = 'ideeën'

class Nieuwsbericht(models.Model):
    datum = models.DateField()
    titel = models.CharField(max_length=255)
    inhoud = RichTextField(blank=True)

    class Meta:
        ordering = ['-datum']
        verbose_name_plural = 'nieuwsberichten'
