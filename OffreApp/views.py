from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Offre
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from .forms import OffreForm


def home(request):
    return HttpResponse("<h1> Welcome To Offre Application </h1>")


def welcome(request, name):
    return HttpResponse(f"hello {name}")


def listOffres(request):
    liste = Offre.objects.all().order_by("-date_proposition")
    return render(request, 'offre/list.html', {"list": liste})


def detailOffre(request, id):
    offre = get_object_or_404(Offre, id=id)
    return render(request, 'offre/details.html', {"offre": offre})


# Class-based views
class Liste_offre(ListView):
    model = Offre
    template_name = 'offre/list.html'
    context_object_name = 'list'


class Detail_offre(DetailView):
    model = Offre
    template_name = 'offre/details.html'
    context_object_name = 'offre'


class Delete_offre(DeleteView):
    model = Offre
    template_name = 'offre/delete.html'
    success_url = reverse_lazy('Offre:liste_classe')


class CreateOffre(CreateView):
    model = Offre
    template_name = 'offre/forms.html'
    form_class = OffreForm
    success_url = reverse_lazy('Offre:liste_classe')


class UpdateOffre(UpdateView):
    model = Offre
    template_name = 'offre/forms.html'
    form_class = OffreForm
    success_url = reverse_lazy('Offre:liste_classe')


# Alias for naming consistency
Update_offre = UpdateOffre
