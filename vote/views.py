# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Voter, VoteRecord, Election, VoteCount

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import VoteForm, VoteIdCheckForm, RegisteredForm, LoginForm
from graphos.renderers import gchart
from graphos.renderers.gchart import BarChart
from graphos.sources.simple import SimpleDataSource
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import VoteForm, VoteIdCheckForm, RegisteredForm, LoginForm
from rest_framework import viewsets
from .serializers import CountSerializer, RecordSerializer
from django.shortcuts import render, HttpResponse
import random, json, requests



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

def view_elections(request):
	query_results = Election.objects.all()
	return render(request, 'view_elections.html', {'query_results': query_results})

@login_required
def view_voters(request):
    query_results = Voter.objects.all()
    return render(request, 'view_voters.html', {'query_results': query_results})


@login_required
def view_elections(request):
	# query_results = Election.objects.all()
    query_results = []
    query_results.append(Election(type='primary', id='ljsadlkfj'))
    query_results.append(Election(type='presidential', id='ljsadlkfj'))
    return render(request, 'view_elections.html', {'query_results': query_results})

@login_required	
def view_voters(request):
	query_results = Voter.objects.all()
	return render(request, 'view_voters.html', {'query_results': query_results})
    # results = requests.get('http://cs3240votingproject.org/voters/?key={API_KEY}')
    # content = results.text
    # return HttpResponse(content)
    # return render(request, 'view_voters.html', {'results': results})

@login_required
def checkin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisteredForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            registered_voter = Voter.objects.get(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                locality=form.cleaned_data['locality']
            )

            if registered_voter:
                task = form.save(commit=False)
                key = generator()
                full_name = task.first_name + " " + task.last_name
                locality = task.locality
                task.confirmation = key
                task.save()
                return render(request, 'booth_assignment.html',
                              {'booth': key, 'full_name': full_name, 'locality': locality})
                registered_voter.confirmation = key
                registered_voter.save()
                # task.confirmation = key
                # task.save(update_fields=['confirmation'])
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
                return render(request, 'vote_id_check.html', {'form': form})  # need an error page?
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
        key += (''.join(''.join(random.choice(seq))))
    return key

@login_required
def vote_count(request):
    records = VoteRecord.objects.all()
    votes = dict()
    positions = dict()
    for vr in records:
        key = vr.president
        if key in votes:
            votes[key] += 1
            positions[key].add('president')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('president')

@login_required
def vote_count(request):
    records = VoteRecord.objects.all()
    votes = dict()
    positions = dict()
    for vr in records:
        key = vr.president
        if key in votes:
            votes[key] += 1
            positions[key].add('president')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('president')

        key = vr.governor
        if key in votes:
            votes[key] += 1
            positions[key].add('governor')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('governor')

        key = vr.lieutenant_Governor
        if key in votes:
            votes[key] += 1
            positions[key].add('lieutenant_Governor')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('lieutenant_Governor')

        key = vr.attorney_General
        if key in votes:
            votes[key] += 1
            positions[key].add('attorney_General')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('attorney_General')

        key = vr.delegate
        if key in votes:
            votes[key] += 1
            positions[key].add('delegate')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('delegate')

        key = vr.commonwealth_Attorney
        if key in votes:
            votes[key] += 1
            positions[key].add('votes')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('votes')

        key = vr.sheriff
        if key in votes:
            votes[key] += 1
            positions[key].add('sheriff')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('sheriff')

        key = vr.treasurer
        if key in votes:
            votes[key] += 1
            positions[key].add('treasurer')
        else:
            votes[key] = 1
            positions[key] = set()
            positions[key].add('treasurer')

    results = []
    for name in votes.keys():
        for position in positions[name]:
            results.append(VoteCount(name=name, position=position, count=str(votes[name])))

    return render(request, 'vote_count.html', {'query_results': results})

@login_required
def results(request):
    prez_count = VoteRecord.objects.filter(president='Gary Johnson').count()
    prez_count2 = VoteRecord.objects.filter(president='Hillary Clinton').count()
    president_data = [
        ['Candidates','Count'],
        ['Gary Johnson', prez_count],
        ['Hillary Clinton', prez_count2]
    ]
    gov_count = VoteRecord.objects.filter(governor='Matthew Ray').count()
    gov_count2 = VoteRecord.objects.filter(governor='Travis Bailey').count()
    gov_count3 = VoteRecord.objects.filter(governor='Marisha Miller').count()

class CountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = VoteCount.objects.all()
    serializer_class = CountSerializer


class RecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = VoteRecord.objects.all()
    serializer_class = RecordSerializer
