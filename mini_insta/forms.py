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