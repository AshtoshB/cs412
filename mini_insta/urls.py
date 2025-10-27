# file: mini_insta/urls.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the urls that holds the URL patterns for mini_insta applicaitons

from django.urls import path
from .views import *
# generic view for authentication/authorization
from django.contrib.auth import views as auth_views

# URL patterns sepcific to the insta_mini app
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all"),

    # URLs for logged-in user's own profile (no pk needed)
    path('profile/', ProfileDetailView.as_view(), name="my_profile"),  # Show logged-in user's profile
    path('profile/feed/', PostFeedListView.as_view(), name="show_feed"),
    path('profile/search/', SearchView.as_view(), name="search"),
    path('profile/update/', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/create_post/', CreatePostView.as_view(), name="create_post"),

    # URLs that view other profiles/posts (pk still needed)
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="profile"),
    path('profile/<int:pk>/follow/', FollowView.as_view(), name="follow"),
    path('profile/<int:pk>/delete_follow/', DeleteFollowView.as_view(), name="delete_follow"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/like/', LikeView.as_view(), name="like"),
    path('post/<int:pk>/delete_like/', DeleteLikeView.as_view(), name="delete_like"),
    path('post/<int:pk>/comment/', CreateCommentView.as_view(), name="create_comment"),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers/', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following/', ShowFollowingDetailView.as_view(), name="show_following"),
    
    ## authorization-related URLs:
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]