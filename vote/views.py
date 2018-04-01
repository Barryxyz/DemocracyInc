# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import VoteForm,RegisteredForm
import random
import string

# Create your views here.

def home(request):
    return render(request, 'vote/base.html', {})

def login(request):
    return render(request, 'vote/login.html', {})

# def checkin(request):
#     return render(request, 'vote/checkin.html', {})

def checkin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisteredForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/booth')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisteredForm()
    return render(request, 'vote/django_checkin.html', {'form': form})

def vote(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VoteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoteForm()
    return render(request, 'vote/vote.html', {'form': form})

def booth_assignment(request):
    boothkeys = ['rFKeel', 'tOLpZV', 'pldygS']

    while True:
        key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))
        if not key in boothkeys:
            break

    return render(request, 'vote/booth_assignment.html', {'booth': key})


def notregistered(request):
    return render(request, 'vote/notregistered.html', {})

