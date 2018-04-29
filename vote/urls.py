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

from rest_framework import routers
from vote import views

router = routers.DefaultRouter()
router.register(r'count_api', views.CountViewSet)
router.register(r'records_api', views.RecordViewSet)


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^load_voters/', views.load_voters, name='load_voters'),
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
    url(r'^view_election/', views.view_elections, name='view_elections'),
    url(r'^vote_count/', views.vote_count, name='vote_count'),
    url(r'^results/', views.results, name='results'),
    url(r'^alreadyvoted/', views.already_voted, name='already_voted')
]


#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'accounts/', include('django.contrib.auth.urls')),
]

#for external api
urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
