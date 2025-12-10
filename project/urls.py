# file: project/urls.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the urls that holds the URL patterns for project applicaitons

from django.urls import path
from .views import *
# generic view for authentication/authorization
from django.contrib.auth import views as auth_views

# URL patterns specific to the project app
urlpatterns = [
    # Main page - shows all media items
    path('', MainPageView.as_view(), name='main'),

    # Media detail - shows details of a specific media item
    path('media/<int:pk>/', MediaItemDetailView.as_view(), name='media_detail'),

    # Add/Edit watchlist entry - form to add or edit a media item in watchlist
    path('media/<int:pk>/watchlist/', AddEditWatchlistEntryView.as_view(), name='add_edit_watchlist'),

    # Delete watchlist entry
    path('watchlist/entry/<int:pk>/delete/', DeleteWatchlistEntryView.as_view(), name='delete_watchlist_entry'),

    # Delete rating
    path('rating/<int:pk>/delete/', DeleteRateMediaView.as_view(), name='delete_rating'),

    # Delete comment
    path('comment/<int:pk>/delete/', DeleteCommentMediaView.as_view(), name='delete_comment'),

    # My watchlist - shows logged-in user's profile and watchlist
    path('my-watchlist/', MyWatchlistView.as_view(), name='my_watchlist'),

    # Update profile
    path('profile/update/', UpdateUserProfileView.as_view(), name='update_profile'),

    # All watchlists - shows all users and their watchlists
    path('watchlists/', AllWatchlistsView.as_view(), name='all_watchlists'),

    # Specific watchlist - shows detail of a specific user's watchlist
    path('watchlist/<int:pk>/', SpecificWatchlistView.as_view(), name='watchlist_detail'),

    ## authorization-related URLs:
    path('login/', ProjectLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]