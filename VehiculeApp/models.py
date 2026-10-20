from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

CAPACITES_VEHICULE = {
    'camionnette': (1, 1500),
    'fourgon': (1, 3500),
    'camion_porteur': (3500, 19000),
    'semi_remorque': (19000, 26000),
}


# Create your models here.
class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=50, unique=True)
    type_vehicule = models.CharField(
        max_length=100,
        choices=[
            ('camionnette', 'Camionnette / utilitaire léger'),
            ('camion_porteur', 'Camion porteur'),
            ('semi_remorque', 'Semi-remorque'),
            ('fourgon', 'Fourgon'),
        ],
    )
    capacite_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "la valeur doit etre strictement possitive")]
    )
    disponible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='vehicules')

    def clean(self):
        super().clean()
        if self.type_vehicule in CAPACITES_VEHICULE and self.capacite_kg is not None:
            minimum, maximum = CAPACITES_VEHICULE[self.type_vehicule]
            if not minimum <= self.capacite_kg <= maximum:
                raise ValidationError({
                    'capacite_kg': f"La capacite doit etre entre {minimum} et {maximum} kg pour ce type de vehicule."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)