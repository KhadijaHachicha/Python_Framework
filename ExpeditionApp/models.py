from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from EntrepriseApp.models import Entreprise


class Expedition(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1, "Le poids doit être supérieur ou égal à 1 kg.")]
    )
    date_souhaitee = models.DateTimeField()
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions',
        blank=True,
        null=True
    )

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({
                'entreprise': "Une expédition ne peut être créée que par un chargeur."
            })

    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"EXP_{annee}"
        dernier = (
            cls.objects
            .filter(reference__startswith=prefixe)
            .order_by('-reference')
            .first()
        )
        compteur = int(dernier.reference[-5:]) + 1 if dernier else 1
        if compteur > 99999:
            raise ValidationError("Limite de 99999 expéditions atteinte pour cette année.")
        return f"{prefixe}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.ville_depart} → {self.ville_arrivee} ({self.statut})"