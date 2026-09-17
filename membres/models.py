# Create your models here.
from django.db import models


class Emprunteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()