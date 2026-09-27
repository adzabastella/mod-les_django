from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView # exo13 et exo17 (import des vues generiques)

from .models import *
# Create your views here.

# exo12 (liste_livres ecrite en CBV avec View et la methode get)
# à partir de l'exo13 l'url livres/ ne pointe plus ici mais vers LivreListView en dessous
class ListeLivres(View):
    #this is the method called in the urls.py

    def get(self, request, *args, **kwargs):
        #step 1: get all the books
        livres = Livre.objects.all()

        html = ""
        count =0
        for livre in livres:
            count +=1
            url = reverse("detail_livre",args=(livre.isbn,)) # this is used to return back the prefix url for that particular urlname
            html += f"{count}.<a href ={url}>{livre.__str__()}</a> <br>"

        return HttpResponse(html)


# exo13 (ajout d'une vraie ListView sur le modele Livre) django va chercher le template bibliotheque/livre_list.html tout seul
class LivreListView(ListView):
    model = Livre
    context_object_name = "livres" # exo14 (au lieu de object_list qui est pas parlant)
    ordering = ["titre"] # exo14 (tri par titre sans toucher au modele)

    # exo22 (on met un print dans la vue pour etre sur que le middleware renvoie bien
    # son 403 sans jamais passer par ici)
    def get(self, request, *args, **kwargs):
        print("la vue liste des livres a bien ete executee")
        return super().get(request, *args, **kwargs)

    # exo25 (on donne les genres au template pour pouvoir faire le lien vers la page
    # livres-par-genre avec url et pas en dur)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        return context


# exo15 (vue generique qui liste seulement les livres du genre demande dans l'url)
# Elle est reutilise pour la synthese de l'exercice 25
class LivresParGenre(ListView):
    template_name = "bibliotheque/livres_genre.html"
    context_object_name = "livres"

    def get_queryset(self):
        nom = self.kwargs["nom"] # le nom du genre recupere dans l'url
        return Livre.objects.filter(genre__nom=nom).order_by("titre")

    # exo16 (ajout du nombre total de livres du genre dans le contexte)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nom_genre"] = self.kwargs["nom"]
        context["nombre_livres"] = self.get_queryset().count()
        return context


# exo17 (detail_livre refait avec DetailView)
# isbn est la cle primaire du modele donc on dit juste a django que le pk s'appelle isbn dans l'url
class LivreDetailView(DetailView):
    model = Livre
    pk_url_kwarg = "isbn"
    context_object_name = "livre"


# avant il y avait :
#     livre = Livre.objects.get(isbn=isbn)
#     if livre is None:
#         return Http404(...)

def detail_livre(request,isbn):
   # exo8 (correction : .get() leve DoesNotExist au lieu de renvoyer None, ca faisait une erreur 500)
   try:
       livre = Livre.objects.get(isbn=isbn)
   except Livre.DoesNotExist:
       raise Http404(f"Book with isbn {isbn} not found") # raise et pas return sinon django affiche pas la page 404
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

# exo11 on teste la methode de la requete et non request.POST
# la version de l'enonce qui fait if request.POST ne marche pas car un QueryDict
# vide est "faux" en python (l'explication complete est dans urls.py)
def ajouter_commentaire(request):
    if request.method == "POST":
        return HttpResponse("Commentaire ajoute")

    return HttpResponse("Formulaire vide")

def livre_json(request):
    livres = Livre.objects.all()
    books = []
    for livre in livres:
        book = { "isbn": livre.isbn, "title":livre.titre}
        books.append(book)
    return JsonResponse(books, safe=False)
# safe = false because we want to tell django that we are intentionally returning a list


# exo13 
# le template que django cherche c'est bibliotheque/livre_list.html
# "bibliotheque" c'est le nom de l'app (app_label) ou se trouve le modele Livre
# "livre_list" c'est le nom du modele en minuscule + le suffixe "_list" de ListView
# (pour DetailView c'est pareil mais avec "_detail" donc bibliotheque/livre_detail.html)

# exo17 
# avec la fonction c'etait a moi de gerer le livre introuvable (try/except + Http404),
# avec DetailView c'est django qui s'en charge, get_object() leve Http404 tout seul si l'isbn existe pas

# exo18 
# je prefere une vue fonction quand la logique est specifique et ne ressemble a aucune vue generique,
# par exemple ajouter_livre qui fait juste une chose differente selon GET ou POST, ou livre_json
# qui construit un dict a la main. En fonction on voit tout le code d'un coup, c'est plus simple a lire et a deboguer.
# je prefere une vue generique quand on fait un truc classique (lister, afficher un detail) sur un modele,
# par exemple la liste des livres ou le detail d'un livre : avec ListView/DetailView on ecrit 3 lignes,
# le 404, la pagination, le contexte sont deja geres donc c'est plus rapide a mettre en place.
# Et si on a juste besoin de changer une petite partie (filtrer par genre) on redefinit seulement get_queryset.
# Par contre si on doit redefinir presque toutes les methodes, la CBV devient plus compliquee qu'une simple fonction.
