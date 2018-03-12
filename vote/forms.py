from django import forms

GOVERNOR = (
    ('d', 'Ralph S. Northam - D'),
    ('r', 'Edward W. "Ed" Gillespie - R'),
    ('l', 'Clifford D. Hyra - L')
)

LIEUTENANT_GOVERNOR = (
    ('d', 'Justin E. Fairfax - D'),
    ('r', 'Jill H. Vogel - R')
)

ATTORNEY_GENERAL = (
    ('d', 'Mark R. Herring - D'),
    ('r', 'John D. Adams - R')
)

HOUSE_OF_DELEGATES = (
    ('d', 'Jeff M. Bourne - D'),
    ('b', '')
)

COMMONWEALTH_ATTORNEY = (
    ('ca1', 'Michael N. Herring'),
)

SHERIFF = (
    ('lg1', 'Antoinette V. Irving'),
    ('lg2', 'Nicole D. Jackson'),
    ('lg3', 'Emmett Johnson Jafari')
)

TREASURER = (
    ('t1', 'Nichole Ona R. Armstead'),
    ('t2', 'Michelle R. Mosby'),
    ('t3', 'L. Shirley Harvey')
)


class VoteForm(forms.Form):

    governor = forms.MultipleChoiceField(
        label="GOVERNOR",
        choices=GOVERNOR,
        widget=forms.RadioSelect(attrs={'class' : 'funkyradio-default'})
    )

    # lieutenant_gov = forms.MultipleChoiceField(
    #     label="LIEUTENANT GOVERNOR",
    #     choices=LIEUTENANT_GOVERNOR,
    #     widget=forms.RadioSelect
    # )
    #
    # attorney_gen = forms.MultipleChoiceField(
    #     label="ATTORNEY GENERAL",
    #     choices=ATTORNEY_GENERAL,
    #     widget=forms.RadioSelect
    # )
    #
    # house_of_delegates = forms.ChoiceField(
    #     label="HOUSE OF DELEGATES",
    #     choices=HOUSE_OF_DELEGATES,
    #     widget=forms.RadioSelect
    # )
    #
    # commonwealth_att = forms.MultipleChoiceField(
    #     label="COMMONWEALTH ATTORNEY",
    #     choices=COMMONWEALTH_ATTORNEY,
    #     widget=forms.RadioSelect
    # )
    #
    # sheriff = forms.MultipleChoiceField(
    #     label="SHERIFF",
    #     choices=SHERIFF,
    #     widget=forms.RadioSelect
    # )
    #
    # treasurer = forms.MultipleChoiceField(
    #     label="TREASURER",
    #     choices=TREASURER,
    #     widget=forms.RadioSelect
    # )

