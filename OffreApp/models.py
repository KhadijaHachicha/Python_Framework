from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from ExpeditionApp import Expedition
# Create your models here.
class offre(models.Model):
    prix = models.FloatField(validators=[MinValueValidator(1,"Le prix ne peut pas etre negative")])
    delais_jour = models.IntegerField(blank=False,null=False,validators=[MinValueValidator(1,"Le delais ne peut pas etre negative")])
    status = models.CharField(max_length=20,choices=[
        ('p','proposee'), 
        ('a','acceptee'),
        ('r','refusee'),
        ('re','retiree'),
        
    ],default='p')
    date_proposition = models.DateTimeField(auto_now_add=True)
    expedition = models.ForeignKey('ExpidationApp.expedition',on_delete=models.CASCADE,related_name='offres')
    transporteur = models.ForeignKey('EntrepriseApp.Enterprise',on_delete=models.CASCADE,related_name='offres')
    vehicule = models.ForeignKey('VehiculesApp.vehicules',on_delete=models.CASCADE,related_name='offres')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def clean(self):
        if self.transporteur and self.transporteur.type_entreprise == 'transporteur':
            raise ValidationError(({
                'transporteur : une offre ne peut etre faite que par un transporteur'
            }))
        if self.vehicule and self.vehicule.entreprise_id != self.transporteur:
            raise ValidationError(({
                " Le véhicule associé à une offre doit appartenir à la même entreprise que le transporteur de l'offre."
            }))
        if self.expedition and self.expedition.status != "p" :
            raise ValidationError(({
                " Une expédition ne peut recevoir de nouvelles offres que si son statut est publiee. "
            }))
        if self.transporteur and self.expedition and self.status == "proposee" :
            expedition_exisite = offre.objects.filter(transporteur=self.transporteur, expedition=self.expedition,status="proposee")
            if self.pk:
                offres_existantes = offres_existantes.exclude(
                    pk=self.pk
                )
        if offres_existantes.exists():
            raise ValidationError({
                'entreprise': (
                    "Cette entreprise possède déjà une offre "
                    "proposée pour cette expédition."
                )
            })
        if self.vehicule_id and self.statut == 'proposee':
            if not self.vehicule.disponible:
                raise ValidationError({
                    'vehicule': (
                        "Ce véhicule n'est pas disponible "
                        "pour une nouvelle offre."
                    )
                })
    def save(self, *args, **kwargs):
        with transaction.atomic():
            ancienne_offre = None

            if self.pk:
                ancienne_offre = (
                    offre.objects
                    .select_for_update()
                    .filter(pk=self.pk)
                    .first()
                )

            devient_acceptee = (
                self.statut == 'acceptee'
                and (
                    ancienne_offre is None
                    or ancienne_offre.statut != 'acceptee'
                )
            )

            super().save(*args, **kwargs)

            if devient_acceptee:
                expedition.objects.filter(
                    pk=self.expedition_id
                ).update(statut='attribuee')

                offre.objects.filter(
                    expedition_id=self.expedition_id,
                    statut='proposee'
                ).exclude(
                    pk=self.pk
                ).update(statut='refusee')