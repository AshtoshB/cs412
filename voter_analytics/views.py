# file: voter_analytics/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for voter_analytics applicaitons

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

# Create your views here.

class VoterListView(ListView):
    '''View to display a list of voters with filtering options'''
  
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        '''Filter the queryset based on form inputs'''
        
        queryset = Voter.objects.all()

        # Get filter parameters from GET request
        party = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')

        # Election filters
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filters
        if party:
            queryset = queryset.filter(party_affiliation=party)

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)

        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)

        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # Filter by elections
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        '''Add additional context for the template'''
        context = super().get_context_data(**kwargs)

        # Get distinct party affiliations for dropdown
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')

        # Get year range for birth dates
        years = Voter.objects.dates('date_of_birth', 'year')
        if years:
            context['birth_years'] = range(years[0].year, years[len(years)-1].year + 1)
        else:
            context['birth_years'] = []

        # Voter scores (0-5)
        context['voter_scores'] = range(0, 6)

        # Preserve filter values in context
        context['selected_party'] = self.request.GET.get('party_affiliation', '')
        
        # Check if 'min_year' parameter exists in the GET request
        if self.request.GET.get('min_year'):
            min_year_value = self.request.GET.get('min_year')
            context['selected_min_year'] = int(min_year_value)
        else:
            context['selected_min_year'] = ''

        # Check if 'max_year' parameter exists in the GET request
        if self.request.GET.get('max_year'):
            max_year_value = self.request.GET.get('max_year')
            context['selected_max_year'] = int(max_year_value)
        else:
            context['selected_max_year'] = ''

        # Check if 'voter_score' parameter exists in the GET request
        if self.request.GET.get('voter_score'):
            voter_score_value = self.request.GET.get('voter_score')
            context['selected_voter_score'] = int(voter_score_value)
        else:
            context['selected_voter_score'] = ''

        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        return context


class VoterDetailView(DetailView):
    '''View to display details for a single voter'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    '''View to display graphs of voter data with filtering options'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        '''Filter the queryset based on form inputs'''
        queryset = Voter.objects.all()

        # Get filter parameters from GET request
        party = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')

        # Election filters
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filters
        if party:
            queryset = queryset.filter(party_affiliation=party)

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)

        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)

        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # Filter by elections
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        '''Add graph data to context'''
        context = super().get_context_data(**kwargs)

        # Get the filtered queryset
        voters = self.get_queryset()

        # Graph 1: Histogram of birth years
        birth_years = [voter.date_of_birth.year for voter in voters]
        year_counts = {}
        for year in birth_years:
            year_counts[year] = year_counts.get(year, 0) + 1

        sorted_years = sorted(year_counts.keys())
        year_values = [year_counts[year] for year in sorted_years]

        birth_year_fig = go.Figure(data=[
            go.Bar(x=sorted_years, y=year_values)
        ])
        birth_year_fig.update_layout(
            title='Distribution of Voters by Year of Birth',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters'
        )
        context['birth_year_graph'] = plotly.offline.plot(birth_year_fig, auto_open=False, output_type='div')

        # Graph 2: Pie chart of party affiliation
        party_counts = {}
        for voter in voters:
            party = voter.party_affiliation
            party_counts[party] = party_counts.get(party, 0) + 1

        party_fig = go.Figure(data=[
            go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
        ])
        party_fig.update_layout(title='Distribution of Voters by Party Affiliation')
        context['party_graph'] = plotly.offline.plot(party_fig, auto_open=False, output_type='div')

        # Graph 3: Histogram of election participation
        elections = {
            'v20state': sum(1 for v in voters if v.v20state),
            'v21town': sum(1 for v in voters if v.v21town),
            'v21primary': sum(1 for v in voters if v.v21primary),
            'v22general': sum(1 for v in voters if v.v22general),
            'v23town': sum(1 for v in voters if v.v23town)
        }

        election_fig = go.Figure(data=[
            go.Bar(x=list(elections.keys()), y=list(elections.values()))
        ])
        election_fig.update_layout(
            title='Voter Participation in Elections',
            xaxis_title='Election',
            yaxis_title='Number of Voters'
        )
        context['election_graph'] = plotly.offline.plot(election_fig, auto_open=False, output_type='div')

        # Add filter context data
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')

        years = Voter.objects.dates('date_of_birth', 'year')
        if years:
            context['birth_years'] = range(years[0].year, years[len(years)-1].year + 1)
        else:
            context['birth_years'] = []

        context['voter_scores'] = range(0, 6)

        # Preserve filter values in context
        context['selected_party'] = self.request.GET.get('party_affiliation', '')
        
        # Check if 'min_year' parameter exists in the GET request
        if self.request.GET.get('min_year'):
            min_year_value = self.request.GET.get('min_year')
            context['selected_min_year'] = int(min_year_value)
        else:
            context['selected_min_year'] = ''

        # Check if 'max_year' parameter exists in the GET request
        if self.request.GET.get('max_year'):
            max_year_value = self.request.GET.get('max_year')
            context['selected_max_year'] = int(max_year_value)
        else:
            context['selected_max_year'] = ''

        # Check if 'voter_score' parameter exists in the GET request
        if self.request.GET.get('voter_score'):
            voter_score_value = self.request.GET.get('voter_score')
            context['selected_voter_score'] = int(voter_score_value)
        else:
            context['selected_voter_score'] = ''

        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        return context
