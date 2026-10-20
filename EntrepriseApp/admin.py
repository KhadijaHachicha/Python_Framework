from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from OffreApp.models import Offre
from VehiculeApp.models import Vehicule
from .models  import Entreprise , Utilisateur
# Register your models here.
admin.site.site_header = 'TransConnect - Administration'
admin.site.site_title = 'TransConnect'
admin.site.index_title = 'Tableau de bord' 
class VehiculeInline(admin.TabularInline): 
    model = Vehicule 
    extra = 0 
    fields = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible') 
    show_change_link=True
class OffreInline(admin.StackedInline): 
    model = Offre 
    extra = 0 
    fk_name = 'expedition' 
    readonly_fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut') 
    show_change_link = True 
    can_delete = False 
class UserAdmin(UserAdmin):
    list_display = ('user_id','username','email','telephone','is_active','created_at','role')
    list_editable = ('username','is_active',)
    search_fields = ('raison_sociale', 'matricule_fiscal') 
    list_filter = ('is_active','role')
    list_per_page = 1
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields":(
                    "username",
                    "usable_password",
                    "password1",
                    "password2",
                    "email",
                    "telephone",
                    "role",


                ),
            },
        ),
    )
admin.site.register(Utilisateur,UserAdmin) 
class EntrepriseAdmin(admin.ModelAdmin): 
    search_fields = ('raison_sociale', 'matricule_fiscal') 
    inlines = [VehiculeInline]

admin.site.register(Entreprise, EntrepriseAdmin)
