# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from vote import models

class election_types(admin.ModelAdmin):
        model = models.Election
        list_display = ['election_id','type']

class positions(admin.ModelAdmin):
        model = models.Position
        list_display = ['name','election']

class candidate_list(admin.ModelAdmin):
        model = models.Candidate
        list_display = ['full_name','position']

class registered_voters(admin.ModelAdmin):
        model = models.Voter
        list_display = ['voter_number']

class countvotes(admin.ModelAdmin):
        model = models.VoteCount
        list_display = ['position','candidate','count']

class voterecord(admin.ModelAdmin):
        model = models.VoteRecord
        list_display = ['election','position','candidate']

class pollworkers(admin.ModelAdmin):
    model = models.PollWorker
    list_display = ['user_id','precinct_id','locality']

# instantiating all the pages so that they exist in the admin page
admin.site.register(models.Election, election_types)
admin.site.register(models.Position, positions)
admin.site.register(models.Candidate, candidate_list)
admin.site.register(models.Voter, registered_voters)
admin.site.register(models.VoteCount, countvotes)
admin.site.register(models.VoteRecord, voterecord)
admin.site.register(models.PollWorker, pollworkers)
