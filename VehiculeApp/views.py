from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Vehicule
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from .forms import VehiculeForm


def home(request):
    return HttpResponse("<h1> Welcome To Vehicule Application </h1>")


def welcome(request, name):
    return HttpResponse(f"hello {name}")


def listVehicules(request):
    liste = Vehicule.objects.all().order_by("immatriculation")
    return render(request, 'vehicule/list.html', {"list": liste})


def detailVehicule(request, id):
    vehicule = get_object_or_404(Vehicule, id=id)
    return render(request, 'vehicule/details.html', {"vehicule": vehicule})


# Class-based views
class Liste_vehicule(ListView):
    model = Vehicule
    template_name = 'vehicule/list.html'
    context_object_name = 'list'


class Detail_vehicule(DetailView):
    model = Vehicule
    template_name = 'vehicule/details.html'
    context_object_name = 'vehicule'


class Delete_vehicule(DeleteView):
    model = Vehicule
    template_name = 'vehicule/delete.html'
    success_url = reverse_lazy('Vehicule:liste_classe')


class CreateVehicule(CreateView):
    model = Vehicule
    template_name = 'vehicule/forms.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('Vehicule:liste_classe')


class UpdateVehicule(UpdateView):
    model = Vehicule
    template_name = 'vehicule/forms.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('Vehicule:liste_classe')


# Alias for naming consistency
Update_vehicule = UpdateVehicule
