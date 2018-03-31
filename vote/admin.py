# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Registered,PollPlaces

class RegisteredPeople(admin.ModelAdmin):
        model = Registered

admin.site.register(Registered, RegisteredPeople)