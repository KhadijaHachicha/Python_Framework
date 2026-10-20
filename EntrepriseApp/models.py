from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


#validators
def validate_email(value):
    if not value:
        raise ValidationError("l'adresse email est obligatoire")
    if not value.endswith("@gmail.com"):
        raise ValidationError("le domaine accepté est gmail")


# Create your models here.
class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True , validators=[validate_email])
    user_id = models.CharField(primary_key=True, max_length=8, unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('c', 'chargeur'),
        ('t', 'transporteur')
    ], default='c')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_user_id(cls):
        year_code = str(timezone.now().year)[-2:]
        prefix = f"{year_code}user"

        last_user = cls.objects.filter(user_id__startswith=prefix).order_by('-user_id').first()

        if last_user:
            try:
                last_sequence = int(last_user.user_id[-2:])
            except (TypeError, ValueError):
                last_sequence = 0
            sequence = last_sequence + 1
        else:
            sequence = 1

        if sequence > 99:
            sequence = 1

        return f"{prefix}{sequence:02d}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        super().save(*args, **kwargs)

matricule_fiscal_validator= RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message=""
)


class Entreprise(models.Model):
    raison_social = models.CharField(max_length=200, blank=False ,null=False)
    matricule_fiscal =models.CharField(max_length=17 ,unique=True, validators=[matricule_fiscal_validator])
    adresse = models.TextField(validators=[MinLengthValidator(20,"l'adresse ne peut pas avoir moins de 20 char"),MaxLengthValidator(400,"l'adresse ne peut pas depasser les 400 char")])
    type_entreprise=models.CharField(max_length=100,choices=[('c','chargeur'),
    ('t','transporteur')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    gerant= models.OneToOneField(Utilisateur ,on_delete=models.CASCADE,related_name='entreprise')