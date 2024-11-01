from django.db import models
from django.core.validators import MinLengthValidator

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
    deplacement = models.IntegerField(blank=True)
    total = models.IntegerField(default=0)
    
class RendezVous(models.Model):
    medecin = models.ForeignKey(Medecins, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10, choices=[
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
    ])
    heure = models.TimeField()

class Patients(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    date_de_naissance = models.DateField(null=True, blank=True)
    telephone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(default='example@example.com')
    password = models.CharField(
        max_length=100, 
        validators=[MinLengthValidator(8)]
    )
    is_active = models.BooleanField(default=False)  # Nouveau champ
    # Ajoutez cette option pour afficher les emails plus lisiblement en cas d’erreurs
    def __str__(self):
        return self.email
