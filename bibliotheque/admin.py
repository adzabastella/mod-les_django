from django.contrib import admin
from .models import Auteur, Livre, Genre, FicheAuteur, Emprunt

# Register your models here.
admin.site.register(Auteur)
admin.site.register(Livre)
admin.site.register(Genre)
admin.site.register(FicheAuteur)
admin.site.register(Emprunt)