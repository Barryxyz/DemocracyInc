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
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))"""

from django.conf.urls import url
from vote import views
from VotingApp import settings
from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    # url('^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
	url(r'^logout_page/', views.logout_page, name='logout_page'),
	url(r'^password_reset/$',views.reset, name='reset_pass'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^vote_id_check/', views.vote_id_check, name='vote_id_check'),
    url(r'^checkin/', views.checkin, name='checkin'),
    # url(r'^notregistered/', views.notregistered, name='notregistered'),
    # url(r'^checkin_success/', views.booth_assignment, name='success'),
	url(r'^view_voters/', views.view_voters, name='view_voters'),
    url(r'^vote_count/', views.vote_count, name='vote_count')
]


#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'accounts/', include('django.contrib.auth.urls')),
]