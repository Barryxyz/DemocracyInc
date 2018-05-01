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

from django.contrib import admin
from django.conf.urls import url, include

from rest_framework import routers
from vote import views

# url links for API
router = routers.DefaultRouter()
router.register(r'^/', views.electionViewSet)
router.register(r'^/2017-11', views.generalViewSet)
router.register(r'^/2017-06', views.primaryViewSet)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/=', admin.site.urls),
    url(r'^load_voters/', views.load_voters, name='load_voters'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout_page/', views.logout_page, name='logout_page'),
    url(r'^password_reset/$',views.reset, name='reset_pass'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^vote_id_check/', views.vote_id_check, name='vote_id_check'),
    url(r'^checkin/', views.checkin, name='checkin'),
    url(r'^view_voters/', views.view_voters, name='view_voters'),
    url(r'^view_election/', views.view_elections, name='view_elections'),
    url(r'^vote_count/', views.vote_count, name='vote_count'),
    url(r'^general_results/', views.general_results, name='general_results'),
    url(r'^primary_results/', views.primary_results, name='primary_results'),
    url(r'^alreadyvoted/', views.already_voted, name='already_voted'),
    url(r'^inactive/', views.inactive, name='inactive')
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^elections', include(router.urls)),
    url(r'^api_doc', views.schema_view, name='docs'),
]

