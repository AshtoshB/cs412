# file: mini_insta/admin.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the admin register for models in mini_insta application 

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile) #registering Profile model
admin.site.register(Post)    #registering Post model
admin.site.register(Photo)   #registering Photo model