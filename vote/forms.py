from django import forms
from .models import Registered,VoteRecord


class VoteForm(forms.ModelForm):
    class Meta:
        model = VoteRecord
        fields = ['president']


class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Registered
        fields = ['first_name', 'last_name', 'date_of_birth', 'address']

class CheckInForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    date_of_birth = forms.CharField(label='Date of birth', max_length=100)