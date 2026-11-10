from django.urls import path
from .views import (home,welcome,listExpeditions,detailExpedition,Liste_expedition,Detail_expedition,Delete_expedition,CreateExpedition,UpdateExpedition,
)

app_name = 'Expedition'

urlpatterns = [
    path('w/<str:name>/', welcome, name="welcomeFunction"),
    path('home/', home, name="home"),

    path('list/', listExpeditions, name='list_expeditions'),
    path('list/', listExpeditions, name='list'),
    path('detail/<int:id>/', detailExpedition, name='detail_expedition'),
    path('details/<int:id>/', detailExpedition, name='details'),

    path('liste/', Liste_expedition.as_view(), name='liste_classe'),
    path('liste/', Liste_expedition.as_view(), name='liste_expedition'),
    path('detail_classe/<int:pk>/', Detail_expedition.as_view(), name='detail_classe'),
    path('delete/<int:pk>/', Delete_expedition.as_view(), name='delete_expedition'),
    path('create/', CreateExpedition.as_view(), name='create_expedition'),
    path('update/<int:pk>/', UpdateExpedition.as_view(), name='update_expedition'),
    path('update_classe/<int:pk>/', UpdateExpedition.as_view(), name='update_classe'),
]
