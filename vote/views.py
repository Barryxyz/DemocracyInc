# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Voter, VoteRecord
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import VoteForm,VoteIdCheckForm,RegisteredForm,LoginForm

import random
from graphos.sources.simple import SimpleDataSource
from graphos.renderers import morris


# Create your views here.

def home(request):
    return render(request, 'base.html', {})

def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            valid_pollworker = User.objects.filter(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            ).exists()

            if valid_pollworker:
                return redirect(reverse('vote_id_check'))
            else:
                return redirect(reverse('home'))
            # process the data in form.cleaned_data as required
            # redirect to a new URL:

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    return render(request, './registration/login.html', {'form': form})

def logout_page(request):
    return render(request, 'registration/logout_success.html', {})

def reset(request):
	return render(request, 'registration/password_reset_form.html', {})

@login_required	
def view_voters(request):
	query_results = Voter.objects.all()
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
            voter_registered = Voter.objects.filter(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                locality=form.cleaned_data['locality']
            ).exists()

            if voter_registered:
                task = form.save(commit=False)
                key = generator()
                full_name = task.first_name + " " + task.last_name
                locality = task.locality
                task.confirmation = key
                task.save()
                return render(request, 'booth_assignment.html', {'booth': key, 'full_name': full_name, 'locality': locality})

            else:
                return render(request, 'notregistered.html', {})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisteredForm()
    return render(request, 'checkin.html', {'form': form})

def vote(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VoteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            voter = Voter.objects.get(confirmation=request.session['input_key'])
            task = form.save(commit=False)
            task.voter = voter
            task.save()
            # redirect to a new URL:
            return redirect(reverse('home'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoteForm()
    return render(request, 'vote.html', {'form': form})

def vote_id_check(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VoteIdCheckForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            input_key = form.cleaned_data['vote_id']
            valid_key = Voter.objects.filter(confirmation=input_key).exists()
            if valid_key:
                request.session['input_key'] = input_key
                return redirect(reverse('vote'))
            else:
                return render(request, 'vote_id_check.html', {'form': form}) # need an error page?
        else:
            return redirect(reverse('home'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoteIdCheckForm()
    return render(request, 'vote_id_check.html', {'form': form})

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key = ''

    for i in range(6):
        key+=(''.join(''.join(random.choice(seq))))
    return key


def vote_count(request):
    # VoteRecord.objects.filter()
    # VoteRecord.objects.filter(president="Hillary Clinton")
    # presidents = VoteRecord.objects.annotate(Count('president'))
    prez_count = VoteRecord.objects.filter(president='Gary Johnson').count()
    prez_count2 = VoteRecord.objects.filter(president='Donald Trump').count()
    # data = [
    #     ['President','Count'],
    #     ['Gary Johnson', prez_count],
    #     ['Donald Trump', prez_count2]
    # ]
    data = [
        ['Year', 'Sales'],
        [2004, 1000],
        [2005, 1170],
        [2006, 660],
        [2007, 1030]
    ]
    # queryset = VoteRecord.objects.all()
    # data_source = ModelDataSource(queryset, fields=['president', 'count'])  # x-axis = presidet, y-axis = count
    # chart = gchart.BarChart(data_source, options={'title': "Election Results", 'xaxis': {'mode': "Count"}})
    data_source = SimpleDataSource(data=data)
    chart = morris.LineChart(data_source, options={'title': "Line Chart"},html_id='gchart_div')
    return render(request,'vote_count.html', {'chart': chart})
