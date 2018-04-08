from django import forms
from .models import Registered #,VoteRecord


class VoteForm(forms.Form):
    President = (
        ('Hillary Clinton', 'Hillary Clinton - (D)'),
        ('Donald Trump', 'Donald Trump - (R)'),
        ('Gary Johnson', 'Gary Johnson - (L)')
    )
    president = forms.ChoiceField(choices=President, widget=forms.RadioSelect())

class RegisteredForm(forms.ModelForm):
    class Meta:
        model = Registered
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'locality']
		
class VoteIdCheckForm(forms.Form):
    vote_id = forms.CharField(max_length=20, label='Enter confirmation number')