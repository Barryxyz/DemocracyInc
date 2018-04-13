from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from .forms import CheckinForm, LoginForm,BallotForm
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
import random, sys
from .models import Voter, Candidate, Vote, Position



# Create your views here.

def home(request):
    return render(request, 'vote/home.html', {})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            firstName = form.cleaned_data.get('first_name')
            lastName = form.cleaned_data.get('last_name')
            conf = form.cleaned_data.get('confirmation')
            voter = Voter.objects.filter(first_name=firstName, last_name=lastName, confirmation=conf)
            if voter:
                HttpResponseRedirect('/ballot')
            else:
                return render(request, 'vote/notregistered.html')
            task.save()  # does nothing, just trigger the validation
    else:
        form = LoginForm()
    return render(request, 'vote/login.html', {'form': form})

def checkin(request):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            confirmation = generator()
            task = form.save(commit=False)
            task.confirmation = confirmation
            task.save()  # does nothing, just trigger the validation
            return render(request, 'vote/confirmation.html', {'key': confirmation})

    else:
        form = CheckinForm()
    return render(request, 'vote/checkin.html', {'form': form})

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key =''

    for i in range(6):
        key+=(''.join(''.join(random.choice(seq))))
    return key

def ballot(request):
    if request.method == 'POST':
        form = BallotForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return render(request, 'vote/vote.html', {'form': form})

            #have a redirect here- new html page needed
        # else:
        return render(request, 'vote/vote.html', {'form': form})
