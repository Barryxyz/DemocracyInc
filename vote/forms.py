from django import forms
from .models import Registered,VoteRecord


class VoteForm(forms.ModelForm):
    class Meta:
        model = VoteRecord
        fields = ['president']

class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Registered
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'locality']
		
class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')