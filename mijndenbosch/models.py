from django.db import models
from django.conf import settings

class Bijeenkomst(models.Model):
    naam = models.CharField('naam netwerk', max_length=255)
    datum = models.DateTimeField(blank=True)
    locatie = models.CharField('naam locatie', max_length=255, blank=True)
    adres = models.TextField('adres locatie', blank=True)
    latitude = models.DecimalField('noorderbreedte', max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField('oosterlengte', max_digits=9, decimal_places=6, blank=True, null=True)
    netwerkhouder = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='netwerkhouder_at', blank=True)
    gespreksleider = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='gespreksleider_at', blank=True, null=True)
    notulist = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notulist_at', blank=True, null=True)
    twitteraar = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='twitteraar_at', blank=True, null=True)
    fotograaf = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fotograaf_at', blank=True, null=True)
    camera = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='camera_at', blank=True, null=True)
    deelnemers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='deelnemer_at', blank=True)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'bijeenkomsten'

class Speerpunt(models.Model):
    beschrijving = models.CharField(max_length=255)
    woord = models.CharField('In één woord', max_length=32)
    bijeenkomst = models.ForeignKey(Bijeenkomst, related_name='speerpunten')

    def __str__(self):
        return self.woord

    class Meta:
        ordering = ['woord']
        verbose_name_plural = 'speerpunten'

class Idee(models.Model):
    beschrijving = models.CharField(max_length=255)
    speerpunt = models.ForeignKey(Speerpunt, related_name='ideeen')
    deelnemers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='ideeen', blank=True)

    def __str__(self):
        return self.beschrijving

    class Meta:
        ordering = ['beschrijving']
        verbose_name_plural = 'ideeën'
