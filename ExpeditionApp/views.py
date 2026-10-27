from django.shortcuts import render
from django.http import HttpResponse
from .models import Expedition

def home(request):
    return HttpResponse("<h1> Welcome To Expedition Application  </h1>")


def welcome(request, name ):
    return HttpResponse(f"hello {name}")

def listExpeditions(request):
    liste = Expedition.objects.filter(statut="publiee").order_by("ville_depart")
    return render (request,'expedition/list.html', {"list":liste} )

def detailExpedition(request ,id ):
    expedition = Expedition.objectifs.get(id=id)
    return render(request, 'expedition/details.html',{"expedition": expedition})
# Create your views here.
