# file: mini_insta/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for mini_insta applicaitons

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all mini_insta Profiles.'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"

class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post
    template_name="mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    '''A view to handle creation of a new Post
    (1) display the HTML form to the user (GET)
    (2) process the form submission and store the new Post object (POST)
    '''
    form_class = CreatePostForm
    template_name="mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the context data'''
        
        # the Profile key attached to the URL pattern
        profile_pk = self.kwargs['pk']
        
        # from the provided reading/reference, https://docs.djangoproject.com/en/5.1/topics/class-based-views/mixins/ 
        # AuthorDetailView part, found how to get context dictionary from superclass 
        context = super().get_context_data(**kwargs)

        # the Profile object corresponding to the Profile key 
        profile = Profile.objects.get(pk=profile_pk)
        context["profile"] = profile


        return context
    
    def form_valid(self, form):
        '''Handle the form submission'''

        # the Profile object corresponding to the Profile key in the URL
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)

        # attach the profile object to the profile attribute
        form.instance.profile = profile

        # savign post 
        response = super().form_valid(form)

        # create a new Photo for this post only if image_url was provided
        image_url = self.request.POST.get('image_url')
        if image_url:
            photo = Photo(post=self.object, image_url=image_url)
            photo.save()

        return response