# file: mini_insta/models.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the file to create models for mini_insta applicaitons 

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''Encapsulates the data of an indiviual user'''

    #define the data attributes of Profile model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.TextField(blank=True)
    display_name = models.CharField(max_length=90)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''retrun a string representation of this (Profile) model instance'''
        return f'{self.username}'
    
    def get_all_posts (self):
        '''Returns a QuerySet of Posts from this Profile'''

        #use the object manager to retriev posts related to this profile
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_absolute_url(self):
            '''Return the URL to display this Profile instance'''
            return reverse('profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        '''Return a list of those Profiles who are followers this profile'''
        
        followers = Follow.objects.filter(profile=self)

        follower_profiles = [] # list to contain the Profile of followers
        for follower in followers:
            follower_profiles.append(follower.follower_profile)

        return follower_profiles

    def get_num_followers(self):
        '''Return the count of followers'''
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        '''Return a list of those Profiles followed by this profile'''
        
        following = Follow.objects.filter(follower_profile=self)

        following_profiles = [] # list to contain the Profile objects being followed
        for follow in following:
            following_profiles.append(follow.profile)

        return following_profiles

    def get_num_following(self):
        '''Return the count of how many profiles are being followed'''
        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        '''Return a QuerySet of Posts from profiles this user is following, ordered by most recent first'''

        # Get all profiles that this profile is following
        following = Follow.objects.filter(follower_profile=self)

        # Extract the profile IDs from the Follow objects
        following_profile_ids = []

        for follow in following:
            following_profile_ids.append(follow.profile.id)
        
        # Get all posts from those profiles, ordered by most recent first
        posts = Post.objects.filter(profile__id__in=following_profile_ids).order_by('-timestamp')

        return posts


class Post(models.Model):
    '''Encapsulates the data of a user's post'''

    #define the data attributes of Post model
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) #forein key to indicate the relastionship to the Profile of the creator of this post
    caption = models.TextField(blank=True) #optional text associated with this post
    timestamp = models.DateTimeField(auto_now=True) #time at which this post was created/saved

    def __str__(self):
        '''retrun a string representation of this Post'''
        if self.caption:
            return f'{self.caption}'

        else: 
            return f'Post by {self.profile.username}'
    
    def get_all_photos (self):
        '''Returns a QuerySet of Photo for this Post'''

        #use the object manager to retriev photos related to this post
        photos = Photo.objects.filter(post=self)
        return photos

    def get_all_comments(self):
        '''Returns a QuerySet of Comments for this Post'''

        #use the object manager to retrieve comments related to this post
        comments = Comment.objects.filter(post=self).order_by('-timestamp')
        return comments

    def get_likes(self):
        '''Returns a QuerySet of Likes for this Post'''

        #use the object manager to retrieve likes related to this post
        likes = Like.objects.filter(post=self)
        return likes

    def get_likes_count(self):
        '''Returns the count of likes for this Post'''
        return Like.objects.filter(post=self).count()

    def get_likes_display_text(self):
        '''Returns formatted text for displaying likes (e.g., "Liked by @user and 5 others")'''
        likes = self.get_likes()
        count = likes.count()

        if count == 0:
            return "No likes yet"
        elif count == 1:
            return f"Liked by @{likes.first().profile.username}"
        else:
            others_count = count - 1
            others_text = "other" if others_count == 1 else "others"
            return f"Liked by @{likes.first().profile.username} and {others_count} {others_text}"

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model'''
        return reverse('post_detail', kwargs={'pk':self.pk})

class Photo(models.Model):
    '''Encapsulates the data for user's Photo for a Post'''
    
    #define the data attributes of Post model
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #foreign key to indicate the relationship to the Post to which this Photo is associated
    image_url = models.TextField(blank=True) #URL to an image
    image_file = models.ImageField(blank=True) #an actual image
    timestamp = models.DateTimeField(auto_now=True) #time at which this image was added

    def __str__(self):
        '''retrun a string representation of this Post'''
        if self.image_file:
            return f'Image file: {self.image_file.name}'
        
        elif self.image_url:
            return f'Image URL: {self.image_url}'
        else:
            return f'There is no image associated with this post'
        
    def get_image_url(self):
        '''return a image url for both image_url or image_file types'''
        if self.image_file:
            return self.image_file.url
        
        else:
            return self.image_url
    

class Follow(models.Model):
    '''Encapsulates the data for a Profile's Followers'''
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile") #indicates which profile is being followed (i.e., the “publisher”)
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile") #indicates  which profile is doing the following (i.e., the “subscriber”)
    timestamp = models.DateTimeField(auto_now=True) #the time at which the follower began following the other profile

    def __str__(self):
        '''retrun a string representation of the Follow'''

        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'


class Comment(models.Model):
    '''Encapsulates the data for a Post comment'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post") #indicates which post a comment belongs to
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="commenter_profile") #indicates which Profile commented on the post
    timestamp = models.DateTimeField(auto_now=True) #the time at which the Comment was made
    text = models.TextField(blank=False) #the actual Comment

    def __str__(self):
        '''return a string representation of the Comment'''
        return f'{self.profile.username}: {self.text[:50]}'

class Like(models.Model):
    '''Encapsulates the data for a Post like'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post") #indicates which post this Like belongs to
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="liker_profile") #indicates which Profile liked the post
    timestamp = models.DateTimeField(auto_now=True) #the time at which the Like was created

    def __str__(self):
        '''return a string representation of the Like'''
        return f'{self.profile.username} likes {self.post}'
