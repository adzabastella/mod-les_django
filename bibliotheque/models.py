from django.db import models

from membres.models import Emprunteur


class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Genre(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
    
class Livre(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    titre = models.CharField(max_length=255)
    nombre_pages = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, blank=True, related_name="livres")

    LANGUES = [
        ("fr", "Français"),
        ("en", "Anglais"),
        ("es", "Espagnol"),
    ]

    resume = models.TextField(blank=True)
    langue = models.CharField(max_length=2, choices=LANGUES, blank=True)
    date_publication = models.DateField(blank=True, null=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name="livres")

    def __str__(self):
        return self.titre


class Emprunt(models.Model):
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateField()
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.emprunteur} → {self.livre}"

