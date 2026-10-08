from rest_framework import serializers
from .models import *

class LivreSerializer(serializers.Serializer):
    # titre = serializers.CharField(max_length=200)
    # isbn = serializers.CharField(max_length=13)
    # nombre_pages = serializers.IntegerField()

    class Meta:
        model = Livre
        fields = ["id", "titre", "isbn", "nombre_pages"]

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must contain 13 characters")
        return value



class EmpruntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprunt
        fields = ["id", "livre", "emprunteur", "date_emprunt", "date_retour_prevue"]

    def validate(self, data):
        if data["date_retour_prevue"] < data["date_emprunt"]:
            raise serializers.ValidationError("The return date must be after the borrowed date")
        return data

class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = ["id", "nom", "livres"]

class AuteurHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    #the hyper link needs the request so that it gets the url
    class Meta:
        model = Auteur
        fields = ["url", "nom", "livres"]

# Exercise 3: it does not work because we always have to call the /is_valid() before the save

# Exercise 7
#model serializer is when the object is tied to a model , also no need to write all the fields in a model serializer
# model serializer has default model creation/update behaviour

# Exercise 14:
# the N+1 problem is a case where we have a relation ship so we make one query to get the object that has the foreign key attached to it
# then we make another query to get the properties of the foreign key
# e.g we get all books with their authors then each author's name
# to solve it we fix it at the query set level usually with select_related() in the get_query_set