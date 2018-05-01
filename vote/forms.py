from django import forms
from vote import models

# Form used to distinguish which political party a voter is casting a ballot for
class CandidateChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.full_name + ' - (' + obj.political_party + ')'

class VoteForm(forms.Form):


    def __init__(self, *args, **kwargs):
        positions = kwargs.pop('positions')
        super(VoteForm, self).__init__(*args, **kwargs)

        for i, p in enumerate(positions):
            self.fields['%s' % p.name] = CandidateChoiceField(queryset=models.Candidate.objects.filter(position=p.id))

# Form used to check if a person is on the registered voters list
class RegisteredForm(forms.ModelForm):
    class Meta:
        model = models.Voter
        fields = ["first_name","last_name","street_address","city","state","zip","locality"]

# Form used after a voter checks in and is confirmed eligible to vote, the voter will input a given randomized code to
# allow them to access the correct ballot
class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')

# Form used to check if the user can access restricted pages (i.e. for poll workers)
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=20, label='Password', widget=forms.PasswordInput)