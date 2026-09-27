from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
import json

from .models import *
# Create your views here.

class ListeLivres(View):
    #this is the method called in the urls.py

    def get(self, request, *args, **kwargs):
        #step 1: get all the books
        livres = Livre.objects.all()

        html = ""
        for index,livre in  enumerate(livres):

            url = reverse("detail_livre",args=(livre.isbn,)) # this is used to return back the prefix url for that particular urlname
            html += f"{index+1}. <a href ={url}>{livre.__str__()}</a> <br>"

        return HttpResponse(html)

def detail_livre(request,isbn):
   livre = Livre.objects.get(isbn=isbn) # we need to add a try and catch here
   # get can only be used on a unique attribute and it produces an error when it doesnot exist and when more than one values are been returned
   # filter returns a list(queryset) but does not generate an error and rather returns an empty list
   if livre is None:
       return Http404(f"Book with isbn {isbn} not found")
   html = f""" <h2>{livre.titre}</h2> 
   <p>ISBN : {livre.isbn}</p> 
   <p>Auteur : {livre.auteur}</p> 
   <p>Pages : {livre.nombre_pages}</p> """

   return HttpResponse(html)

def ajouter_livre(request):
    if request.method == "GET":
        return HttpResponse("<p>You just performed a GET method</p>")
    if request.method == "POST":
        return HttpResponse("<p>You just performed a POST method</p>")

    return HttpResponse(f"<p>Unexpected method {request.method} </p>")

def livre_json(request):
    livres = Livre.objects.all()
    books = []
    for livre in livres:
        book = { "isbn": livre.isbn, "title":livre.titre}
        books.append(book)
    row_json = json.dumps(books) # another method to convert the list to json and then return it in the HttpResponse
    return JsonResponse(books, safe=False)
# safe = false because we want to tell django that we are intentionally returning a list