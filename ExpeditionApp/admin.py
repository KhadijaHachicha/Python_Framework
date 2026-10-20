from django.contrib import admin
from django.utils import timezone
from .models import Expedition


class EnRetardFilter(admin.SimpleListFilter):
    title = "en retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return [("oui", "Oui"), ("non", "Non")]

    def queryset(self, request, queryset):
        aujourd_hui = timezone.now()
        if self.value() == "oui":
            return queryset.filter(statut="publiee", date_souhaitee__lt=aujourd_hui)
        if self.value() == "non":
            return queryset.exclude(statut="publiee", date_souhaitee__lt=aujourd_hui)
        return queryset


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):         
    list_display = (
        "reference", "ville_depart", "ville_arrive",
        "statut", "date_souhaitee", "poids_kg",
    )
    list_filter = ("statut", "ville_depart","ville_arrive", EnRetardFilter)
    search_fields = ("reference", "ville_depart", "ville_arrive")
    readonly_fields = ("created_at", "updated_at", "reference")
    ordering = ("-date_souhaitee",)

    fieldsets = (
        ("Détails de l'expédition", {
            "fields": (
                "reference",
                "ville_depart", "ville_arrive",
                "poids_kg", "date_souhaitee",
                "description", "statut", "entreprise",
            ),
        }),
        ("Horodatage", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
