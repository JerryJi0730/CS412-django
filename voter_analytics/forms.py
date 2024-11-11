from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(
        choices=[('', 'All')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False
    )
    min_dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), required=False, label='Born After')
    max_dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), required=False, label='Born Before')
    voter_score = forms.ChoiceField(
        choices=[('', 'All')] + [(str(score), str(score)) for score in range(6)],  # Assuming voter_score is from 0 to 5
        required=False
    )
    v20state = forms.BooleanField(required=False, label='Voted in 2020 State Election')
    v21town = forms.BooleanField(required=False, label='Voted in 2021 Town Election')
    v21primary = forms.BooleanField(required=False, label='Voted in 2021 Primary')
    v22general = forms.BooleanField(required=False, label='Voted in 2022 General Election')
    v23town = forms.BooleanField(required=False, label='Voted in 2023 Town Election')
