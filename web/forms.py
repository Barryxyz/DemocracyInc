from django import forms
from .models import Voter, Candidate, Vote, Position

class CheckinForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["first_name", "last_name","date_of_birth", "election_type","locality"]

class LoginForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["first_name", "last_name", "confirmation"]
