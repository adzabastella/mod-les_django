from django.db import models
from bibliotheque.models import Livre

# Create your models here.
class Emprunteur(models.Model):
    nom = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    livres = models.ManyToManyField(Livre, through="bibliotheque.Emprunt")
    # added it here bc its more interesting to see the list of the books he has borrowed

    def __str__(self):
        return f"{self.nom}({self.email})"