from django.db import models
from django.core.validators import     MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.
class expedition(models.Model):
    entreprise = models.ForeignKey('EntrepriseApp.Enterprise',on_delete=models.CASCADE,related_name='expeditions')
    reference = models.CharField(max_length=20,unique=True,auto_created=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.FloatField(validators=[
        MinValueValidator(1,"Le poids ne peut pas etre negative")
    ])
    date_souhaitee = models.DateTimeField()
    description = models.TextField()
    status = models.CharField(max_length=20,choices=[
        ('p','publiee'),
        ('a','attribuee'),
        ('ec','en_cours'),
        ('l','livree'),
        ('an','annulee')
    ],default='publiee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def clean(self):
        super().clean() #S'il y a une validataion de deux valeurs ou plus on doit appeler la methode clean de la classe parent
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError(({
                'entreprise : une expedition ne peut etre cree que par un chargeur'
            }))
    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime("%y")
        prefix = f"EXP_{annee}"
        dernier = (
            cls.objects.filter(reference_startswith=prefix) # Note 1 : <==>  SELECT * FROM expedition
            .order_by("-reference") # Note 2 using - it will order by reference desc
            .first()
        )
        compteur = int(dernier.reference[-5:]) + 1 if dernier else 1
        if compteur > 99999:
            raise ValueError("Limit Exceed")
        return f"{prefix}{compteur:05d}"
    def save(self,*args,**kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        self.full_clean()  # fonction pour valiser tous les validateurs
        super().save(*args,**kwargs)