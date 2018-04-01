from django import forms


President = (
    ('d', 'Hillary Clinton - (D)'),
    ('r', 'Donald Trump - (R)'),
    ('l', 'Gary Johnson - (L)')
)

class VoteForm(forms.Form):
    my_field = forms.MultipleChoiceField(
        label = "Presidential Candidates",
        choices = President,
        widget=forms.RadioSelect(),
        required = True
    )

class CheckInForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    date_of_birth = forms.CharField(label='Date of birth', max_length=100)