from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator 
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.


class Expedition(models.Model):
    Reference = models.CharField(max_length=200 ,unique=True)
    ville_depart = models.CharField(max_length=100 )
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10 , decimal_places=2, validators=[MinValueValidator(1, "Le poids doit être strictement supérieure à 0.")])
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

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError ({
                'entreprise':'une expedition ne peut etre crée que par un chargeur '
            })


    @classmethod   
    def _generate_reference(cls):
        annee = timezone.now().strtime('%y')
        prefixe = f"EXP_{annee}"
        dernier = (
            cls.objectifs.filtrer(refernce_startswich=prefixe).ordre_by('-reference').last()
        )
        compteur= (
            int (dernier.reference[-5:])+1 if dernier 
            else 1       
        )
        if compteur > 99999:
            raise ValidationError("limit exceeded ")
        return f"{prefixe}{compteur:05d}"

    def save(self ,*args , **kwargs):
        if not self.reference:
            self.reference =self._generate_reference()



        self.full_clean()
        super().save(*args, **kwargs)
    

