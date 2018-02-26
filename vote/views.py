# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'vote/base.html', {})

def login(request):
    return render(request, 'vote/login.html', {})
