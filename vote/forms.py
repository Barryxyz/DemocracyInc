from django import forms
President = (
    ('d', 'Hillary Clinton - (D)'),
    ('r', 'Donald Trump - (R)'),
    ('l', 'Gary Johnson - (L)')
)


class VoteForm(forms.Form):
    president = forms.MultipleChoiceField(
        label="President",
        choices=President,
        widget = forms.RadioSelect
    )