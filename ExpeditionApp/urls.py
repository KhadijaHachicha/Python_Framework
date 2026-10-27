from django.urls import path 
from .views import home
from .views import welcome , listExpeditions, detailExpedition

app_name= 'ExpeditionApp'
urlpatterns=[
    
    path('w/str:name>/',welcome, name="welcomeFunction"),
    path('home/', home, name="home"),
    path('list/',listExpeditions,name="list"),
    path('details/<int:id>/', detailExpedition,name="details")
    
]
