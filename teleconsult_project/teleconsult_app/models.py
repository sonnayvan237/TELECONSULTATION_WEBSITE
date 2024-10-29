from django.db import models

# Create your models here.
class Medecins(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')  # Fournir une valeur par défaut
    photo = models.ImageField(upload_to='images/')

class Exams(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    photo = models.ImageField(upload_to='images/')