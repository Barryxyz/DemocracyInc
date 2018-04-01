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