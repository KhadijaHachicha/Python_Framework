from django.contrib import admin
from .models import Vehicule
# Register your models here.
@admin.register(Vehicule)
class vehicule_admin(admin.ModelAdmin):
    list_display = ('immatriculation','capacite_kg','created_at','disponible')
    readonly_fields = ('created_at','updated_at')
    search_fields = ('immatriculation', 'type_vehicule','capacite_kg')
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
 
#admin.site.register(vehicule)