# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Voter, PollWorker, VoteCount, VoteRecord, Election

class registered_voters(admin.ModelAdmin):
        model = Voter

class pollworkers(admin.ModelAdmin):
        model = PollWorker

class elections(admin.ModelAdmin):
        model = Election

class countvotes(admin.ModelAdmin):
        model = VoteCount

class voterecord(admin.ModelAdmin):
        model = VoteRecord


# instantiating all the pages so that they exist in the admin page
admin.site.register(Voter, registered_voters)
admin.site.register(PollWorker, pollworkers)
admin.site.register(Election, elections)
admin.site.register(VoteCount, countvotes)
admin.site.register(VoteRecord, voterecord)
