# file: voter_analytics/urls.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: URL patterns for voter_analytics application

from django.urls import path
from .views import *

urlpatterns = [
    
    path('', VoterListView.as_view(), name='voters'), # List view to shows all voters with filtering
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'), # Detail view to shows a single voter
]
