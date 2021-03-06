# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from django.shortcuts import render, redirect
from django.urls import reverse
from vote import models,forms, serializers
import random, requests

# Create your views here.

# for swagger UI
schema_view = get_schema_view(title='Election API', urlconf='vote.urls', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

# Homepage/landing page
def home(request):
    return render(request, 'base.html', {})

# user authentication
def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            valid_pollworker = User.objects.filter(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            ).exists()

            if valid_pollworker:
                return redirect(reverse('vote_id_check'))
            else:
                return redirect(reverse('home'))
            # process the data in form.cleaned_data as required
            # redirect to a new URL:

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.LoginForm()
    return render(request, './registration/login.html', {'form': form})

def logout_page(request):
    return render(request, 'registration/logout_success.html', {})

def reset(request):
    return render(request, 'registration/password_reset_form.html', {})

def already_voted(request):
    return render(request, 'alreadyvoted.html', {})

def view_elections(request):
    query_results = models.Election.objects.all()
    return render(request, 'view_elections.html', {'query_results': query_results})

# certain pages require a certain elevated user access
# page to see the list of all registered and eligible voters
@login_required
def view_voters(request):
    query_results = models.Voter.objects.all()
    return render(request, 'view_voters.html', {'query_results': query_results})

# function to load voter api into database on heroku
def load_voters(request):
    r = requests.get('http://cs3240votingproject.org/voters/?key=democracy')
    response = r.json()
    status = response["status"]
    if (status == "200"):
        voters = response["voters"]
        for voter in voters:
            voter_exists = models.Voter.objects.filter(voter_number=voter["voter_number"]).exists()
            if not voter_exists:
                models.Voter(voter_number = voter["voter_number"],
                      voter_status = voter["voter_status"],
                      date_registered = voter["date_registered"],
                      first_name = voter["first_name"],
                      last_name = voter["last_name"],
                      street_address = voter["street_address"],
                      city = voter["city"],
                      state = voter["state"],
                      zip = voter["zip"],
                      locality = voter["locality"],
                      precinct=voter["precinct"],
                      precinct_id = voter["precinct_id"]
                ).save()
    return render(request, 'base.html', {})

@login_required
def checkin(request):
    # if this is a POST request we need to process the form data
    active_election = models.Election.objects.get(status="active").type
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.RegisteredForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            registered_voter = models.Voter.objects.filter(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                street_address=form.cleaned_data['street_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip=form.cleaned_data['zip'],
                locality=form.cleaned_data['locality'].upper() + " COUNTY"
            ).exists()

            if registered_voter:
                voter = models.Voter.objects.get(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    street_address=form.cleaned_data['street_address'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    zip=form.cleaned_data['zip']
                )

                v_id = voter.id

                exists = models.VoteRecord.objects.filter(voter_id=v_id).exists()

                locality = voter.locality
                precinct = voter.precinct_id
                full_name = voter.first_name + " " + voter.last_name

                curr_user = User.objects.get(username=request.user.username)
                curr_pollworker = models.PollWorker.objects.get(user=curr_user.id)
                polling_precinct = curr_pollworker.precinct_id
                polling_locality = curr_pollworker.locality

                if voter.voter_status == "inactive":
                    return redirect(reverse('inactive'))
                if exists:
                    return redirect(reverse('already_voted'))

                if precinct != polling_precinct:
                    return render(request, 'incorrect_precinct.html', {'full_name': full_name, 'locality': locality, 'precinct': precinct, 'polling_locality': polling_locality, 'polling_precinct': polling_precinct})

                else:
                    key = generator()
                    full_name = voter.first_name + " " + voter.last_name
                    locality = voter.locality
                    voter.confirmation = key
                    voter.save()
                    return render(request, 'booth_assignment.html', {'booth': key, 'full_name': full_name, 'locality': locality})

            else:
                return render(request, 'notregistered.html', {})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.RegisteredForm()
    return render(request, 'checkin.html', {'form': form})

def inactive(request):
    return render(request, 'inactive.html', {})

def vote(request):
    active_election = models.Election.objects.get(status="active")
    voter = models.Voter.objects.get(confirmation=request.session['input_key'])
    has_voted = models.VoteRecord.objects.filter(voter_id=voter.id).exists()
    if has_voted:
        return redirect(reverse('already_voted'))
    else:
        positions = models.Position.objects.filter(election=active_election.id)
        form = forms.VoteForm(request.POST or None, positions=positions)
        if form.is_valid():
            names = []
            for p in positions:
                candidate = form.cleaned_data['%s' % p.name]
                names.append(candidate)
                models.VoteRecord(election=active_election,
                           position=p,
                           candidate=candidate).save()
            return render(request, 'ballot_print.html', {'form': form, 'election': active_election, 'positions': positions, 'names': names})
        return render(request, 'vote.html', {'form': form})

def vote_id_check(request):
    isNotCheckedIn = False
    active_election = models.Election.objects.get(status="active").type
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.VoteIdCheckForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            input_key = form.cleaned_data['vote_id']
            valid_key = models.Voter.objects.filter(confirmation=input_key).exists()

            if valid_key:

                voter = models.Voter.objects.get(confirmation=input_key)
                has_voted = models.VoteRecord.objects.filter(voter_id=voter.id).exists()

                if has_voted:
                    return redirect(reverse('already_voted'))
                else:
                    request.session['input_key'] = input_key
                    return redirect(reverse('vote'))
            else:
                isNotCheckedIn = True
                return render(request, 'vote_id_check.html', {'form': form, 'isNotCheckedIn':isNotCheckedIn})  # need an error page?
        else:
            return redirect(reverse('home'))

    else:
        form = forms.VoteIdCheckForm()
    return render(request, 'vote_id_check.html', {'form': form, 'isNotCheckedIn':isNotCheckedIn})

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key = ''

    for i in range(6):
        key += (''.join(''.join(random.choice(seq))))
    return key

def count_votes(type):
    models.VoteCount.objects.all().delete()
    election = models.Election.objects.get(type=type)
    positions = models.Position.objects.filter(election=election)
    for position in positions:
        candidates = models.Candidate.objects.filter(position=position)
        for candidate in candidates:
            count = models.VoteRecord.objects.filter(position=position,candidate=candidate).count()
            models.VoteCount(election=election.type,
                             position=position.name,
                             candidate=candidate.full_name,
                             count=count).save()

@login_required
def vote_count(request):
    count_votes(models.Election.objects.get(status="active").type)
    return render(request, 'vote_count.html', {'query_results': models.VoteCount.objects.all()})

@login_required
def results(request):

    context = {}
    election = models.Election.objects.get(status="active")
    positions = models.Position.objects.filter(election=election)
    for position in positions:
        data = [['Candidates','Count']]
        candidates = models.Candidate.objects.filter(position=position)
        for candidate in candidates:
            count = models.VoteRecord.objects.filter(position=position,candidate=candidate).count()
            data.append([candidate.full_name, count])
        data_source = SimpleDataSource(data=data)
        chart = gchart.PieChart(data_source, options={'title': position.name})
        context['%s' % position.name] = chart

    return render(request, 'results.html', {'context': context, 'election': election.type.upper()})

# external API to view general election results
class VoteCountViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Return an instance of a candidate.

        list:
            Returns result of the number of vote per candidate.

        create:
            Create an instance of a candidate result.

        delete:
            Remove an instance of a candidate result.

        partial_update:
            Update one or more fields of a candidate.

        update:
            Update a candidate.
    """
    queryset = models.VoteCount.objects.all()
    serializer_class = serializers.VoteCountSerializer

    def get_queryset(self):
        election_id = self.kwargs['election_id']
        election_type = models.Election.objects.get(election_id=election_id).type
        count_votes(election_type)
        return models.VoteCount.objects.filter(election=election_type)

# # external API to view general election results
# class primaryViewSet(viewsets.ModelViewSet):
#     """
#         retrieve:
#             Return an instance of a candidate.
#
#         list:
#             Returns result of the number of vote per candidate.
#
#         create:
#             Create an instance of a candidate result.
#
#         delete:
#             Remove an instance of a candidate result.
#
#         partial_update:
#             Update one or more fields of a candidate.
#
#         update:
#             Update a candidate.
#     """
#
#     queryset = models.VoteRecord.objects.filter(election=models.Election.objects.filter(type="primary"))
#     serializer_class = voteSerializer


# external API to view election types
class ElectionViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return an instance of election type/date.

    list:
        Return all available elections, ordered by date.

    create:
        Create an instance of an election.

    delete:
        Remove an instance of an election.

    partial_update:
        Update one or more fields on an existing election.

    update:
        Update an election.
    """

    queryset = models.Election.objects.all()
    serializer_class = serializers.ElectionSerializer
    lookup_field = 'election_id'