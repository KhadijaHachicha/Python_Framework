from django.db import models
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition

# Create your models here.
class Offre(models.Model):
    prix=models.DecimalField(max_digits=10,decimal_places=3)
    delai_jours=models.PositiveBigIntegerField()
    statut=models.CharField(max_length=100,choices=[
        ('p','propose'), 
        ('a','accepte'),
        ('r','refuse'),
        ('re','retiree') 
        ],default='p')
    date_proposition=models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE,related_name='offres')
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE,related_name='offres')
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE,related_name='offres')



    