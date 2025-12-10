# file: project/models.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the file to create models for project applicaitons 

from django.db import models
from django.contrib.auth.models import User


# media type choices for MediaItem model's type attribute; type of media (moive, show, or unknown)
# learned to use it from : https://www.geeksforgeeks.org/python/how-to-use-django-field-choices/
MEDIA_TYPES = [
    ('movie', 'Movie'),
    ('show', 'Show'),
    ('unknown', 'Unknown')
]

# watch staus choices for WatchListEntry's status attribute
#  status of the media in the watchlist (watching, watched, want to watch)
WATCH_STATUS = [
    ('watching', 'Watching'),
    ('want_to_watch', 'Want to watch'),
    ('watched', 'Watched')
]


#https://docs.djangoproject.com/en/5.2/ref/models/fields/
class Rating(models.IntegerChoices):
    Unrated = 0
    Awful = 1
    Bad = 2
    Ok = 3
    Good = 4
    Great = 5



# Create your models here.
class MediaItem(models.Model):
    '''Encapsulates the data of a movie or show media item'''

    title = models.TextField(blank=False) # Title of the media (title of moive or show)
    type = models.CharField(max_length=20, blank=False, choices=MEDIA_TYPES, default='unknown') # type of media (choice between movie, show, or unknown)
    release_date = models.DateField(blank=False, auto_now=False) # media's release date
    poster_url = models.URLField() # Url for the movie or show's poster
    description = models.TextField(blank=True) # description of the show or moive
    rating =  models.IntegerField(blank=True, null=True) # rating of the show or movie 
    
    # the episodes per season for shows media 
    # E.g: {"1": 10, "2": 11} means season 1 has 10 episodes, season 2 has 11 episodes
    season_ep = models.JSONField(default=dict) 

    def __str__(self):
        '''return a string representation of this MediaItem'''

        return f"{self.type}: {self.title}, released in {self.release_date}"

class UserProfile(models.Model):
    '''Encapsulates the User's general data'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    display_name = models.CharField(max_length=10, blank=False)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True)
    is_private = models.BooleanField(default=False)  # Privacy setting: True = private watchlist, False = public

    def __str__(self):
        '''return a string representation of User's Profile'''
        return f"{self.user.username}'s profile: going by {self.display_name}"

class WatchListEntry(models.Model):
    '''Encapsulates the User's data of a movie or show media item'''

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='watchlist_entries', null=True, blank=True) # foreign key to UserProfile that this entry belongs to
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name='watchlist_entries') # foreign key to MediaItem in the watchlist
    status = models.CharField(max_length=20, blank=False, choices=WATCH_STATUS, default='want_to_watch') # viewing staus of the media item
    date_added = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        '''return a string representation of this WatchListEntry'''
        return f"{self.user_profile.display_name} has {self.media_item.title} in their list as {self.status}"
        
    
    def get_episode_progress(self):
        '''Returns a QuerySet of EpisodeProgress for this WatchListEntry'''

        #using the object manager to retriev and return episode progress related to this media entry
        return EpisodeProgress.objects.filter(watchlist_entry=self)
        
    
    def get_total_episodes(self):
        '''Returns a dictionary of all seasons and its episodes (dictionary)'''
        
        return self.media_item.season_ep

class EpisodeProgress(models.Model):
    '''Encapsulates the data of a show media item in Users WatchListEntry'''

    watchlist_entry = models.ForeignKey(WatchListEntry, on_delete=models.CASCADE, related_name='episode_progress') #foreign key to WatchListEntry that this EpisodeProgress belongs to 
    
    # dictonary that contains episodes per seasons watched by a user
    # key: seasons watched, value: list of episodes watched
    # E.g: {"1": [1,2,3], "2": [1,2]} means watched episodes 1, 2 and3 of season 1 and episodes 1 and 2 of season 2
    season_ep_watched = models.JSONField(default=dict, blank=True)

    def __str__(self):
        '''return a string representation of WatchListEntry's EpisodeProgress'''
        display_name = self.watchlist_entry.user_profile.display_name

        if self.season_ep_watched and "1" in self.season_ep_watched and self.season_ep_watched["1"]:
            season_one_eps_watched = self.season_ep_watched["1"]
            ep_range = f"{season_one_eps_watched[0]}-{season_one_eps_watched[-1]}"
            return f"{display_name} has watched episodes {ep_range} of season 1 of {self.watchlist_entry.media_item.title}"

        return f"{display_name}'s episode progress for {self.watchlist_entry.media_item.title}"
    

class RateMedia(models.Model):
    '''Encapsulates the User's rating for a WatchListEntry'''

    watchlist_entry = models.OneToOneField(WatchListEntry, on_delete=models.CASCADE) #foreign key to WatchListEntry that this rating belongs to
    rating = models.IntegerField(choices=Rating) # user rating of the media

    def __str__(self):
        '''return a string representation of rating of media in WatchListEntry of a User'''
        display_name = self.watchlist_entry.user_profile.display_name
        return f"{display_name} rates {self.watchlist_entry.media_item.title} {self.rating}/5"

class CommentMedia(models.Model):
    '''Encapsulates the User's comment on a MediaItem in their WatchListEntry'''

    watchlist_entry = models.OneToOneField(WatchListEntry, on_delete=models.CASCADE, related_name='media_comment')
    comment = models.CharField(max_length=250)

    def __str__(self):
        '''Return a string representation of a comment on a media by a User'''
        display_name = self.watchlist_entry.user_profile.display_name 
        return f"{display_name} commented on {self.watchlist_entry.media_item.title}"

