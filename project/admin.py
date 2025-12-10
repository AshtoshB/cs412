# file: project/admin.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the admin register for models in project application 

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MediaItem)         #registering MediaItem model
admin.site.register(UserProfile)       #registering UserProfile model
admin.site.register(WatchListEntry)    #registering WatchListEntry model
admin.site.register(EpisodeProgress)   #registering EpisodeProgress model
admin.site.register(RateMedia)         #registering RateMedia model
admin.site.register(CommentMedia)      #registering CommentMeida model