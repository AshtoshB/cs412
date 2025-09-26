# file: mini_insta/models.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the file to create models for mini_insta applicaitons 

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulates the data of an indiviual user'''
    
    #define the data attributes of Profile model
    username = models.TextField(blank=True)
    display_name = models.CharField(max_length=90)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''retrun a string representation of this (Profile) model instance'''
        return f'{self.username}'

