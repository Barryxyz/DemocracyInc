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

from VotingApp import settings
from django.contrib import admin
from django.conf.urls import url, include

from rest_framework import routers, serializers, viewsets
from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from vote import views

router = routers.DefaultRouter()
router.register(r'elections', views.electionViewSet)
router.register(r'2018-11', views.generalViewSet)
router.register(r'2018-07', views.primaryViewSet)


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
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
    url(r'^results/', views.results, name='results'),
    url(r'^alreadyvoted/', views.already_voted, name='already_voted'),
    url(r'^inactive/', views.inactive, name='inactive')
]


#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'accounts/', include('django.contrib.auth.urls')),
]

#for external api
urlpatterns += [
    # viewing api
    url(r'^', include(router.urls)),
    # url(r'^elections/2018-11/', include(router.urls)),


    # swagger UI material
    # url(r'^', views.schema_view, name='docs'),
    # url(r'^elections/', include(router.urls)),
    # url(r'^elections/2018-07', include(router.urls)),
    # url(r'^elections/2018-11', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
