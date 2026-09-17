from django.contrib import admin

# Register your models here.
from .models import Auteur, Livre

admin.site.register(Auteur)
admin.site.register(Livre)

from .models import Auteur, Livre, Emprunteur, Emprunt
# pour l'exo 1 laiser emprunteur
# admin.site.register(Emprunteur)
admin.site.register(Emprunt)

# exo 5
from .models import Auteur, Livre, Genre, Emprunt
admin.site.register(Genre)