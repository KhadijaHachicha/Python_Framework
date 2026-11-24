from django.urls import path
from .views import (
    home,
    welcome,
    listOffres,
    detailOffre,
    Liste_offre,
    Detail_offre,
    Delete_offre,
    CreateOffre,
    UpdateOffre,
)

app_name = 'Offre'

urlpatterns = [
    path('w/<str:name>/', welcome, name="welcomeFunction"),
    path('home/', home, name="home"),

    # Function-based views
    path('list/', listOffres, name='list_offres'),
    path('list/', listOffres, name='list'),
    path('detail/<int:id>/', detailOffre, name='detail_offre'),
    path('details/<int:id>/', detailOffre, name='details'),

    # Class-based views
    path('liste/', Liste_offre.as_view(), name='liste_classe'),
    path('liste/', Liste_offre.as_view(), name='liste_offre'),
    path('detail_classe/<int:pk>/', Detail_offre.as_view(), name='detail_classe'),
    path('delete/<int:pk>/', Delete_offre.as_view(), name='delete_offre'),
    path('create/', CreateOffre.as_view(), name='create_offre'),
    path('update/<int:pk>/', UpdateOffre.as_view(), name='update_offre'),
    path('update_classe/<int:pk>/', UpdateOffre.as_view(), name='update_classe'),
]
