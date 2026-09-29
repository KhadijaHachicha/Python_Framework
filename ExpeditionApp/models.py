from django.db import models
from EntrepriseApp.models import Entreprise

# Create your models here.


class Expedition(models.Model):
    Reference = models.CharField(max_length=200 ,unique=True)
    ville_depart = models.CharField(max_length=100 )
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10 , decimal_places=2)
    date_souhaitee = models.DateTimeField()
    description = models.TextField()
    statue = models.CharField(max_length=100 , choices=[
        ('en_attente' , 'en_attente'),
        ('t' , 'terminee'),
        ('a', 'annulee')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='entreprise', blank =True, null=True )

