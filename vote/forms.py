from django import forms
<<<<<<< HEAD
from .models import Registered,VoteRecord
=======
from .models import Voter, VoteRecord
>>>>>>> master


class VoteForm(forms.ModelForm):
    class Meta:
        model = VoteRecord
<<<<<<< HEAD
        fields = ['president']

class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Registered
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'locality']
		
class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')
=======
        fields = ['president','governor','lieutenant_Governor','attorney_General','delegate','commonwealth_Attorney','sheriff','treasurer']

class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'locality']

class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=20, label='Password')
>>>>>>> master
