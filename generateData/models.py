from django.db import models

class TypeDonnees(models.Model):
    libelle     = models.CharField(max_length=25)
    description = models.CharField(max_length=100)

    #définition des champs visibles au niveau de la page d'administration
    def __str__(self):
    	return self.libelle

class ExempleTypeDonnees(models.Model):
    typedonnees = models.ForeignKey(TypeDonnees)
    short_code = models.CharField(max_length=50)
    libelle    = models.CharField(max_length=50)

    #définition des champs visibles au niveau de la page d'administration
    def __str__(self):
    	return self.short_code

class Pays(models.Model):
    code      = models.PositiveSmallIntegerField(default=1)
    alpha2    = models.CharField(max_length=2, unique=True)
    alpha3    = models.CharField(max_length=2, unique=True)
    nom_en_gb = models.CharField(max_length=45)
    nom_fr_fr = models.CharField(max_length=45)

    #définition des champs visibles au niveau de la page d'administration
    def __str__(self):
    	return self.nom_fr_fr

class Noms(models.Model):
    libelle    = models.CharField(max_length=25)
    sexe       = models.CharField(max_length=1)
    pays       = models.ForeignKey(Pays)

    #définition des champs visibles au niveau de la page d'administration
    def __str__(self):
    	return self.libelle

class Prenoms(models.Model):
    libelle    = models.CharField(max_length=25)
    sexe       = models.CharField(max_length=1)
    pays       = models.ForeignKey(Pays)

    #définition des champs visibles au niveau de la page d'administration
    def __str__(self):
    	return self.libelle