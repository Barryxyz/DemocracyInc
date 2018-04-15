# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import VoteForm,RegisteredForm,VoteIdCheckForm
from .models import Registered
from .models import CheckedIn
from django.contrib.auth.decorators import login_required
import random, string


# Create your views here.

cache = {}

#@login_required
def home(request):
    return render(request, 'base.html', {})

def login(request):
    return render(request, 'login.html', {})
	
def logout_page(request):
    return render(request, 'registration/logout_success.html', {})

def reset(request):
	return render(request, 'registration/password_reset_form.html', {})

@login_required	
def view_voters(request):
	query_results = Registered.objects.all()
	return render(request, 'view_voters.html', {'query_results': query_results})

@login_required
def checkin(request):
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
                cache['first_name'] = form.cleaned_data['first_name']
                cache['last_name'] = form.cleaned_data['last_name']
                cache['address'] = form.cleaned_data['address']
                cache['date_of_birth'] = form.cleaned_data['date_of_birth']
                cache['Locality'] = form.cleaned_data['locality']
                return HttpResponseRedirect('/checkin_success')
				
            else:
                return HttpResponseRedirect('/notregistered')

            # redirect to a new URL:
            return HttpResponseRedirect('/checkin_success')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisteredForm()
    return render(request, 'checkin.html', {'form': form})

def vote(request):

    voter_info = CheckedIn.objects.filter(confirm_key=cache['in_key'])
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
    return render(request, 'vote.html', {'form': form,'voter_info': voter_info})

def vote_id_check(request):
    
    isNotCheckedIn = False
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VoteIdCheckForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            input_key = form.cleaned_data['vote_id']
            check = CheckedIn.objects.filter(confirm_key=input_key)
            if check.exists():
                cache['in_key'] = input_key
                return HttpResponseRedirect('/vote')
            else:
                isNotCheckedIn = True
                return render(request, 'vote_id_check.html', {'form': form, 'isNotCheckedIn':isNotCheckedIn})
        else:
            return HttpResponseRedirect('/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoteIdCheckForm()
    return render(request, 'vote_id_check.html', {'form': form, 'isNotCheckedIn':isNotCheckedIn})

@login_required
def booth_assignment(request):
    boothkeys = ['rFKeel', 'tOLpZV', 'pldygS']

    key = generator()
    cache['booth'] = key
	
    check = CheckedIn.objects.filter(first_name=cache['first_name'],
        last_name=cache['last_name'],
        date_of_birth=cache['date_of_birth'],
		address=cache['address'],
        locality=cache['Locality'])

    if check.exists():
	    check.update(confirm_key=key)
		
    else :	
        foo_instance = CheckedIn.objects.create(first_name=cache['first_name'],
        last_name=cache['last_name'],
        date_of_birth=cache['date_of_birth'],
		address=cache['address'],
        locality=cache['Locality'],
		confirm_key=key)

    #key = 'WAHOOWA' # hardcode a key for demo purposes
    return render(request, 'booth_assignment.html', cache)

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key =''

    for i in range(6):
        key+=(''.join(''.join(random.choice(seq))))
    return key

@login_required
def notregistered(request):
    return render(request, 'notregistered.html', {})

