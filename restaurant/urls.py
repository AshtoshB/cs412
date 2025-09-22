# file: restaurant/urls.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for url patters for the restaurant app

from django.urls import path
from django.conf import settings
from . import views

# URL patterns sepcific to the resturant app
urlpatterns = [
    path (r'main/', views.main, name='main_page'), #path to main page(restaurant main page)
    path (r'order/', views.order, name='order_page'), #path to order page to make the order
    path (r'confirmation/', views.confirmation, name='confirmation_page'), #path to confirmation page to confirm the order
]