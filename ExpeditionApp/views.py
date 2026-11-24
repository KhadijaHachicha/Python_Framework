from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Expedition
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExpeditionForm


def home(request):
    return HttpResponse("<h1> Welcome To Expedition Application  </h1>")


def welcome(request, name):
    return HttpResponse(f"hello {name}")


def listExpeditions(request):
    liste = Expedition.objects.filter(statut="publiee").order_by("ville_depart")
    return render(request, 'expedition/list.html', {"list": liste})


def detailExpedition(request, id):
    expedition = get_object_or_404(Expedition, id=id)
    return render(request, 'expedition/details.html', {"expedition": expedition})


# Class-based views
class Liste_expedition(ListView):
    model = Expedition
    template_name = 'expedition/list.html'
    context_object_name = 'list'


class Detail_expedition(DetailView):
    model = Expedition
    template_name = 'expedition/details.html'
    context_object_name = 'expedition'


class Delete_expedition(DeleteView):
    model = Expedition
    template_name = 'expedition/delete.html'
    success_url = reverse_lazy('Expedition:liste_classe')  # redirection vers la liste après suppression


class CreateExpedition(CreateView):
    model = Expedition
    template_name = 'expedition/forms.html'
    form_class = ExpeditionForm
    success_url = reverse_lazy('Expedition:liste_classe')


class UpdateExpedition(LoginRequiredMixin, UpdateView):
    model = Expedition
    template_name = 'expedition/forms.html'
    form_class = ExpeditionForm
    success_url = reverse_lazy('Expedition:liste_classe')

Update_expedition = UpdateExpedition
