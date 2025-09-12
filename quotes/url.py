from django.urls import path
from django.conf import settings
from . import views

# URL patterns sepcific to the quotes app
urlpatterns = [
    path (r'', views.main, name ='main'), #path to main page(quotes page)
    path(r'quote', views.main, name='quote'), #path to quote page 
    path (r'show_all/', views.show_all, name='show_all'), #path to show_all page
    path (r'about/', views.about, name = 'about')  #path to the about page

]