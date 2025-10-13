# file: mini_insta/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for mini_insta applicaitons

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import *

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

        # OLD :create a new Photo for this post only if image_url was provided
        # image_url = self.request.POST.get('image_url')
        # if image_url:
        #     photo = Photo(post=self.object, image_url=image_url)
        #     photo.save()

        # process uploaded image files
        files = self.request.FILES.getlist('image_file')
        for file in files:
            photo = Photo(post=self.object, image_file=file)
            photo.save()

        return response
    
class UpdateProfileView(UpdateView):
    '''Update user profile '''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html" 

class DeletePostView(DeleteView):
    '''A view to handle deletion of a Post
    (1) display a confirmation page (GET)
    (2) process the delete request and remove the Post (POST)
    '''
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    
    def get_context_data(self, **kwargs):
        '''Add the Post and Profile objects to the template context data'''
        context = super().get_context_data(**kwargs)
        
        # the Post object being deleted
        context['post'] = self.object
        
        # the Profile of the user who made the Post
        context['profile'] = self.object.profile
        
        return context
    
    def get_success_url(self):
        '''Return the URL to redirect to after successful deletion'''
        # redirect to the profile page of the user whose Post was deleted
        profile_pk = self.object.profile.pk
        return reverse('profile', kwargs={'pk': profile_pk})

class UpdatePostView(UpdateView):
    '''A view to handle updating an existing Post
    (1) display the HTML form pre-filled with current data (GET)
    (2) process the form submission and update the Post object (POST)
    '''
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    
    def get_context_data(self, **kwargs):
        '''Add the Post and Profile objects to the context data'''
        context = super().get_context_data(**kwargs)
        
        # the Post object being updated
        context['post'] = self.object
        
        # the Profile of the user who made the Post
        context['profile'] = self.object.profile
        
        return context
