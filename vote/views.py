# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Voter, General_VoteRecord, Primary_VoteRecord, Election, VoteCount, Candidate
from .forms import VoteIdCheckForm, RegisteredForm, LoginForm, GeneralVoteForm, PrimaryVoteForm
from rest_framework import viewsets

from .serializers import CountSerializer
from django.shortcuts import render, redirect
from django.urls import reverse
import random, json, requests
from itertools import groupby

# Create your views here.

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
                exists = VoteRecord.objects.filter(voter_id=v_id).exists()

                inactive = voter.voter_status

                if inactive == "inactive":
                    return redirect(reverse('inactive'))

                if exists:
                    return redirect(reverse('alreadyvoted'))

                else:
                    key = generator()
                    full_name = registered_voter.first_name + " " + registered_voter.last_name
                    locality = registered_voter.locality
                    registered_voter.confirmation = key
                    registered_voter.save()
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
            exists = VoteRecord.objects.filter(voter_id=v_id).exists()

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
                return redirect(reverse('home'))
    # if a GET (or any other method) we'll create a blank form
    else:
        if (active_election == 'general'):
            form = GeneralVoteForm()
        elif (active_election == 'primary'):
            form = PrimaryVoteForm()

    return render(request, 'vote.html', {'form': form})

def vote_id_check(request):
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
                exists = VoteRecord.objects.filter(voter_id=v_id).exists()

                if exists:
                    return redirect(reverse('alreadyvoted'))
                else:

                    request.session['input_key'] = input_key
                    return redirect(reverse('vote'))
            else:
                return render(request, 'vote_id_check.html', {'form': form})  # need an error page?
        else:
            return redirect(reverse('home'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VoteIdCheckForm()
    return render(request, 'vote_id_check.html', {'form': form})

def generator():
    seq = "ABCDFGHJIKLMNOPQRSTUVWXYZ1234567890"
    key = ''

    for i in range(6):
        key += (''.join(''.join(random.choice(seq))))
    return key

@login_required
def vote_count(request):
    # records = VoteRecord.objects.all()
    # votes = dict()
    # positions = dict()
    # for vr in records:
    #     key = vr.president
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('president')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('president')
    #
    #     key = vr.governor
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('governor')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('governor')
    #
    #     key = vr.lieutenant_Governor
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('lieutenant_Governor')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('lieutenant_Governor')
    #
    #     key = vr.attorney_General
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('attorney_General')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('attorney_General')
    #
    #     key = vr.delegate
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('delegate')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('delegate')
    #
    #     key = vr.commonwealth_Attorney
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('votes')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('votes')
    #
    #     key = vr.sheriff
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('sheriff')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('sheriff')
    #
    #     key = vr.treasurer
    #     if key in votes:
    #         votes[key] += 1
    #         positions[key].add('treasurer')
    #     else:
    #         votes[key] = 1
    #         positions[key] = set()
    #         positions[key].add('treasurer')
    #
    # results = []
    # for name in votes.keys():
    #     for position in positions[name]:
    #         results.append(VoteCount(name=name, position=position, count=str(votes[name])))

    # return render(request, 'vote_count.html', {'query_results': results})
    return render(request, 'vote_count.html')


@login_required
def general_results(request):
    #for General Election
    from django.db.models import Count
    # prez_count = General_VoteRecord.objects.values('president').annotate(the_count=Count('president'))
    # candidates_pres = General_VoteRecord.objects.all().values_list('president', flat=True).order_by('president')

    from collections import Counter
    # primary_records = Primary_VoteRecord.objects.all().values_list('president_nominee', flat=True).orderby('president_nominee')
    # c = Counter(getattr() for i in primary_records)
    general_records = General_VoteRecord.objects.all().values_list('president', flat=True).order_by('president')
    president_data = [[]]
    for candidate in general_records:
        count = General_VoteRecord.objects.filter(president=candidate).count()
        president_data.append([candidate,count])

    # president_data = {item['president']: item['president__count'] for item in general_records}
        # president_data=[
        #     ['president',general_records]
        # ]

    #
    # primary_positions = ['president_nominee']
    # general_positions = ['president', 'vice_president', 'house_rep', 'senator']
    # primary_records = Primary_VoteRecord.objects.all().values_list('president_nominee', flat=True).orderby('president_nominee')
    # for i in range(primary_records):
    #     if
    #
    #
    # for i in primary_positions:
    #     president_data =[
    #         ['president_nominee',primary_records]
    #     ]
    # general_records = General_VoteRecord.objects.all()

    # prez_count = General_VoteRecord.objects.filter(president='Hillary Clinton').count()
    # prez_count2 = General_VoteRecord.objects.filter(president='Donald Trump').count()
    # president_data = [
    #     ['Candidates','Count'],
    #     ['Hillary Clinton', prez_count],
    #     ['Donald Trump', prez_count2]
    # ]
    vp_count = General_VoteRecord.objects.filter(vice_president='Tim Kaine').count()
    vp_count2 = General_VoteRecord.objects.filter(vice_president='Mike Pence').count()
    governor_data = [
        ['Candidates', 'Count'],
        ['Tim Kaine', vp_count],
        ['Mike Pence', vp_count2],
    ]
    houserep_count = General_VoteRecord.objects.filter(house_rep='LuAnn Bennett').count()
    houserep_count2 = General_VoteRecord.objects.filter(house_rep='Barbara Comstock').count()
    houserep_data = [
        ['Candidates', 'Count'],
        ['LuAnn Bennett', houserep_count],
        ['Barbara Comstock', houserep_count2],
    ]
    senator_count = General_VoteRecord.objects.filter(senator='Mark Warner').count()
    senator_count2 = General_VoteRecord.objects.filter(senator='Ed Gillespie').count()
    senator_data =[
        ['Candidates', 'Count'],
        ['Mark Warner', senator_count],
        ['Ed Gillespie', senator_count2],
    ]

    prez_data_source = SimpleDataSource(data=president_data)
    gov_data_source = SimpleDataSource(data=governor_data)
    houserep_data_source = SimpleDataSource(data=houserep_data)
    senator_data_source = SimpleDataSource(data=senator_data)
    prez_chart = gchart.PieChart(prez_data_source, options={'title': "President"})
    vp_chart = gchart.PieChart(gov_data_source, options={'title': "Vice President"})
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
    return render(request, 'primary_results.html')



class CountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = VoteCount.objects.all()
    serializer_class = CountSerializer

# class RecordViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = VoteRecord.objects.all()
#     serializer_class = RecordSerializer
