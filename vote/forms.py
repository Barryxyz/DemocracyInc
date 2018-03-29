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

