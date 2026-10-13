from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
# Create your models here.
class vehicules(models.Model):
    immatriculation = models.CharField(max_length=20,unique=True)
    capacite_kg = models.PositiveIntegerField(validators=[
        MinValueValidator(1,"La capacite ne peut pas etre negative"),
    ])
    entreprise = models.ForeignKey('EntrepriseApp.Enterprise',on_delete=models.CASCADE,related_name='vehicules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disponible = models.BooleanField(default=True)
    type_vehicule = models.CharField(max_length=20,choices=[])
    def clean(self):
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError(({
                'entreprise : un vehicule ne peut etre cree que par un transporteur'
            }))

        if self.vehicule_id and self.statut == 'proposee':
            if not self.vehicule.disponible:
                raise ValidationError({
                    'vehicule': "Ce véhicule n'est pas disponible."
                })

        if self.vehicule_id and self.expedition_id:
            capacites = {
                'camionnette': 1.5,
                'fourgon': 3.5,
                'camion_porteur': 19,
                'semi_remorque': 26,
            }

            type_vehicule = self.vehicule.type_vehicule
            poids = self.expedition.poids

            capacite_max = capacites.get(type_vehicule)

            if capacite_max is None:
                raise ValidationError({
                    'vehicule': "Le type de véhicule est inconnu."
                })

            if poids is None or poids <= 0:
                raise ValidationError({
                    'expedition': "Le poids doit être strictement positif."
                })

            if poids > capacite_max:
                raise ValidationError({
                    'vehicule': (
                        f"Le véhicule de type '{type_vehicule}' "
                        f"ne peut pas transporter {poids} tonnes. "
                        f"Capacité maximale indicative : "
                        f"{capacite_max} tonnes."
                    )
                })
            