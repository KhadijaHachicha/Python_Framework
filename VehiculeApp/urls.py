from django.urls import path
from .views import (
    home,
    welcome,
    listVehicules,
    detailVehicule,
    Liste_vehicule,
    Detail_vehicule,
    Delete_vehicule,
    CreateVehicule,
    UpdateVehicule,
)

app_name = 'Vehicule'

urlpatterns = [
    path('w/<str:name>/', welcome, name="welcomeFunction"),
    path('home/', home, name="home"),

    # Function-based views
    path('list/', listVehicules, name='list_vehicules'),
    path('list/', listVehicules, name='list'),
    path('detail/<int:id>/', detailVehicule, name='detail_vehicule'),
    path('details/<int:id>/', detailVehicule, name='details'),

    # Class-based views
    path('liste/', Liste_vehicule.as_view(), name='liste_classe'),
    path('liste/', Liste_vehicule.as_view(), name='liste_vehicule'),
    path('detail_classe/<int:pk>/', Detail_vehicule.as_view(), name='detail_classe'),
    path('delete/<int:pk>/', Delete_vehicule.as_view(), name='delete_vehicule'),
    path('create/', CreateVehicule.as_view(), name='create_vehicule'),
    path('update/<int:pk>/', UpdateVehicule.as_view(), name='update_vehicule'),
    path('update_classe/<int:pk>/', UpdateVehicule.as_view(), name='update_classe'),
]
