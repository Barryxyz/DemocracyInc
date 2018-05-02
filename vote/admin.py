# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Election, Position, Candidate, VoteRecord, VoteCount, Voter

class election_types(admin.ModelAdmin):
        model = Election

class positions(admin.ModelAdmin):
        model = Position

class candidate_list(admin.ModelAdmin):
        model = Candidate

class registered_voters(admin.ModelAdmin):
        model = Voter

class countvotes(admin.ModelAdmin):
        model = VoteCount

class voterecord(admin.ModelAdmin):
        model = VoteRecord


# instantiating all the pages so that they exist in the admin page
admin.site.register(Election, election_types)
admin.site.register(Position, positions)
admin.site.register(Candidate, candidate_list)
admin.site.register(Voter, registered_voters)
admin.site.register(VoteCount, countvotes)
admin.site.register(VoteRecord, voterecord)
