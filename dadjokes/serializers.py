# file: dadjokes/serializers.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: converts django data models to a text-representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''
        A serializer for the Joke model. Specify which model/fields to send in the API
    '''

    class Meta: 
        model = Joke
        fields  =['text', 'name', 'timestamp'] 

    
    # add methods to customze the Create/Read/Update/Delete operations
    def create(self, validated_data):
    #     '''Override teh superclass method that handles object creation.'''

    #     print(f'JokeSerializer.create,validated_data={validated_data}')
    #     #crate a Joke object
    #     joke = Joke(**validated_data)

    #     # if there was a user (foreing key), the attach a PK for the Joke (but not needed because there is no object)
    #     joke.user = Joke.objects.first()

    #     #save the object to the database
    #     joke.save

    #     return joke
    
        # a simplified way:
        # attach a FK for the Joke
        #validated_data[''] = Joke.objects.first()
        #do create and save all at once: 
        return Joke.objects.create(**validated_data)


class PictureSerializer(serializers.ModelSerializer):
    '''
        A serializer for the Picture model. Specify which model/fields to send in the API
    '''

    class Meta: 
        model = Picture
        fields  =['image_url', 'name', 'timestamp'] 

    
    # add methods to customze the Create/Read/Update/Delete operations
    def create(self, validated_data):
    #     '''Override teh superclass method that handles object creation.'''

    #     print(f'JokeSerializer.create,validated_data={validated_data}')
    #     #crate a Joke object
    #     joke = Joke(**validated_data)

    #     # if there was a user (foreing key), the attach a PK for the Joke (but not needed because there is no object)
    #     joke.user = Joke.objects.first()

    #     #save the object to the database
    #     joke.save

    #     return joke
    
        # a simplified way:
        # attach a FK for the Joke
        #validated_data[''] = Joke.objects.first()
        #do create and save all at once: 
        return Picture.objects.create(**validated_data)




