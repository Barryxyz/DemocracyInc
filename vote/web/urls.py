"""VotingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from ..web import views
from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
    url(r'^/', views.home, name='base'),
    url(r'^home/', views.home, name='home'),
    url(r'^checkin/', views.checkin, name="checkin"),
    url(r'^confirmation/', views.generator, name="generator"),
    url(r'^login/', views.login, name="login"),
    # url(r'^vote/', views.vote, name='vote'),
    # url(r'^notregistered/', views.notregistered, name='notregistered'),
    # url(r'^booth/', views.booth_assignment, name='booth')
]
