# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import VoteForm,RegisteredForm,VoteIdCheckForm
from .models import Registered
import random, string


# Create your views here.

cache = {}

def home(request):
    return render(request, 'vote/base.html', {})

def login(request):
    return render(request, 'vote/login.html', {})

def django_checkin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisteredForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            voter_registered = Registered.objects.filter(first_name=form.cleaned_data['first_name'],
                                                      last_name=form.cleaned_data['last_name'],
                                                      date_of_birth=form.cleaned_data['date_of_birth'],
                                                      address=form.cleaned_data['address'],
                                                      locality=form.cleaned_data['locality']).exists()
            if voter_registered:
                cache['full_name'] = form.cleaned_data['last_name'] + ", " + form.cleaned_data['first_name']
                cache['date_of_birth'] = form.cleaned_data['date_of_birth']
                cache['Locality'] = form.cleaned_data['locality']
                return HttpResponseRedirect('/booth')
				
            else:
                return HttpResponseRedirect('/notregistered')

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

def vote_id_check(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VoteIdCheckForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data['vote_id'] == 'WAHOOWA':
                # redirect to a new URL:
                return HttpResponseRedirect('/vote')
            else:
                return HttpResponseRedirect('/vote_id_check')
        else:
            return HttpResponseRedirect('/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoteIdCheckForm()
    return render(request, 'vote/vote_id_check.html', {'form': form})

def booth_assignment(request):
    boothkeys = ['rFKeel', 'tOLpZV', 'pldygS']

    while True:
        key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))
        if not key in boothkeys:
            break
    #print(most_recent_data[0])
    cache['booth'] = key

    key = 'WAHOOWA' # hardcode a key for demo purposes
    return render(request, 'vote/booth_assignment.html', {'booth': key})


def notregistered(request):
    return render(request, 'vote/notregistered.html', {})

