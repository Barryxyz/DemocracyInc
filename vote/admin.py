# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Voter

class RegisteredPeople(admin.ModelAdmin):
        model = Voter

admin.site.register(Voter, RegisteredPeople)