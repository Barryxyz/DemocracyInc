from django import forms
from .models import Registered,VoteRecord,CheckedIn


class VoteForm(forms.ModelForm):
    class Meta:
        model = VoteRecord
        # fields = ['president']
        fields = ['president','governor','lieutenant_Governor','attorney_General','delegate','commonwealth_Attorney','sheriff','treasurer']

class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Registered
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'locality']


class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckedIn
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'locality']


class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')