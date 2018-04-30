from django import forms
from .models import Voter, Candidate, Position, General_VoteRecord, Primary_VoteRecord

class CandidateChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.full_name


class GeneralVoteForm(forms.ModelForm):
    class Meta:
        model = General_VoteRecord
        fields = ['president', 'vice_president', 'house_rep', 'senator']
    president = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="president")))
    vice_president = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="vice_president")))
    house_rep = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="house_rep")))
    senator = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="senator")))

class PrimaryVoteForm(forms.ModelForm):
    class Meta:
        model = Primary_VoteRecord
        fields = ['president_nominee']
    president_nominees = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="president_nominee")))

#
# class VoteForm(forms.ModelForm):
#     class Meta:
#         model = VoteRecord
#         fields = ['president', 'governor', 'lieutenant_Governor', 'attorney_General', 'delegate',
#                   'commonwealth_Attorney', 'sheriff', 'treasurer']

class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["first_name","last_name","street_address","city","state","zip","precinct_id"]

class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=20, label='Password', widget=forms.PasswordInput)