# file: voter_analytics/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for voter_analytics applicaitons

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q

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
        context['selected_min_year'] = self.request.GET.get('min_year', '')
        context['selected_max_year'] = self.request.GET.get('max_year', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
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
