# file: mini_insta/models.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the file to create models for mini_insta applicaitons 

from django.db import models
from django.urls import reverse

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
    
    def get_all_posts (self):
        '''Returns a QuerySet of Posts from this Profile'''

        #use the object manager to retriev posts related to this profile
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_absolute_url(self):
            '''Return the URL to display this Profile instance'''
            return reverse('profile', kwargs={'pk': self.pk})

    
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
    
  