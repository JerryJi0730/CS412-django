from django.views.generic import ListView
from django.shortcuts import render
from .models import Voter
from .forms import VoterFilterForm
from django.views.generic import DetailView
from django.db.models import Count
from django.views.generic import TemplateView
import plotly.graph_objects as go

class GraphsView(TemplateView):
    template_name = 'voter_analytics/graphs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter form
        form = VoterFilterForm(self.request.GET)
        context['form'] = form
        
        # Start with the base queryset
        voters = Voter.objects.all()

        if form.is_valid():
            if form.cleaned_data.get('party_affiliation'):
                voters = voters.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data.get('min_dob'):
                voters = voters.filter(date_of_birth__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data.get('max_dob'):
                voters = voters.filter(date_of_birth__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data.get('voter_score'):
                voters = voters.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data.get('v20state'):
                voters = voters.filter(v20state=True)
            if form.cleaned_data.get('v21town'):
                voters = voters.filter(v21town=True)
            if form.cleaned_data.get('v21primary'):
                voters = voters.filter(v21primary=True)
            if form.cleaned_data.get('v22general'):
                voters = voters.filter(v22general=True)
            if form.cleaned_data.get('v23town'):
                voters = voters.filter(v23town=True)

        # Generate the histogram for year of birth
        birth_years = [voter.date_of_birth.year for voter in voters]
        birth_year_hist = go.Histogram(x=birth_years, nbinsx=30, name="Year of Birth")
        birth_year_fig = go.Figure(data=[birth_year_hist])
        context['birth_year_fig'] = birth_year_fig.to_html(full_html=False)

        # Generate the pie chart for party affiliation
        party_counts = voters.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_names = [party['party_affiliation'] for party in party_counts]
        party_values = [party['count'] for party in party_counts]
        party_pie = go.Pie(labels=party_names, values=party_values, name="Party Affiliation")
        party_fig = go.Figure(data=[party_pie])
        context['party_fig'] = party_fig.to_html(full_html=False)

        # Generate the histogram for voter participation in elections
        election_counts = {
            '2020 State': sum(voter.v20state == True for voter in voters),
            '2021 Town': sum(voter.v21town == True for voter in voters),
            '2021 Primary': sum(voter.v21primary == True for voter in voters),
            '2022 General': sum(voter.v22general == True for voter in voters),
            '2023 Town': sum(voter.v23town == True for voter in voters),
        }
        election_names = list(election_counts.keys())
        election_values = list(election_counts.values())
        election_hist = go.Bar(x=election_names, y=election_values, name="Election Participation")
        election_fig = go.Figure(data=[election_hist])
        context['election_fig'] = election_fig.to_html(full_html=False)

        return context

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            party_affiliation = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_dob')
            max_dob = form.cleaned_data.get('max_dob')
            voter_score = form.cleaned_data.get('voter_score')
            voted_elections = {
                'v20state': form.cleaned_data.get('v20state'),
                'v21town': form.cleaned_data.get('v21town'),
                'v21primary': form.cleaned_data.get('v21primary'),
                'v22general': form.cleaned_data.get('v22general'),
                'v23town': form.cleaned_data.get('v23town'),
            }

            if party_affiliation:
                queryset = queryset.filter(party_affiliation=party_affiliation)
            if min_dob:
                queryset = queryset.filter(date_of_birth__gte=min_dob)
            if max_dob:
                queryset = queryset.filter(date_of_birth__lte=max_dob)
            if voter_score:
                queryset = queryset.filter(voter_score=voter_score)
            if form.cleaned_data.get('v20state'):
                voters = voters.filter(v20state=True)

            if form.cleaned_data.get('v21town'):
                voters = voters.filter(v21town=True)

            if form.cleaned_data.get('v21primary'):
             voters = voters.filter(v21primary=True)

            if form.cleaned_data.get('v22general'):
                voters = voters.filter(v22general=True)

            if form.cleaned_data.get('v23town'):
                voters = voters.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context
    


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
