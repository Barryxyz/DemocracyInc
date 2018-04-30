# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from graphos.renderers import gchart
from graphos.renderers.gchart import BarChart
from graphos.sources.simple import SimpleDataSource
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Voter, VoteRecord, Election, VoteCount, Candidate, General_VoteRecord, Primary_VoteRecord
from .forms import VoteForm, VoteIdCheckForm, RegisteredForm, LoginForm, GeneralVoteForm, PrimaryVoteForm

from rest_framework import viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .serializers import generalSerializer, primarySerializer, electionSerializer
from django.shortcuts import render, redirect
from django.urls import reverse
import random, requests

# Create your views here.

# for swagger UI
schema_view = get_schema_view(title='Election API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

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
            # print(voter)
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
            registered_voter = Voter.objects.filter(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                street_address=form.cleaned_data['street_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip=form.cleaned_data['zip']
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
                #exists = VoteRecord.objects.filter(voter_id=v_id).exists()

                inactive = voter.voter_status

                if inactive == "inactive":
                    return redirect(reverse('inactive'))

                if exists:
                    return redirect(reverse('already_voted'))

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
    print(active_election)
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
                return render(request, 'ballot_print.html', {'form': form, 'president': task.president, 'vice_president': task.vice_president,
				'house_rep': task.house_rep, 'senator': form.cleaned_data['senator']})

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

@login_required
def vote_count(request):
    # primary_positions = [a for a in dir(Primary_VoteRecord) if (not a.startswith('__') and  a is not 'voter' and a is not 'time_stamp')]
    # general_positions = [a for a in dir(General_VoteRecord) if (not a.startswith('__') and  a is not 'voter' and a is not 'time_stamp')]
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
            results.append(VoteCount(name=name, position=primary_positions[i], count=primary_votes[i][name], election = 'primary'))

    for i in range(0, len(general_positions)):
        for name in general_votes[i].keys():
            results.append(VoteCount(name=name, position=general_positions[i], count=general_votes[i][name], election = 'general'))

    return render(request, 'vote_count.html', {'query_results': results})

@login_required
def results(request):
#    candidates_pres = General_VoteRecord.president
#	
#    president_data = [['Candidates','Count']]
#    for candidate in candidates_pres:
#        count = VoteCount.objects.filter(president=candidate).count()
#        president_data.append(candidate,count)

################################################################################		
    prez_count = VoteRecord.objects.filter(president='Gary Johnson').count()
    prez_count2 = VoteRecord.objects.filter(president='Hillary Clinton').count()
    president_data = [
        ['Candidates','Count'],
        ['Gary Johnson', prez_count],
        ['Hillary Clinton', prez_count2]
    ]
    gov_count = VoteRecord.objects.filter(governor='Matthew Ray').count()
    gov_count2 = VoteRecord.objects.filter(governor='Travis Bailey').count()
    gov_count3 = VoteRecord.objects.filter(governor='Marisha Miller').count()
    governor_data = [
        ['Candidates', 'Count'],
        ['Matthew Ray', gov_count],
        ['Travis Bailey', gov_count2],
        ['Marisha Miller', gov_count3]
    ]

    prez_data_source = SimpleDataSource(data=president_data)
    gov_data_source = SimpleDataSource(data=governor_data)
    prez_chart = BarChart(prez_data_source, options={'title': "President", 'xaxis': 'Count'})
    gov_chart = gchart.PieChart(gov_data_source, options={'title': "Governor"})
    context = {
        "prez_chart": prez_chart,
        "gov_chart": gov_chart,
    }
    return render(request, 'results.html', context)

####################################################################

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

