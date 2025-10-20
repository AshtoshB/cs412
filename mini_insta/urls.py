# file: mini_insta/urls.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the urls that holds the URL patterns for mini_insta applicaitons

from django.urls import path
from .views import *

# URL patterns sepcific to the insta_mini app
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name ="profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name ="post_detail"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name = "create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/<int:pk>/feed', PostFeedListView.as_view(), name="show_feed"),
    path('profile/<int:pk>/search', SearchView.as_view(), name="search"),
]