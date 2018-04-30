# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Voter, General_VoteRecord, Primary_VoteRecord, Election, VoteCount, Position, Candidate, PollWorker
from .forms import VoteIdCheckForm, RegisteredForm, LoginForm, GeneralVoteForm, PrimaryVoteForm

from rest_framework import viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .serializers import generalSerializer, primarySerializer, electionSerializer
from django.shortcuts import render, redirect
from django.urls import reverse
import random, requests
from itertools import groupby

# Create your views here.

# for swagger UI
schema_view = get_schema_view(title='Election API', urlconf='vote.urls', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

def home(request):
    return render(request, 'base.html', {})

def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
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
        form = LoginForm()
    return render(request, './registration/login.html', {'form': form})

def logout_page(request):
    return render(request, 'registration/logout_success.html', {})

def reset(request):
    return render(request, 'registration/password_reset_form.html', {})

def already_voted(request):
    return render(request, 'alreadyvoted.html', {})

def view_elections(request):
    query_results = Election.objects.all()
    return render(request, 'view_elections.html', {'query_results': query_results})

@login_required
def view_voters(request):
    query_results = Voter.objects.all()
    return render(request, 'view_voters.html', {'query_results': query_results})

def load_voters(request):
    r = requests.get('http://cs3240votingproject.org/voters/?key=democracy')
    response = r.json()
    status = response["status"]
    if (status == "200"):
        voters = response["voters"]
        for voter in voters:
            voter_exists = Voter.objects.filter(voter_number=voter["voter_number"]).exists()
            if not voter_exists:
                Voter(voter_number = voter["voter_number"],
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
    active_election = Election.objects.get(status="active").type
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisteredForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            registered_voter = Voter.objects.get(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                street_address=form.cleaned_data['street_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip=form.cleaned_data['zip'],
                locality=form.cleaned_data['locality'].upper() + " COUNTY"
            ).exists()

            if registered_voter:
                voter = Voter.objects.get(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    street_address=form.cleaned_data['street_address'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    zip=form.cleaned_data['zip']
                )

                v_id = voter.id

                if (active_election == 'general'):
                    exists = General_VoteRecord.objects.filter(voter_id=v_id).exists()
                elif (active_election == 'primary'):
                    exists = Primary_VoteRecord.objects.filter(voter_id=v_id).exists()

                locality = voter.locality
                precinct = voter.precinct_id
                full_name = voter.first_name + " " + voter.last_name

                curr_user = User.objects.get(username=request.user.username)
                curr_pollworker = PollWorker.objects.get(user=curr_user.id)
                polling_precinct = curr_pollworker.precinct_id

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
        form = RegisteredForm()
    return render(request, 'checkin.html', {'form': form})


def inactive(request):
    return render(request, 'inactive.html', {})

def vote(request):
    active_election = Election.objects.get(status="active").type
    if request.method == 'POST' :
        # create a form instance and populate it with data from the request:
        if(active_election == 'general'):
            form = GeneralVoteForm(request.POST)
        elif(active_election == 'primary'):
            form = PrimaryVoteForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            voter = Voter.objects.get(confirmation=request.session['input_key'])

            v_id = voter.id
            if (active_election == 'general'):
                exists = General_VoteRecord.objects.filter(voter_id=v_id).exists()
            elif (active_election == 'primary'):
                exists = Primary_VoteRecord.objects.filter(voter_id=v_id).exists()

            if exists:
                return redirect(reverse('already_voted'))
            else:
                task = form.save(commit=False)
                if active_election == 'general':
                    task.president = form.cleaned_data['president'].full_name
                    task.vice_president = form.cleaned_data['vice_president'].full_name
                    task.house_rep = form.cleaned_data['house_rep'].full_name
                    task.senator = form.cleaned_data['senator'].full_name
                elif active_election == 'primary':
                    task.president_nominee = form.cleaned_data['president_nominee'].full_name
                task.voter = voter
                task.save()
                # redirect to a new URL:
                # return redirect(reverse('home'))
                return render(request, 'ballot_print.html', {'form': form, 'president': task.president, 'vice_president': task.vice_president,'house_rep': task.house_rep, 'senator': form.cleaned_data['senator']})

    # if a GET (or any other method) we'll create a blank form
    else:
        if (active_election == 'general'):
            form = GeneralVoteForm()
        elif (active_election == 'primary'):
            form = PrimaryVoteForm()

    return render(request, 'vote.html', {'form': form})

def vote_id_check(request):
    isNotCheckedIn = False
    active_election = Election.objects.get(status="active").type
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VoteIdCheckForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            input_key = form.cleaned_data['vote_id']
            valid_key = Voter.objects.filter(confirmation=input_key).exists()

            if valid_key:

                voter = Voter.objects.get(confirmation=input_key)
                v_id = voter.id
                if (active_election == 'general'):
                    exists = General_VoteRecord.objects.filter(voter_id=v_id).exists()

                elif (active_election == 'primary'):
                    exists = Primary_VoteRecord.objects.filter(voter_id=v_id).exists()

                if exists:
                    return redirect(reverse('already_voted'))
                else:

                    request.session['input_key'] = input_key
                    return redirect(reverse('vote'))
            else:
                isNotCheckedIn = True
                return render(request, 'vote_id_check.html', {'form': form, 'isNotCheckedIn':isNotCheckedIn})  # need an error page?
        else:
            return redirect(reverse('home'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoteIdCheckForm()
    return render(request, 'vote_id_check.html', {'form': form, 'isNotCheckedIn':isNotCheckedIn})

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key = ''

    for i in range(6):
        key += (''.join(''.join(random.choice(seq))))
    return key

def count_votes():
    VoteCount.objects.all().delete()
    primary_positions = ['president_nominee']
    general_positions = ['president', 'vice_president', 'house_rep', 'senator']
    primary_records = Primary_VoteRecord.objects.all()
    general_records = General_VoteRecord.objects.all()

    primary_votes = [dict() for i in primary_positions]
    general_votes = [dict() for i in general_positions]

    for vr in primary_records:
        for i in range(0, len(primary_positions)):
            pos = primary_positions[i]
            name = getattr(vr, pos)
            if name in primary_votes[i]:
                primary_votes[i][name] += 1
            else:
                primary_votes[i][name] = 0

    for vr in general_records:
        for i in range(0, len(general_positions)):
            pos = general_positions[i]
            name = getattr(vr, pos)
            if name in general_votes[i]:
                general_votes[i][name] += 1
            else:
                general_votes[i][name] = 0

    results = []
    for i in range(0, len(primary_positions)):
        for name in primary_votes[i].keys():
            results.append(
                VoteCount(name=name, position=primary_positions[i], count=primary_votes[i][name], election='primary'))

    for i in range(0, len(general_positions)):
        for name in general_votes[i].keys():
            results.append(
                VoteCount(name=name, position=general_positions[i], count=general_votes[i][name], election='general'))

    for r in results:
        r.save()

@login_required
def vote_count(request):
    count_votes()
    results = VoteCount.objects.all()
    return render(request, 'vote_count.html', {'query_results': results})

@login_required
def general_results(request):
    president_data = [['Candidates','Count']]
    vp_data = [['Candidates','Count']]
    houserep_data = [['Candidates','Count']]
    senator_data = [['Candidates','Count']]

    general_id = Election.objects.get(type="general").id
    general_positions = Position.objects.filter(election=general_id)
    for position in general_positions:
        general_candidates = Candidate.objects.filter(position=position.id).values_list("full_name", flat=True)
        for candidate in general_candidates:
            if position.name == "president":
                count = General_VoteRecord.objects.filter(president=candidate).count()
                president_data.append([candidate, count])
            elif position.name == "vice_president":
                count = General_VoteRecord.objects.filter(vice_president=candidate).count()
                vp_data.append([candidate, count])
            elif position.name == "house_rep":
                count = General_VoteRecord.objects.filter(house_rep=candidate).count()
                houserep_data.append([candidate, count])
            elif position.name == "senator":
                count = General_VoteRecord.objects.filter(senator=candidate).count()
                senator_data.append([candidate, count])

    print(president_data)

    prez_data_source = SimpleDataSource(data=president_data)
    vp_data_source = SimpleDataSource(data=vp_data)
    houserep_data_source = SimpleDataSource(data=houserep_data)
    senator_data_source = SimpleDataSource(data=senator_data)

    prez_chart = gchart.PieChart(prez_data_source, options={'title': "President"})
    vp_chart = gchart.PieChart(vp_data_source, options={'title': "Vice President"})
    houserep_chart = gchart.PieChart(houserep_data_source, options={'title': "House of Representative"})
    senator_chart = gchart.PieChart(senator_data_source, options={'title': "Senator"})

    context = {
        "prez_chart": prez_chart,
        "vp_chart": vp_chart,
        "houserep_chart": houserep_chart,
        "senator_chart": senator_chart
    }

    return render(request, 'general_results.html', context)

@login_required
def primary_results(request):
    pn_data = [['Candidates','Count']]

    primary_id = Election.objects.get(type="primary").id
    primary_positions = Position.objects.filter(election=primary_id)
    for position in primary_positions:
        general_candidates = Candidate.objects.filter(position=position.id).values_list("full_name", flat=True)
        for candidate in general_candidates:
            if position.name == "president_nominee":
                count = Primary_VoteRecord.objects.filter(president_nominee=candidate).count()
                pn_data.append([candidate, count])

    pn_data_source = SimpleDataSource(data=pn_data)
    pn_chart = gchart.PieChart(pn_data_source, options={'title': "President Nominee"})
    context = {
        "pn_chart": pn_chart
    }
    return render(request, 'primary_results.html', context)


class primaryViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Return an instance of a candidate

        list:
            Returns result of the number of vote per candidate

        create:
            Create an instance of a candidate result.

        delete:
            Remove an instance of a candidate result.

        partial_update:
            Update one or more fields of a candidate.

        update:
            Update a candidate.
    """
    queryset = Primary_VoteRecord.objects.all()
    serializer_class = primarySerializer


class generalViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Return an instance of a candidate

        list:
            Returns result of the number of vote per candidate

        create:
            Create an instance of a candidate result.

        delete:
            Remove an instance of a candidate result.

        partial_update:
            Update one or more fields of a candidate.

        update:
            Update a candidate.
    """

    queryset = General_VoteRecord.objects.all()
    serializer_class = generalSerializer

    def perform_create(self, serializer):
        serializer.save()

class electionViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return an instance of election type/date

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

    queryset = Election.objects.all()
    serializer_class = electionSerializer

