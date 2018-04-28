from django import forms
from .models import Voter, VoteRecord, Candidate, Position, Election, General_VoteRecord


class GeneralVoteForm(forms.ModelForm):
    class Meta:
        model = General_VoteRecord
        fields = ['president','primary']
    president = forms.ModelChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="president")).values_list("full_name", flat=True))
    vice_president = forms.ModelChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="vice_president")).values_list("full_name", flat=True))
    #need to change fields accordingly in the General_VoteRecord


class PrimaryVoteForm(forms.ModelForm):
    class Meta:
        model = General_VoteRecord #change/create new Primary_voterecord?
        fields = ['president_nominee']
    president_nominees = forms.ModelChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="president_nominee")).values_list("full_name", flat=True))


class VoteForm(forms.ModelForm):
    class Meta:
        model = VoteRecord
        fields = ['president', 'governor', 'lieutenant_Governor', 'attorney_General', 'delegate',
                  'commonwealth_Attorney', 'sheriff', 'treasurer']


class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["first_name","last_name","street_address","city","state","zip","locality"]

class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=20, label='Password', widget=forms.PasswordInput)