from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

# Create your models here.
class Medecins(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')  # Fournir une valeur par défaut
    photo = models.ImageField(upload_to='images/')
    age = models.IntegerField(default=1)
    

class Exams(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    photo = models.ImageField(upload_to='images/')
    deplacement = models.IntegerField(blank=True, default=0)
    total = models.IntegerField(default=0)
        
class Patients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Relation avec le modèle User
    nom_prenom = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    telephone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nom_prenom
    

class Rendezvous(models.Model):
    medecin = models.ForeignKey(Medecins, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, null=True) 
    jour = models.CharField(max_length=10, choices=[
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
    ])
    heure = models.TimeField()

class Ordonnances(models.Model):
    fichier = models.FileField(upload_to='ordonnances/')
    commentaire = models.TextField(null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username