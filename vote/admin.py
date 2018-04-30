# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Voter, PollPlace, VoteRecord, VoteCount, General_VoteRecord, Primary_VoteRecord

class registered_voters(admin.ModelAdmin):
        model = Voter

class pollplaces(admin.ModelAdmin):
        model = PollPlace

class voterecord(admin.ModelAdmin):
        model = VoteRecord

class countvotes(admin.ModelAdmin):
        model = VoteCount

class general_election(admin.ModelAdmin):
        model = General_VoteRecord

class primary_election(admin.ModelAdmin):
        model = Primary_VoteRecord



admin.site.register(Voter, registered_voters)
admin.site.register(PollPlace, pollplaces)
admin.site.register(VoteRecord, voterecord)
admin.site.register(VoteCount, countvotes)
admin.site.register(General_VoteRecord, general_election)
admin.site.register(Primary_VoteRecord, primary_election)
