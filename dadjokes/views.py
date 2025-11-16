# file: dadjokes/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for dadjokes applicaitons

from rest_framework import generics
from django.views.generic import TemplateView, DetailView, ListView
from django.shortcuts import render
from .serializers import *
import random
# Create your views here.
    

class RandomJokeAndPictureView(TemplateView):
    '''View that displays a random Joke and Picture'''

    template_name = 'dadjokes/random.html'

    
    # overwriting context data to add the joke and picture
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # retrieveing all Joke and Picture
        all_jokes = Joke.objects.all()
        all_pictures = Picture.objects.all()

        # passing only one random Joke and picture as context
        if all_jokes:
            context['joke'] = random.choice(all_jokes)
        if all_pictures:
            context['picture'] = random.choice(all_pictures)

        return context
    
class JokeListView(ListView):
    '''View that shows all Joke'''

    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    '''View that shows a detail page for a single Joke'''
    
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'

class PictureListView(ListView):
    '''View that shows all Picture'''

    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    '''View that shows a detail page for a single Picture'''

    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'pic'
   

class JokeListAPIView(generics.ListCreateAPIView):
    '''An API view to return a listing of Jokes and to create an Joke'''

    queryset  = Joke.objects.all()
    serializer_class  = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class RandomJokeDetailAPIView(generics.RetrieveAPIView):
    '''An API view to return a random Joke'''
    serializer_class = JokeSerializer
    
    def get_object(self):
        # Get a random joke from the database
        return Joke.objects.order_by('?').first()

class PictureListAPIView(generics.ListCreateAPIView):
    '''An API view to return a listing of Pictures and to create an Picture'''

    queryset  = Picture.objects.all()
    serializer_class  = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureDetailAPIView(generics.RetrieveAPIView):
    '''An API view to return a random Picture'''
    serializer_class = PictureSerializer
    
    def get_object(self):
        # Get a random joke from the database
        return Picture.objects.order_by('?').first()
