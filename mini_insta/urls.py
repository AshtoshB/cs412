# file: mini_insta/urls.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the urls that holds the URL patterns for mini_insta applicaitons

from django.urls import path
from .views import ProfileListView, ProfileDetailView

# URL patterns sepcific to the insta_mini app
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name ="profile"),
]