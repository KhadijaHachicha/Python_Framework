from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Validators
def validate_email(value):
    if not value:
        raise ValidationError("L'adresse e-mail est obligatoire.")
    if not value.endswith('@gmail.com'):
        raise ValidationError("Format d'adresse e-mail invalide.")

matricule_fiscal_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message="Format attendu : 7 chiffres, 1 lettre (clé de contrôle), "
            "1 lettre (A/B/D/N/P), 1 lettre (M/P/C/N/E), 3 chiffres "
            "(ex. 1234567AAM000 ou 1234567-A-A-M-000)."
)

class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, editable=False)
    email = models.EmailField(unique=True, validators=[validate_email])
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
        ('administrateur', 'Administrateur')
    ], default='chargeur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_user_id(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"{annee}user"
        dernier = (
            cls.objects
            .filter(user_id__startswith=prefixe)
            .order_by('-user_id')
            .first()
        )
        compteur = int(dernier.user_id[-2:]) + 1 if dernier else 0
        if compteur > 99:
            raise ValueError(f"Limite de 100 utilisateurs atteinte pour l'année 20{annee}.")
        return f"{prefixe}{compteur:02d}"

    def __str__(self):
        return f"{self.user_id} - {self.username}"


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200, blank=False, null=False)
    matricule_fiscal = models.CharField(
        max_length=17,
        unique=True,
        validators=[matricule_fiscal_validator]
    )
    adresse = models.TextField(validators=[
        MinLengthValidator(20, "L'adresse ne peut avoir moins de 20 caractères."),
        MaxLengthValidator(400, "L'adresse ne peut pas dépasser 400 caractères.")
    ])
    type_entreprise = models.CharField(max_length=20, choices=[
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='entreprise'
    )

    def __str__(self):
        return f"{self.raison_sociale} - {self.matricule_fiscal}"