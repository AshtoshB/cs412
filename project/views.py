# file: project/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for project applicaitons

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib import messages
import requests
from datetime import datetime
from django.conf import settings

# Create your views here.
class CreateProfileView(CreateView):
    '''View to create a profile.'''
    model = UserProfile
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'

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
        return reverse('main')


class MainPageView(ListView):
    """Display all movies and shows with search and OMDb API fallback"""
    model = MediaItem
    template_name = 'project/main.html'
    context_object_name = 'media_items'
    paginate_by = 20

    def get_queryset(self):
        queryset = MediaItem.objects.all()
        search_query = self.request.GET.get('search', '').strip()

        # If user typed something into search:
        if search_query:
            # First search Django DB
            db_results = queryset.filter(title__icontains=search_query)

            if db_results.exists():
                queryset = db_results

            else:
                # Nothing in DB, so instead try OMDb
                try:
                    api_url = "https://www.omdbapi.com/"
                    search_params = {
                        "s": search_query,
                        "apikey": settings.OMDB_API_KEY
                    }

                    search_res = requests.get(api_url, params=search_params, timeout=5)
                    search_data = search_res.json()

                    if search_data.get("Response") == "True" and "Search" in search_data:
                        created_ids = []

                        for entry in search_data["Search"]:
                            imdb_id = entry.get("imdbID")
                            if not imdb_id:
                                continue

                            # Check if this entry already exists in DB
                            existing = MediaItem.objects.filter(description__icontains=imdb_id)
                            if existing.exists():
                                created_ids.append(existing.first().id)
                                continue

                            # Fetch full details
                            detail_params = {
                                "i": imdb_id,
                                "apikey": settings.OMDB_API_KEY
                            }
                            detail_res = requests.get(api_url, params=detail_params, timeout=5)
                            detail = detail_res.json()

                            if detail.get("Response") != "True":
                                continue

                            # Determine media type
                            omdb_type = detail.get("Type")
                            if omdb_type == "movie":
                                media_type = "movie"
                            elif omdb_type == "series":
                                media_type = "show"
                            else:
                                media_type = "unknown"

                            # Parse release date
                            year = detail.get("Year", "2000")[:4]
                            try:
                                release_date = datetime(int(year), 1, 1)
                            except:
                                release_date = datetime(2000, 1, 1)

                            # Parse rating safely
                            imdb_rating = detail.get("imdbRating")
                            try:
                                rating = (
                                    int(float(imdb_rating))
                                    if imdb_rating not in ("N/A", None)
                                    else None
                                )
                            except:
                                rating = None

                            # Create item
                            new_item = MediaItem.objects.create(
                                title=detail.get("Title", "Unknown Title"),
                                type=media_type,
                                release_date=release_date,
                                poster_url=detail.get("Poster", ""),
                                description=f"{detail.get('Plot', '')}\nIMDbID: {imdb_id}",
                                rating=rating,
                                season_ep={}
                            )

                            created_ids.append(new_item.id)

                        queryset = MediaItem.objects.filter(id__in=created_ids)

                    else:
                        queryset = MediaItem.objects.none()

                except Exception:
                    queryset = MediaItem.objects.none()

        # Filtering 
        media_type = self.request.GET.get('type', '')
        if media_type:
            queryset = queryset.filter(type=media_type)

        min_rating = self.request.GET.get('min_rating', '')
        if min_rating:
            queryset = queryset.filter(rating__gte=int(min_rating))

        max_rating = self.request.GET.get('max_rating', '')
        if max_rating:
            queryset = queryset.filter(rating__lte=int(max_rating))

        release_year = self.request.GET.get('release_year', '')
        if release_year:
            queryset = queryset.filter(release_date__year=release_year)

        return queryset.order_by('-release_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['min_rating'] = self.request.GET.get('min_rating', '')
        context['max_rating'] = self.request.GET.get('max_rating', '')
        context['release_year'] = self.request.GET.get('release_year', '')
        context['media_types'] = MEDIA_TYPES
        return context



class MediaItemDetailView(DetailView):
    '''View to display details of a specific movie or show'''
    model = MediaItem
    template_name = 'project/media_detail.html'
    context_object_name = 'media_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_item = self.get_object()

        # Get public reviews (ratings and comments) from other users
        public_reviews = []

        # Get all watchlist entries for this media item
        watchlist_entries = WatchListEntry.objects.filter(
            media_item=media_item
        ).select_related('user_profile')

        for entry in watchlist_entries:
            # Check if user profile is public
            if not entry.user_profile.is_private:
                review_data = {
                    'user': entry.user_profile.display_name,
                    'rating': None,
                    'comment': None
                }

                # Get rating if exists
                try:
                    rate_media = RateMedia.objects.get(watchlist_entry=entry)
                    review_data['rating'] = rate_media.rating
                except RateMedia.DoesNotExist:
                    pass

                # Get comment if exists
                try:
                    comment_media = CommentMedia.objects.get(watchlist_entry=entry)
                    review_data['comment'] = comment_media.comment
                except CommentMedia.DoesNotExist:
                    pass

                # Only add if there's a rating or comment
                if review_data['rating'] is not None or review_data['comment']:
                    public_reviews.append(review_data)

        context['public_reviews'] = public_reviews

        # Check if current user has this in their watchlist
        context['in_watchlist'] = False
        if self.request.user.is_authenticated:
            try:
                user_profile = self.request.user.user_profile
                context['in_watchlist'] = WatchListEntry.objects.filter(
                    user_profile=user_profile,
                    media_item=media_item
                ).exists()
            except UserProfile.DoesNotExist:
                pass

        return context

class AllWatchlistsView(ListView):
    '''View to display all users and their watchlists'''
    model = UserProfile
    template_name = 'project/all_watchlists.html'
    context_object_name = 'user_profiles'

    def get_queryset(self):
        # Only return public user profiles who have watchlist entries
        return UserProfile.objects.filter(
            watchlist_entries__isnull=False,
            is_private=False
        ).distinct()

class SpecificWatchlistView(DetailView):
    '''View to display a specific user's watchlist with categorized status'''
    model = UserProfile
    template_name = 'project/watchlist_detail.html'
    context_object_name = 'user_profile'

    def get(self, request, *args, **kwargs):
        '''Check if profile is private before displaying'''
        user_profile = self.get_object()
        if user_profile.is_private:
            # Redirect to all watchlists page if profile is private
            messages.warning(request, f"{user_profile.display_name}'s watchlist is private.")
            return redirect('all_watchlists')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        # Get all watchlist entries for this user profile
        watchlist_entries = WatchListEntry.objects.filter(user_profile=user_profile)

        # Helper function to add rating and comment to entry
        def add_rating_comment(entry):
            entry_data = {
                'entry': entry,
                'rating': None,
                'comment': None
            }

            # Get rating if exists
            try:
                rate_media = RateMedia.objects.get(watchlist_entry=entry)
                entry_data['rating'] = rate_media.rating
            except RateMedia.DoesNotExist:
                pass

            # Get comment if exists
            try:
                comment_media = CommentMedia.objects.get(watchlist_entry=entry)
                entry_data['comment'] = comment_media.comment
            except CommentMedia.DoesNotExist:
                pass

            return entry_data

        # Categorize by status and add rating/comment
        watched = [add_rating_comment(entry) for entry in watchlist_entries.filter(status='watched')]
        want_to_watch = [add_rating_comment(entry) for entry in watchlist_entries.filter(status='want_to_watch')]

        # Add episode progress information for "watching" shows
        watching_with_progress = []
        for entry in watchlist_entries.filter(status='watching'):
            progress_info = add_rating_comment(entry)
            progress_info['total_episodes'] = 0
            progress_info['watched_episodes'] = 0

            # Calculate total episodes for the show
            if entry.media_item.season_ep:
                total_episodes = sum(entry.media_item.season_ep.values())
                progress_info['total_episodes'] = total_episodes

            # Calculate watched episodes
            episode_progress = entry.get_episode_progress()
            if episode_progress:
                watched_episodes = 0
                for ep_prog in episode_progress:
                    if ep_prog.season_ep_watched:
                        for season, episodes in ep_prog.season_ep_watched.items():
                            watched_episodes += len(episodes)
                progress_info['watched_episodes'] = watched_episodes

            watching_with_progress.append(progress_info)

        context['watched'] = watched
        context['watching'] = watching_with_progress
        context['want_to_watch'] = want_to_watch

        return context

class ProjectLoginView(auth_views.LoginView):
    '''Custom login view that redirects to main page after login'''
    template_name = 'project/login.html'

    def get_success_url(self):
        return reverse('main')

# Mixin for authenticated users
class AuthenticatedUserMixin(LoginRequiredMixin):
    '''Mixin that requires login and provides helper method to get the logged-in user's UserProfile'''

    def get_user_profile(self):
        '''Return the UserProfile object associated with the logged-in user'''
        return UserProfile.objects.get(user=self.request.user)

    def get_login_url(self):
        '''Return the URL to the login page'''
        return reverse('login')

class MyWatchlistView(AuthenticatedUserMixin, DetailView):
    '''Display the logged-in user's profile and watchlist'''
    model = UserProfile
    template_name = 'project/my_watchlist.html'
    context_object_name = 'user_profile'

    def get_object(self):
        '''Return the logged-in user's UserProfile'''
        return self.get_user_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        # Get all watchlist entries for this user profile
        watchlist_entries = WatchListEntry.objects.filter(user_profile=user_profile)

        # Categorize by status and add rating/comment
        def add_rating_comment(entry):
            entry_data = {
                'entry': entry,
                'rating': None,
                'comment': None
            }

            # Get rating if exists
            try:
                rate_media = RateMedia.objects.get(watchlist_entry=entry)
                entry_data['rating'] = rate_media.rating
                entry_data['rate_media'] = rate_media
            except RateMedia.DoesNotExist:
                pass

            # Get comment if exists
            try:
                comment_media = CommentMedia.objects.get(watchlist_entry=entry)
                entry_data['comment'] = comment_media.comment
                entry_data['comment_media'] = comment_media
            except CommentMedia.DoesNotExist:
                pass

            return entry_data

        watched = [add_rating_comment(entry) for entry in watchlist_entries.filter(status='watched')]
        want_to_watch = [add_rating_comment(entry) for entry in watchlist_entries.filter(status='want_to_watch')]

        # Add episode progress information for "watching" shows
        watching_with_progress = []
        for entry in watchlist_entries.filter(status='watching'):
            progress_info = add_rating_comment(entry)
            progress_info['total_episodes'] = 0
            progress_info['watched_episodes'] = 0

            # Calculate total episodes for the show
            if entry.media_item.season_ep:
                total_episodes = sum(entry.media_item.season_ep.values())
                progress_info['total_episodes'] = total_episodes

            # Calculate watched episodes
            episode_progress = entry.get_episode_progress()
            if episode_progress:
                watched_episodes = 0
                for ep_prog in episode_progress:
                    if ep_prog.season_ep_watched:
                        for season, episodes in ep_prog.season_ep_watched.items():
                            watched_episodes += len(episodes)
                progress_info['watched_episodes'] = watched_episodes

            watching_with_progress.append(progress_info)

        context['watched'] = watched
        context['watching'] = watching_with_progress
        context['want_to_watch'] = want_to_watch

        return context

class UpdateUserProfileView(AuthenticatedUserMixin, UpdateView):
    '''Update user profile'''
    model = UserProfile
    form_class = UpdateProfileForm
    template_name = "project/update_profile_form.html"

    def get_object(self):
        '''Return the logged-in user's UserProfile'''
        return self.get_user_profile()

    def get_success_url(self):
        '''Return URL to redirect to after successful profile update'''
        return reverse('my_watchlist')

class AddEditWatchlistEntryView(AuthenticatedUserMixin, View):
    '''View to add or edit a watchlist entry'''

    def get(self, request, pk):
        '''Display the form to add/edit watchlist entry'''
        media_item = MediaItem.objects.get(pk=pk)
        user_profile = self.get_user_profile()

        # Check if entry already exists
        try:
            entry = WatchListEntry.objects.get(user_profile=user_profile, media_item=media_item)
            form = AddToWatchlistForm(instance=entry)
            is_new = False
        except WatchListEntry.DoesNotExist:
            form = AddToWatchlistForm()
            entry = None
            is_new = True

        # Get existing rating and comment if they exist
        rating_form = None
        comment_form = None

        if entry:
            try:
                rate_media = RateMedia.objects.get(watchlist_entry=entry)
                rating_form = RateMediaForm(instance=rate_media)
            except RateMedia.DoesNotExist:
                rating_form = RateMediaForm()

            try:
                comment_media = CommentMedia.objects.get(watchlist_entry=entry)
                comment_form = CommentMediaForm(instance=comment_media)
            except CommentMedia.DoesNotExist:
                comment_form = CommentMediaForm()
        else:
            rating_form = RateMediaForm()
            comment_form = CommentMediaForm()

        context = {
            'media_item': media_item,
            'form': form,
            'rating_form': rating_form,
            'comment_form': comment_form,
            'is_new': is_new,
            'entry': entry
        }
        return render(request, 'project/add_edit_watchlist.html', context)

    def post(self, request, pk):
        '''Process the form submission'''
        media_item = MediaItem.objects.get(pk=pk)
        user_profile = self.get_user_profile()

        # Get or create watchlist entry
        try:
            entry = WatchListEntry.objects.get(user_profile=user_profile, media_item=media_item)
            form = AddToWatchlistForm(request.POST, instance=entry)
        except WatchListEntry.DoesNotExist:
            form = AddToWatchlistForm(request.POST)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.user_profile = user_profile
            entry.media_item = media_item
            entry.save()

            # Handle rating
            rating = request.POST.get('rating')
            if rating:
                RateMedia.objects.update_or_create(
                    watchlist_entry=entry,
                    defaults={'rating': rating}
                )

            # Handle comment
            comment = request.POST.get('comment')
            if comment:
                CommentMedia.objects.update_or_create(
                    watchlist_entry=entry,
                    defaults={'comment': comment}
                )

            return redirect('my_watchlist')

        return redirect('add_edit_watchlist', pk=pk)

class DeleteWatchlistEntryView(AuthenticatedUserMixin, DeleteView):
    '''Delete a watchlist entry'''
    model = WatchListEntry
    template_name = "project/delete_watchlist_entry.html"

    def get_success_url(self):
        '''Return URL to redirect to after successful deletion'''
        return reverse('my_watchlist')

class DeleteRateMediaView(AuthenticatedUserMixin, TemplateView):
    '''Delete a media rating'''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the delete operation and redirect'''
        rate_media = RateMedia.objects.get(pk=self.kwargs['pk'])
        rate_media.delete()
        return redirect('my_watchlist')

class DeleteCommentMediaView(AuthenticatedUserMixin, TemplateView):
    '''Delete a media comment'''

    def dispatch(self, request, *args, **kwargs):
        '''Handle the delete operation and redirect'''
        comment_media = CommentMedia.objects.get(pk=self.kwargs['pk'])
        comment_media.delete()
        return redirect('my_watchlist')

