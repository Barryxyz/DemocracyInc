# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Registered(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth= models.DateField()
    address = models.CharField(max_length=100)

class PollPlaces(models.Model):
    precinct = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    poll_booths = models.IntegerField()

class VoteRecord(models.Model):
    President = (
        ('Hillary Clinton', 'Hillary Clinton - (D)'),
        ('Donald Trump', 'Donald Trump - (R)'),
        ('Gary Johnson', 'Gary Johnson - (L)')
    )
    president = models.CharField(max_length=50, choices=President)

