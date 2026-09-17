from django.db import models

# Create your models here.
class Auteur(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    date_naissance = models.DateField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Genre(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return f"Genre : {self.nom}"

    class Meta:
        verbose_name_plural = "genres" # this will be displayed by django admin

class Livre(models.Model):
    LANGS = {
        "EN":"English",
        "FR":"French",
        "KO":"Korean"
    }
    titre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=10, primary_key=True)
    nombre_pages = models.IntegerField()
    resume = models.TextField(blank=True) # to make it optional,
    langue = models.CharField(max_length=2, choices=LANGS)
    date_publication = models.DateField(blank=True, null=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.SET_NULL,null=True)
    genre = models.ManyToManyField(Genre)

    class Meta:
        ordering = ['titre'] # to sort by title by default whenever we query it

    def __str__(self):
        return f" {self.titre} ({self.isbn}) par {self.auteur}"

    @property
    def est_disponible(self):
        emprunts = Emprunt.objects.filter(livre=self,date_retour_effective=None)
        return not emprunts.exists()

    def save(self, **kwargs):
        self.titre = self.titre.title() # the .title() capitalises all the first letters of the word of a sentence
        super().save(**kwargs)







# class Emprunteur(models.Model):
#     nom = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     livres = models.ManyToManyField(Livre, through="Emprunt")
#     # added it here bc its more interesting to see the list of the books he has borrowed
#
#     def __str__(self):
#         return f"{self.nom}({self.email})"

class Emprunt(models.Model):
    emprunteur = models.ForeignKey("membres.Emprunteur",on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateField()
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(blank=True,null=True)

    def __str__(self):
        return f"{self.emprunteur} - {self.livre} le {self.date_emprunt}"

class FicheAuteur(models.Model):
    biographie = models.TextField()
    site_web = models.CharField(max_length=100)
    auteur = models.OneToOneField(Auteur,on_delete=models.CASCADE)

    def __str__(self):
        return f"fiche de {self.auteur}"

# the reason why we create this lies in the question , the relationship is optional
# so its like additional information that an author might have but is not forced to
# this is usually useful when there are many optional informations to keep it clean



# Null is at the database level while Blank is at the entry level it permits you to leave the field as it is
# i chose to put null and blank to true for the publication date because at the admin level ,
# we can leave it out while filling it but at the db level it should be null where as the summary
# should not be null at the db level but rather an empty string
def capitalize_sentence(sentence):
    words = sentence.split()
    words = [word.capitalize() for word in words]
    return " ".join(words)