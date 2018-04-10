from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from .forms import CheckinForm, LoginForm
from .models import Voter
import random, sys

# Create your views here.

def home(request):
    return render(request, 'vote/home.html', {})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            voter = Voter.objects.get(first_name=task.first_name, last_name=task.last_name)
            if (task.confirmation == voter.confirmation):
                voter_id = generator()
                voter.voter_id = voter_id
                voter.save()
                return render(request, 'vote/confirmation.html', {'key': voter_id})
            else:
                return render(request, 'vote/notregistered.html', {})
    else:
        form = LoginForm()
    return render(request, 'vote/login.html', {'form': form})

def checkin(request):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            confirmation_number = generator()
            task.confirmation = confirmation_number
            task.save()  # does nothing, just trigger the validation
            return render(request, 'vote/confirmation.html', {'key': confirmation_number})

    else:
        form = CheckinForm()
    return render(request, 'vote/checkin.html', {'form': form})

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key =''

    for i in range(6):
        key+=(''.join(''.join(random.choice(seq))))
    return key