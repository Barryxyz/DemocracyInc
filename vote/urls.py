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
from vote import views
from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^vote_id_check/', views.vote_id_check, name='vote_id_check'),
    url(r'^django_checkin/', views.django_checkin, name='django_checkin'),
    url(r'^notregistered/', views.notregistered, name='notregistered'),
    url(r'^booth/', views.booth_assignment, name='booth')
]
