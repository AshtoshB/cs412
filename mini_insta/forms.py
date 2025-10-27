# # file: mini_insta/forms.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: define the forms for mini_insta applicaitons we use for create/updaet/delete operations 

from django import forms
from .models import *

class CreatePostForm (forms.ModelForm):
    '''A form to add a Post to the database,'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database.'''

    class Meta:
        '''associate this form with the Profile model.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']


class UpdatePostForm(forms.ModelForm):
    '''A form to update a Post in the database.'''

    class Meta:
        '''associate this form with the Post model.'''
        model = Post
        fields = ['caption']


class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile in the database.'''

    class Meta:
        '''associate this form with the Profile model.'''
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']


class CreateCommentForm(forms.ModelForm):
    '''A form to create a new Comment in the database.'''

    class Meta:
        '''associate this form with the Comment model.'''
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }
