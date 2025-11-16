# file: dadjokes/models.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the file to create models for dad_jokes applicaitons 

from django.db import models

# Create your models here.


class Joke(models.Model):
    '''A model that represents a text based joke'''

    text = models.TextField(blank=False) # the text of the joke
    name = models.TextField(blank=False) # the name of the contributor
    timestamp = models.DateTimeField(auto_now=True) # timestamp of when the Joke was created


class Picture(models.Model):
    '''A model that represents a picutre based joke'''

    image_url = models.TextField(blank=False) # the url of the joke image or GIF
    name = models.TextField(blank=False) # the name of the contributor
    timestamp = models.DateTimeField(auto_now=True) # timestamp of when the Joke was created

