from django import forms
from .models import Voter, Candidate, Position, General_VoteRecord, Primary_VoteRecord

# Form used to distinguish which political party a voter is casting a ballot for
class CandidateChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.full_name # add policital part here. maybe change to full name to first and last name?

# Form used to record the ballot of the general election
class GeneralVoteForm(forms.ModelForm):
    class Meta:
        model = General_VoteRecord
        fields = ['president', 'vice_president', 'house_rep', 'senator']
    president = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="president")))
    vice_president = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="vice_president")))
    house_rep = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="house_rep")))
    senator = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="senator")))

# Form used to record the ballot for electing candidates in the primary election
class PrimaryVoteForm(forms.ModelForm):
    class Meta:
        model = Primary_VoteRecord
        fields = ['president_nominee']
    president_nominee = CandidateChoiceField(queryset=Candidate.objects.filter(position=Position.objects.get(name="president_nominee")))

# Form used to check if a person is on the registered voters list
class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["first_name","last_name","street_address","city","state","zip","locality"]

# Form used after a voter checks in and is confirmed eligible to vote, the voter will input a given randomized code to
# allow them to access the correct ballot
class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')

# Form used to check if the user can access restricted pages (i.e. for poll workers)
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=20, label='Password', widget=forms.PasswordInput)