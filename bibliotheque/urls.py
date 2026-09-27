
from django.urls import path, register_converter
from . import views


class ISBNConverter:
    regex = "BOOK[0-9]{3}" # to match what i have
    # regex = "[0-9]{3}-[0-9]-[0-9]{4}-[0-9]{4}-[0-9]" # corresponding to the isbn-13 format stated by the lecturer

    def to_python(self, value):
        return value # returns the value in the datatype format expected by the view

    def to_url(self, value):
        return value

# registering the converter
register_converter(ISBNConverter,"isbn")
urlpatterns = [
    path('livres/', views.ListeLivres.as_view(), name="liste_livres"),# when someone reaches this route /livres we execute this function in the views.py
    path('livres/json', views.livre_json, name="livre_json"),# when someone reaches this route /livres we execute this function in the views.py
    path('livres/add', views.ajouter_livre, name="ajouter_livre"),# when someone reaches this route /livres we execute this function in the views.py
    path('ouvrage/<isbn:isbn>', views.detail_livre,  name="detail_livre") # to get details on a particular book
]

# Exercise 3
# the page livres/nouveautes will never display what we want it will always enter the first condition so it will instead assume that  we want to view a book with isbn "nouveautes"
# to solve this problem we weill have rather change the other of the paths put the /nouveates before the other

#Exercise 6
# we had to do research on converters
# Now converters are used to make sure that the url regex matches a particular pattern rather than django's built in str, int etc
# so we have to create an isbn converter to make sure the isn matches our regex

#A converter is a class that includes the following
# a regex class attribute
# a to_python(self,value) for converting the matched string into a type that will be used in the view function
# a to_url(self,value) for converting the python type into string to add to the url

