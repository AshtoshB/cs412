# file: dadjokes/admin.py
# author: Ashtosh Bhandari ashtosh@bu.edu


from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)