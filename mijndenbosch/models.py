from django.db import models
from django.conf import settings

class Bijeenkomst(models.Model):
    naam = models.CharField(max_length=255)
    datum = models.DateTimeField(blank=True)
    adres = models.TextField(blank=True)
    organisator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='georganiseerde_bijeenkomsten', blank=True)
    deelnemers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bijeenkomsten', blank=True)

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
