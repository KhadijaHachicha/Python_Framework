from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Expedition(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    ville_depart = models.CharField(max_length=80)
    ville_arrive = models.CharField(max_length=80)
    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, "le poids doit etre possitive")],
    )
    date_souhaitee = models.DateTimeField()
    description = models.TextField()
    statut = models.CharField(
        max_length=100,
        choices=[
            ('en_attente', 'En attente'),
            ('publiee', 'Publiée'),
            ('attribuee', 'Attribuée'),
            ('terminee', 'Terminée'),
            ('annulee', 'Annulée'),
        ],
        default='en_attente',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='expeditions')

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'c':
            raise ValidationError({"entreprise": "une expedition ne peut pas etre cree que par un chargeur"})

    @classmethod
    def _generate_reference(cls):
        anne = timezone.now().strftime('%y')
        prefix = f"EXP_{anne}_"
        dernier = (
            cls.objects.filter(reference__startswith=prefix)
            .order_by('reference')
            .last()
        )
        compteur = int(dernier.reference[-5:]) + 1 if dernier else 1
        if compteur > 99999:
            raise ValueError("Le compteur a dépassé la limite de 5 chiffres.")
        return f"{prefix}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        self.full_clean()
        super().save(*args, **kwargs)