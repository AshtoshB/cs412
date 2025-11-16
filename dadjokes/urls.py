# file: dadjokes/urls.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the urls that holds the URL patterns for dadjokes REST API 

from django.urls import path
from .views import *

# URL patterns sepcific to the insta_mini app
urlpatterns = [

    # URLs for logged-in user's own profile (no pk needed)
    path(r'', RandomJokeAndPictureView.as_view(), name="main"),
    path(r'random/', RandomJokeAndPictureView.as_view(), name="random"),
    path(r'jokes/', JokeListView.as_view(), name='jokes'),
    path(r'joke/<int:pk>', JokeDetailView.as_view(), name = 'joke'),
    path(r'pictures/', PictureListView.as_view(), name='pictures'),
    path(r'picture/<int:pk>', PictureDetailView.as_view(), name = 'picture'),


    path(r'api/', RandomJokeDetailAPIView.as_view()),
    path(r'api/random', RandomJokeDetailAPIView.as_view()),

    path(r'api/jokes', JokeListAPIView.as_view()),
    path(r'api/joke/<int:pk>', JokeDetailAPIView.as_view()),
    path(r'api/pictures', PictureListAPIView.as_view()),
    path(r'api/picture/<int:pk>', PictureDetailAPIView.as_view()),
    path(r'api/random_picture', RandomPictureDetailAPIView.as_view()),


]