from django.db import models
#
from membres.models import Emprunteur

# Create your models here.
## exo 1
class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()



class Livre(models.Model):
    titre = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    nombre_pages = models.PositiveIntegerField()



## retirer cette classe pour la mettre dans "membre" pour l'exo 6
#class Emprunteur(models.Model):
 #   nom = models.CharField(max_length=100)
  #  email = models.EmailField()
   # livres = models.ManyToManyField(Livre, through="Emprunt", related_name="emprunteurs")


class Emprunt(models.Model):
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateField()
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(blank=True, null=True)  

    
