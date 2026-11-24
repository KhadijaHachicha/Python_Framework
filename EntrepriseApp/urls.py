from django.urls import path
from .views import (
    home,
    welcome,
    listEntreprises,
    detailEntreprise,
    Liste_entreprise,
    Detail_entreprise,
    Delete_entreprise,
    CreateEntreprise,
    UpdateEntreprise,
)

app_name = 'Entreprise'

urlpatterns = [
    path('w/<str:name>/', welcome, name="welcomeFunction"),
    path('home/', home, name="home"),

    # Function-based views
    path('list/', listEntreprises, name='list_entreprises'),
    path('list/', listEntreprises, name='list'),
    path('detail/<int:id>/', detailEntreprise, name='detail_entreprise'),
    path('details/<int:id>/', detailEntreprise, name='details'),

    # Class-based views
    path('liste/', Liste_entreprise.as_view(), name='liste_classe'),
    path('liste/', Liste_entreprise.as_view(), name='liste_entreprise'),
    path('detail_classe/<int:pk>/', Detail_entreprise.as_view(), name='detail_classe'),
    path('delete/<int:pk>/', Delete_entreprise.as_view(), name='delete_entreprise'),
    path('create/', CreateEntreprise.as_view(), name='create_entreprise'),
    path('update/<int:pk>/', UpdateEntreprise.as_view(), name='update_entreprise'),
    path('update_classe/<int:pk>/', UpdateEntreprise.as_view(), name='update_classe'),
]
