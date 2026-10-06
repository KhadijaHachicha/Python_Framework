from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator , RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


#validators
def validate_email(value):
    if not value:
        raise ValidationError("l'adresse mail est obligatoire")
    if not value.endswith("@gmail.com"):
        raise ValidationError("le domaine accepté est gmail")
matricule_fiscale_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message = "format erroné"



)


# Create your models here.
class Utilisateur(AbstractUser):
    user_id = models.CharField(primary_key=True, max_length=8)
    email = models.EmailField(unique=True , validators=[validate_email])
    telephone = models.CharField(max_length=15 , blank=True, null=True)
    role = models.CharField(max_length=20 , choices=[
        ('admin', 'Admin '),
        ('c', 'Chargeur'),
        ('t', 'Transporteur')

    ] , default ='c')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_user_id(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"{annee}user"
        dernier = (
                cls.objects.filter(user_id__startswith=prefixe)
                .order_by('-user_id')
                .first()
            )
        compteur = int(dernier.user_id[-2:]) + 1 if dernier else 0
        if compteur > 99:
            raise ValidationError("La limite de 99 utilisateurs pour cette année a été atteinte.")
            
        return f"{prefixe}{compteur:02d}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        super().save(*args, **kwargs)
        
            
    def __str__(self):
        return f"{self.user_id} - {self.username}"
        





class Entreprise(models.Model):
    raison_social = models.CharField(max_length=200, blank=False , null=False) #blank au niveau formulaire (required), null fel BD
    matricule_fiscale = models.CharField(max_length=17 , unique=True,validators=[matricule_fiscale_validator])
    adresse = models.TextField(validators= [
        MinLengthValidator(20, "l'adresse ne peut avoir moins de 20 char "),
        MaxLengthValidator(400,"l'adresse ne peut pas depasser les 400 char" )
    
    ])
    type_entreprise = models.CharField(max_length=100, choices = [
        ('c', 'Chargeur '),
        ('t', 'Transporteur')
    ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE , related_name='entreprise')