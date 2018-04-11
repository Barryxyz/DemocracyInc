from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from .forms import CheckinForm, LoginForm
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
import random, sys


# Create your views here.

def home(request):
    return render(request, 'vote/home.html', {})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()  # does nothing, just trigger the validation
            return render(request, 'vote/confirmation.html', {'key': generator()})
    else:
        form = LoginForm()
    return render(request, 'vote/login.html', {'form': form})

def checkin(request):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()  # does nothing, just trigger the validation
            return render(request, 'vote/confirmation.html', {'key': generator()})

    else:
        form = CheckinForm()
    return render(request, 'vote/checkin.html', {'form': form})

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key =''

    for i in range(6):
        key+=(''.join(''.join(random.choice(seq))))
    return key
