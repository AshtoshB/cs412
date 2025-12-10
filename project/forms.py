# file: project/forms.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: define the forms for project applicaitons we use for create/updaet/delete operations 

from django import forms
from .models import *


# documentatoin used for widgets: 
# https://docs.djangoproject.com/en/6.0/ref/forms/widgets/
# https://medium.com/@ptejendra91/understanding-django-widgets-a-detailed-guide-with-examples-1008084c05bf

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile in the database.'''

    class Meta:
        '''associate this form with the Profile model.'''
        model = UserProfile
        fields = ['display_name', 'bio', 'profile_pic']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update user profile information.'''

    class Meta:
        '''associate this form with the UserProfile model.'''
        model = UserProfile
        fields = ['display_name', 'bio', 'profile_pic', 'is_private']

class AddToWatchlistForm(forms.ModelForm):
    '''A form to add a media item to user's watchlist'''

    class Meta:
        model = WatchListEntry
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect
        }

        

class RateMediaForm(forms.ModelForm):
    '''A form to rate a media item'''

    class Meta:
        model = RateMedia
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=Rating.choices) 
        }

        

class CommentMediaForm(forms.ModelForm):
    '''A form to comment on a media item'''

    class Meta:
        model = CommentMedia
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 50})
        }

