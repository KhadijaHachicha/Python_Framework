from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Entreprise
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from .forms import EntrepriseForm
from .forms import RegisterUserForm
from django.shortcuts import redirect

def home(request):
    return HttpResponse("<h1> Welcome To Entreprise Application </h1>")


def welcome(request, name):
    return HttpResponse(f"hello {name}")


def listEntreprises(request):
    liste = Entreprise.objects.all().order_by("raison_social")
    return render(request, 'entreprise/list.html', {"list": liste})


def detailEntreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    return render(request, 'entreprise/details.html', {"entreprise": entreprise})


# Class-based views
class Liste_entreprise(ListView):
    model = Entreprise
    template_name = 'entreprise/list.html'
    context_object_name = 'list'


class Detail_entreprise(DetailView):
    model = Entreprise
    template_name = 'entreprise/details.html'
    context_object_name = 'entreprise'


class Delete_entreprise(DeleteView):
    model = Entreprise
    template_name = 'entreprise/delete.html'
    success_url = reverse_lazy('Entreprise:liste_classe')


class CreateEntreprise(CreateView):
    model = Entreprise
    template_name = 'entreprise/forms.html'
    form_class = EntrepriseForm
    success_url = reverse_lazy('Entreprise:liste_classe')


class UpdateEntreprise(UpdateView):
    model = Entreprise
    template_name = 'entreprise/forms.html'
    form_class = EntrepriseForm
    success_url = reverse_lazy('Entreprise:liste_classe')


# Alias for naming consistency
Update_entreprise = UpdateEntreprise
def register(request):
    if request.method=='POST':
        form= RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form =RegisterUserForm()
    return render(request , 'register.html', {'form':form})

