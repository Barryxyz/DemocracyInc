from django.contrib import admin
from .models import Voter, Candidate, Vote, Position


# Register your models here.

myModels = [Voter, Candidate, Vote, Position]

admin.site.register(myModels)
