# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Voter, PollPlaces, VoteRecord, VoteCount

class registered_voters(admin.ModelAdmin):
        model = Voter

class pollplaces(admin.ModelAdmin):
        model = PollPlaces

class voterecord(admin.ModelAdmin):
        model = VoteRecord

class countvotes(admin.ModelAdmin):
        model = VoteCount



admin.site.register(Voter, registered_voters)
admin.site.register(PollPlaces, pollplaces)
admin.site.register(VoteRecord, voterecord)
admin.site.register(VoteCount, countvotes)