# file: mini_insta/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for mini_insta applicaitons

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from .models import Profile, Post, Photo, Follow, Like
from .forms import *

# Create your views here.

class AuthenticatedProfileMixin(LoginRequiredMixin):
    '''Mixin that requires login and provides helper method to get the logged-in user's Profile'''

    def get_profile(self):
        '''Return the Profile object associated with the logged-in user'''
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self):
        '''Return the URL to the login page for this application'''
        return reverse('login')

class ProfileListView(ListView):
    '''Define a view class to show all mini_insta Profiles.'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''Return the Profile object - either from pk or from logged-in user'''
        # If pk is in URL, use default behavior to show that profile
        if 'pk' in self.kwargs:
            return super().get_object()
        # Otherwise, return the logged-in user's profile (for 'my_profile' URL)
        else:
            return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        '''Add information about whether the logged-in user is following this profile'''
        context = super().get_context_data(**kwargs)

        # Check if user is authenticated
        if self.request.user.is_authenticated:
            # Get the logged-in user's profile
            logged_in_profile = Profile.objects.get(user=self.request.user)

            # Check if logged-in user is following this profile
            is_following = Follow.objects.filter(
                follower_profile=logged_in_profile,
                profile=self.object
            ).exists()

            context['is_following'] = is_following

        return context

class CreateProfileView(CreateView):
    '''View to create a profile.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        '''Add any additional context if needed.'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()  #add a user creation form to the context
        return context

    def form_valid(self, form):
        '''Create the associated User object before saving the Profile.'''
        signup_form = UserCreationForm(self.request.POST)
        if signup_form.is_valid(): #check if the user creation form is valid
            user = signup_form.save()  #create the User object
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')  #log in the new user
            form.instance.user = user  #associate the User with the Profile
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        '''Return URL to redirect to after successful profile creation'''
        return reverse('my_profile')

class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post
    template_name="mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        '''Add information about whether the logged-in user has liked this post'''
        context = super().get_context_data(**kwargs)

        # Check if user is authenticated
        if self.request.user.is_authenticated:
            # Get the logged-in user's profile
            logged_in_profile = Profile.objects.get(user=self.request.user)

            # Check if logged-in user has liked this post
            has_liked = Like.objects.filter(
                profile=logged_in_profile,
                post=self.object
            ).exists()

            context['has_liked'] = has_liked

        return context

class CreatePostView(AuthenticatedProfileMixin, CreateView):
    '''A view to handle creation of a new Post
    (1) display the HTML form to the user (GET)
    (2) process the form submission and store the new Post object (POST)
    '''
    form_class = CreatePostForm
    template_name="mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the context data'''

        context = super().get_context_data(**kwargs)

        # Get the logged-in user's profile
        profile = self.get_profile()
        context["profile"] = profile

        return context

    def form_valid(self, form):
        '''Handle the form submission'''

        # Get the logged-in user's profile
        profile = self.get_profile()

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

    def get_success_url(self):
        '''Return URL to redirect to after successful post creation'''
        return reverse('my_profile')

class UpdateProfileView(AuthenticatedProfileMixin, UpdateView):
    '''Update user profile '''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        '''Return the logged-in user's Profile'''
        return self.get_profile()

    def get_success_url(self):
        '''Return URL to redirect to after successful profile update'''
        return reverse('my_profile')

class DeletePostView(AuthenticatedProfileMixin, DeleteView):
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

class UpdatePostView(AuthenticatedProfileMixin, UpdateView):
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

class ShowFollowersDetailView(DetailView):
    '''Display a profile's followers'''

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    '''Display who a profile is following'''

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(AuthenticatedProfileMixin, DetailView):
    '''Display the post feed for a profile - shows posts from profiles they follow'''

    model = Profile
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"

    def get_object(self):
        '''Return the logged-in user's Profile'''
        return self.get_profile()

    def get_context_data(self, **kwargs):
        '''Add the post feed to the context'''
        context = super().get_context_data(**kwargs)

        # Get the post feed for this profile
        context['posts'] = self.object.get_post_feed()

        return context

class SearchView(AuthenticatedProfileMixin, ListView):
    '''Display search form and search results for profiles and posts'''

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request - show search form if no query, otherwise show results'''

        # Check if query parameter is present
        if 'query' not in self.request.GET or not self.request.GET['query']:

            # No query, show the search form
            profile = self.get_profile()
            return render(request, 'mini_insta/search.html', {'profile': profile})

        # Query present, continue with normal ListView behavior
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return Posts that match the search query'''

        # Get the query from the GET parameters
        query = self.request.GET.get('query', '')

        # Search for posts where the caption contains the query
        posts = Post.objects.filter(caption__icontains=query)

        return posts

    def get_context_data(self, **kwargs):
        '''Add profile, query, and matching profiles to context'''
        context = super().get_context_data(**kwargs)

        # Get the logged-in user's profile
        profile = self.get_profile()
        context['profile'] = profile

        # Get the query
        query = self.request.GET.get('query', '')
        context['query'] = query

        # Get matching profiles (search in username, display_name, or bio_text)
        matching_username = Profile.objects.filter(username__icontains=query)
        matching_name =  Profile.objects.filter(display_name__icontains=query)
        matching_bio = Profile.objects.filter(bio_text__icontains=query)

        matching_profiles = matching_username | matching_name | matching_bio
        context['profiles'] = matching_profiles

        return context

class FollowView(AuthenticatedProfileMixin, TemplateView):
    '''View to create a Follow relationship between logged-in user and another profile'''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the follow operation and redirect back to the profile'''

        # Get the logged-in user's profile (the follower)
        follower_profile = self.get_profile()

        # Get the profile to follow (from URL pk parameter)
        profile_to_follow = Profile.objects.get(pk=self.kwargs['pk'])

        # Create the Follow relationship if it doesn't already exist
        # and if the user is not trying to follow themselves
        if follower_profile != profile_to_follow:
            Follow.objects.get_or_create(
                follower_profile=follower_profile,
                profile=profile_to_follow
            )

        # Redirect back to the profile page
        return redirect('profile', pk=profile_to_follow.pk)

class DeleteFollowView(AuthenticatedProfileMixin, TemplateView):
    '''View to delete a Follow relationship between logged-in user and another profile'''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the unfollow operation and redirect back to the profile'''

        # Get the logged-in user's profile (the follower)
        follower_profile = self.get_profile()

        # Get the profile to unfollow (from URL pk parameter)
        profile_to_unfollow = Profile.objects.get(pk=self.kwargs['pk'])

        # Delete the Follow relationship if it exists
        Follow.objects.filter(
            follower_profile=follower_profile,
            profile=profile_to_unfollow
        ).delete()

        # Redirect back to the profile page
        return redirect('profile', pk=profile_to_unfollow.pk)

class LikeView(AuthenticatedProfileMixin, TemplateView):
    '''View to create a Like relationship between logged-in user and a post'''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the like operation and redirect back to the post'''

        # Get the logged-in user's profile
        profile = self.get_profile()

        # Get the post to like (from URL pk parameter)
        post = Post.objects.get(pk=self.kwargs['pk'])

        # Create the Like relationship if it doesn't already exist
        # and if the user is not trying to like their own post
        if post.profile != profile:
            Like.objects.get_or_create(
                profile=profile,
                post=post
            )

        # Redirect back to the post page
        return redirect('post_detail', pk=post.pk)

class DeleteLikeView(AuthenticatedProfileMixin, TemplateView):
    '''View to delete a Like relationship between logged-in user and a post'''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the unlike operation and redirect back to the post'''

        # Get the logged-in user's profile
        profile = self.get_profile()

        # Get the post to unlike (from URL pk parameter)
        post = Post.objects.get(pk=self.kwargs['pk'])

        # Delete the Like relationship if it exists
        Like.objects.filter(
            profile=profile,
            post=post
        ).delete()

        # Redirect back to the post page
        return redirect('post_detail', pk=post.pk)

class CreateCommentView(AuthenticatedProfileMixin, CreateView):
    '''View to create a Comment on a Post'''

    form_class = CreateCommentForm
    template_name = 'mini_insta/create_comment_form.html'

    def form_valid(self, form):
        '''Handle the form submission - associate the comment with the post and profile'''

        # Get the logged-in user's profile
        profile = self.get_profile()

        # Get the post to comment on (from URL pk parameter)
        post = Post.objects.get(pk=self.kwargs['pk'])

        # Associate the comment with the profile and post
        form.instance.profile = profile
        form.instance.post = post

        # Save the comment
        return super().form_valid(form)

    def get_success_url(self):
        '''Return URL to redirect to after successful comment creation'''
        # Redirect back to the post detail page
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})
