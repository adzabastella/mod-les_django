import time
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import MiddlewareNotUsed


class LogRequeteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # exo21 (print au tout debut et a la toute fin de chaque middleware)
        print("LogRequete avant :", request.method, request.path)
        response = self.get_response(request)
        print("LogRequete apres")
        return response


# Exercice 23 
class TempsMiddleware:
    def __init__(self, get_response):
        if not hasattr(settings, "MESURE_TEMPS_ACTIVE"):
            raise MiddlewareNotUsed("mesure du temps desactivee")
        self.get_response = get_response
    def __call__(self, request):
        # exo21 (print au tout debut et a la toute fin de chaque middleware)
        print("Temps avant")
        debut = time.time()
        response = self.get_response(request)
        fin = time.time()
        duree = (fin - debut) * 1000
        print("temps de traitement :", duree, "ms")
        return response


class AutorisationLivresMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/bibliotheque/livres/":
            if "X-Client-Autorise" not in request.headers:
                return HttpResponse("acces refuse", status=403)

        response = self.get_response(request)
        return response


# Exercice 25
class TokenGenreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/bibliotheque/livres-par-genre/"):
            token = request.headers.get("X-Token")
            if token != "secret123":
                return HttpResponse("non autorise", status=403)
        response = self.get_response(request)
        return response
