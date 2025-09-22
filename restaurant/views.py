# file: restaurant/views.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the controller for restaurant appilcaiton 

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Images for the reusturant (photos are of an actual Itialian bakery shop I worked in )
resturant_images = ["https://static.where-e.com/United_States/Massachusetts/Bristol_County/Marzillis-Bakery_4dbc54ae49d0df810422636cd86aa0ce.jpg",
          "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgZ8y_evB7UQ9nrU1DkDcGbTpLwvckUJ-at8imdn7T2-A0pKSdRfPoot_MoOqRnCAhIH26iSc0FSFmGjWuGegUDYhmZDQ-Da6MdqD7BkKh2VUlqS4Le6S1qSzHiGkA3gdKk4C3amUHnprg/s280/100_4272.jpg",
        ]

# regular menue list that contain a dictionary of 
menu = {
    'Italian Sandwich': {'ingredients': 'Mortadella, Salami, Hot Ham', 'price': 5.45},
    'Turkey Club Sandwich': {'ingredients': 'Turkey, Bacon, Lettuce, Tomatoes', 'price': 7.85},
    'Pastrami Sandwich': {'ingredients': 'Pastrami Meat', 'price': 6.70},
    'Cheeseburger Sandwich': {'ingredients': 'Beef Patty, American Cheese, Lettuce', 'price': 8.99},
}

special_menu = {
    'Thanksgiving Sandwich': {'ingredients': 'Turkey, Crannberry, Stuffings', 'price': 8.25},
    'Combo Sandwich': {'ingredients': 'Meatball, Italian Sausage', 'price': 8.25},
    'Seafood Salad Sandwich': {'ingredients': 'Surimi, Shrimp, Crab, Mayonnaise', 'price': 8.25},
    'Prosciutto Sandwich': {'ingredients': 'Prosciutto, Fresh Mozzarella, Balsamic glaze, Mayonnaise', 'price': 8.25},
    'Chicken Sandwich': {'ingredients': 'Chicken Cutlet, Mozzarella Cheese, Marinara Sauce, Mayonnaise', 'price': 8.25},
    'Caprese Sandwich': {'ingredients': 'Fresh Mozzarella, Tomatoes, Basil Leaves, Olive Oil', 'price': 8.25},
    'Ham & Cheese Sandwich': {'ingredients': 'Ham, Provolone Cheese, Lettuce, Tomatoes, Olive Oil', 'price': 8.25}
}

add_ons = ['Lettuce', 'Tomatoes', 'Onions', 'Peppers', 'Provolone Cheese', 'American Cheese', 'Swiss Cheese', 'Mozzarella Cheese']

# Create your views here.
def main(request):
    '''Fund to respond to the "main" request. Acts as the main page with basic information about the restaurant'''

    template_name = "restaurant/main.html"

    context = {
        'images' : resturant_images
    }

    return render(request, template_name, context)

def order(request):
    '''Fund to respond to the "show_all" request. Shows display an online order form'''
    
    template_name = "restaurant/order.html"

    # Simulated day by randomly picking a sandwhic
    all_special = list(special_menu.keys()) #creating a list of all sandwich names in special menu
    daily_special = random.choice(all_special) # randomly choosing one name 
    daily_special_detail = special_menu[daily_special] #getting corresponding sandwhich details

    context = {
        'daily_special': daily_special,
        'daily_special_detail': daily_special_detail,
        'menu': menu,
        'add_ons': add_ons
    }


    return render(request, template_name, context)

def confirmation(request):
    '''Fund to respond to the "confirmation" request. Confirms order'''

    #check if POST data was sent with the HTTP POST message:
    if request.POST:

        #Extracting the order details into variable
        name = request.POST['name']      
        phone = request.POST['phone']
        email = request.POST['email']
        instructions = request.POST['instructions']

        #get list because the person ordering might not have select these fields
        #in which case we get an empty list
        ordered_special = request.POST.getlist('order_special')
        addons = request.POST.getlist('addons')
        ordered_sandwhiches = request.POST.getlist('order_items') 
        
        #calculating total and getting the menu order detial in one coheisve list
        total = 0
        order = []
        for sandwich in ordered_sandwhiches:
            price = menu[sandwich]['price']
            full_detail = {'name': sandwich, 'price':price}
            order.append(full_detail)
            total += price

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'instructions': instructions,
            'ordered_special': '',
            'ordered_special_detail': '',
            'addons':[],
            'ordered_sandwhiches': order,
            'menu': menu,
            'total': total
        }

        # if the special menue sandwhich is picked, then only do we need to add its fields 
        # which incudes the add ons, and updating the price accordingly
        if len(ordered_special) > 0:
            special_sandwhich = ordered_special[0]
            context['ordered_special'] = special_sandwhich
            context['ordered_special_detail'] = special_menu[special_sandwhich]
            context['addons'] = addons
            total += special_menu[special_sandwhich]['price']
            context['total'] = total

        
    template_name = "restaurant/confirmation.html"

    return render (request, template_name, context=context)
