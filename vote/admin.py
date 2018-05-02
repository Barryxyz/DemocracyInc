# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Election, Position, Candidate, VoteRecord, VoteCount, Voter

class election_types(admin.ModelAdmin):
        model = Election
        list_display = ['election_id','type']

class positions(admin.ModelAdmin):
        model = Position
        list_display = ['election','name']

class candidate_list(admin.ModelAdmin):
        model = Candidate
        list_display = ['full_name','position']

class registered_voters(admin.ModelAdmin):
        model = Voter
        list_display = ['voter_number']

class countvotes(admin.ModelAdmin):
        model = VoteCount
        list_display = ['position','candidate','count']

class voterecord(admin.ModelAdmin):
        model = VoteRecord
        list_display = ['election','position','candidate']

# instantiating all the pages so that they exist in the admin page
admin.site.register(Election, election_types)
admin.site.register(Position, positions)
admin.site.register(Candidate, candidate_list)
admin.site.register(Voter, registered_voters)
admin.site.register(VoteCount, countvotes)
admin.site.register(VoteRecord, voterecord)
