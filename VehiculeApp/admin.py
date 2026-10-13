from django.contrib import admin
from .models import Vehicule

# Register your models here.
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display=('immatriculation','type_vehicule','capacite_kg','disponible')
    readonly_fields=('created_at','updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('immatriculation', 'type_vehicule', 'capacite_kg')
        }),
        ('Statut et rattachement', {
            'fields': ('disponible', 'entreprise')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )